#!/usr/bin/env python3
"""The prompt bound to its version (workshop lesson 3.6): what make prompt-version runs.

    python commands/prompt_pin.py              # from deploy/: the label, the text's sha256, the registry's verdict
    python commands/prompt_pin.py --kit DIR    # the same check on another copy of the kit

The label is the one the rag-api answers under: config.py's prompt_id and prompt_version, joined as /version joins
them (main.py: f"{settings.prompt_id}@{settings.prompt_version}"), so documind-rag@v3. main.py's usage_row() writes
the version on every row it makes, and the answer cache's scope includes it (semantic_cache.scope_of).

The text is generator.py's SYSTEM followed by DATED_RULE: generate() and generate_stream() start every prompt with
f"{SYSTEM}{_dated_rule(packed)}", with nothing between the two and the rule only when a packed chunk carries an
effective date. The sha256 is of that text in UTF-8, the instructions as the default backend (MODEL_BACKEND=vertex)
sends them; the gateway backend splits the same prompt into two turns and adds GATEWAY_JSON_RULE, which is not hashed
here. The registry, services/rag-api/prompt_versions.json, maps every registered label to its text's sha256.

The rule: a changed prompt needs a new version. When SYSTEM or DATED_RULE changes and prompt_version does not, the
label's registered sha256 is another text's, and this exits 1 with the version to set and the line to add. The lines
already there stay: a registered version never changes its sha256. commands/tests/test_prompt_versions.py pins v3's,
and holds evals/make_trainset.py's copy of SYSTEM equal to the generator's, so a tuned model is served behind the
prompt it was trained behind (lesson 12.1).

Standard library only. The rag-api is read as text and by AST, never imported: its modules need google-genai,
fastapi and pydantic-settings, config.py's settings need GOOGLE_CLOUD_PROJECT, and generator.py builds a Gemini
client at import. So this runs offline, with no credential, at Rs 0. It checks the code, not a deployed service: a
PROMPT_VERSION in a service's environment overrides config.py's default (pydantic-settings reads it), and that
service's /version names what it serves.

Exit 0: the label is registered with its text's sha256. 1: the label is registered to another text, or not at all.
2: a file is missing, or not in the shape read here.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import re
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]          # deploy/: the root of the learner's clone
GENERATOR = "services/rag-api/generator.py"
CONFIG = "services/rag-api/config.py"
REGISTRY = "services/rag-api/prompt_versions.json"
# How generate() and generate_stream() join SYSTEM and DATED_RULE. If either line changes, the text hashed below may
# no longer be what the model receives, so the check stops (exit 2) instead of guessing.
JOIN = '    prompt = f"{SYSTEM}{_dated_rule(packed)}\\n\\nContext:\\n{context}\\n\\nQuestion: {query}"'
DATED = '    return DATED_RULE if any(c.get("effective_from") for c in packed) else ""'
SHA256 = re.compile(r"[0-9a-f]{64}")


class Unreadable(Exception):
    """A file the check reads is missing, or not in the shape it reads: exit 2, never a guess."""


def read(kit: Path, rel: str) -> str:
    try:
        return (kit / rel).read_text(encoding="utf-8")
    except OSError as e:
        raise Unreadable(f"{rel}: cannot read it ({e.strerror or e})") from None


def parse(source: str, rel: str) -> ast.Module:
    try:
        return ast.parse(source)
    except SyntaxError as e:
        raise Unreadable(f"{rel}: does not parse (line {e.lineno})") from None


def prompt_text(generator: str) -> str:
    """SYSTEM + DATED_RULE, as generate() joins them: each set once, at module level, to a string literal."""
    if generator.count(JOIN) != 2 or DATED not in generator:
        raise Unreadable(f"{GENERATOR}: generate() and generate_stream() no longer start the prompt with SYSTEM, then "
                         "DATED_RULE, so their sha256 may not be what the model receives: update commands/prompt_pin.py")
    found: dict[str, list] = {"SYSTEM": [], "DATED_RULE": []}
    for node in parse(generator, GENERATOR).body:
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, (ast.AnnAssign, ast.AugAssign)):
            targets = [node.target]
        else:
            continue
        for t in targets:
            if isinstance(t, ast.Name) and t.id in found:
                found[t.id].append(node)
    text = ""
    for name, nodes in found.items():
        node = nodes[0] if len(nodes) == 1 else None
        try:
            value = ast.literal_eval(node.value) if isinstance(node, (ast.Assign, ast.AnnAssign)) and node.value else None
        except (ValueError, TypeError):
            value = None
        if not isinstance(value, str):
            raise Unreadable(f"{GENERATOR}: {name} must be set once, at module level, to a string literal")
        text += value
    return text


def label(config: str) -> str:
    """prompt_id@prompt_version: their defaults in config.py's settings class, a string or Field("..."), as /version
    joins them."""
    found: dict[str, list] = {"prompt_id": [], "prompt_version": []}
    for node in ast.walk(parse(config, CONFIG)):
        if isinstance(node, ast.ClassDef):
            for st in node.body:
                if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name) and st.target.id in found:
                    found[st.target.id].append(st.value)
    parts = []
    for name, values in found.items():
        value = values[0] if len(values) == 1 else None
        if isinstance(value, ast.Call) and getattr(value.func, "id", "") == "Field" and value.args:
            value = value.args[0]                      # Field("v3", alias=...): the default comes first
        if not (isinstance(value, ast.Constant) and isinstance(value.value, str) and value.value):
            raise Unreadable(f"{CONFIG}: {name} must be declared once in the settings class, with a string default")
        parts.append(value.value)
    return "@".join(parts)


def registry(text: str) -> dict[str, str]:
    """The registry's "versions": label -> sha256. A label written twice, or a value that is not a sha256, is refused."""
    def once(pairs):
        keys = [k for k, _ in pairs]
        twice = sorted({k for k in keys if keys.count(k) > 1})
        if twice:
            raise Unreadable(f"{REGISTRY}: {', '.join(twice)} written twice; a version has one sha256")
        return dict(pairs)
    try:
        doc = json.loads(text, object_pairs_hook=once)
    except ValueError as e:
        raise Unreadable(f"{REGISTRY}: not JSON ({e})") from None
    versions = doc.get("versions") if isinstance(doc, dict) else None
    if not isinstance(versions, dict) or not versions:
        raise Unreadable(f'{REGISTRY}: no "versions" object of label -> sha256')
    bad = sorted(k for k, v in versions.items() if not (isinstance(v, str) and SHA256.fullmatch(v)))
    if bad:
        raise Unreadable(f"{REGISTRY}: not a sha256 (64 lower-case hex digits): {', '.join(bad)}")
    return versions


def next_version(name: str, versions: dict) -> str:
    """The version after the highest vN of this prompt_id, registered or in use: documind-rag@v3 gives v4."""
    prompt_id = name.split("@", 1)[0]
    numbers = []
    for key in [*versions, name]:
        m = re.fullmatch(re.escape(prompt_id) + r"@v(\d+)", key)
        if m:
            numbers.append(int(m.group(1)))
    return f"v{max(numbers) + 1}" if numbers else "<new version>"


def check(kit: Path = KIT) -> tuple[int, list[str]]:
    """(exit code, lines to print): 0 when the label config.py serves under is registered with its text's sha256."""
    text = prompt_text(read(kit, GENERATOR))
    name = label(read(kit, CONFIG))
    versions = registry(read(kit, REGISTRY))
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    lines = [f"prompt:   {name} ({CONFIG}: prompt_id@prompt_version, as /version reports it)",
             f"text:     SYSTEM + DATED_RULE, {len(text)} characters, as generate() joins them ({GENERATOR})",
             f"sha256:   {digest}"]
    if versions.get(name) == digest:
        return 0, lines + [f"registry: {name} has this sha256 ({REGISTRY}): the text is the one its version names"]
    same = sorted(k for k, v in versions.items() if v == digest)     # labels already registered to this text
    switch = f'set prompt_version to "{same[0].split("@", 1)[1]}" in {CONFIG}' if same else ""

    def add(new_label: str) -> list[str]:
        return [f'    "{new_label}": "{digest}"', f'to "versions" in {REGISTRY}, keeping the lines already there.']

    if name not in versions:
        lines += [f"registry: {name} is not registered ({REGISTRY})", "Register it: add", *add(name)]
        if same:
            lines.append(f"Or, since this text is registered as {same[0]}, {switch}.")
    elif same:
        lines += [f"registry: {name} has another sha256, {versions[name]}",
                  f"This text is registered as {same[0]}: {switch}, or restore {name}'s text."]
    else:
        new = next_version(name, versions)
        lines += [f"registry: {name} has another sha256, {versions[name]}: SYSTEM or DATED_RULE changed and "
                  "prompt_version did not",
                  f'A changed prompt needs a new version. Set prompt_version to "{new}" in {CONFIG}, then add',
                  *add(f"{name.split('@', 1)[0]}@{new}")]
    return 1, lines


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="The prompt bound to its version: config.py's label, the sha256 of "
                                 "generator.py's SYSTEM + DATED_RULE, and services/rag-api/prompt_versions.json.")
    ap.add_argument("--kit", type=Path, default=KIT, help="the kit's root, deploy/ (default: the one this file is in)")
    args = ap.parse_args(argv)
    try:
        code, lines = check(args.kit)
    except Unreadable as e:
        print(f"prompt_pin: {e}", file=sys.stderr)
        return 2
    print("\n".join(lines))
    return code


if __name__ == "__main__":
    sys.exit(main())
