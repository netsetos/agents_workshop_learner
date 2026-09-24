"""Lesson 7.1 / s7: Paraphrase pairs and generated candidates: two kinds of row that are not golden

Summary and purpose:
The answer cache of Module 9 serves an earlier answer when a new question's embedding has a cosine similarity of at least 0.95 with an earlier one. That number was chosen, not measured. paraphrases.jsonl is what measures it. Each pair rewords a golden question. A pair marked same asks the same fact in other words, so a cache hit would be right. A pair marked different is a few words away with a different answer: E3 against E2, minimum against maximum, probation against confirmed. A cache hit there is a wrong answer served fast. cache_threshold.py embeds both sides and prints, for each candidate threshold, the hit rate on the same pairs and the false-hit rate on the different ones. The cache stays off until a threshold has no false hit on this set. The labels are yours to get right: the self-test checks that each pair names a real golden row and differs from its question, not that its label is true. Add two pairs against lk-32. One asks the same fact in other words. The other asks the clause's other fact, the kind of near miss a loose threshold would answer with 45 days.

HTML instruction: bash — run in the operator shell, in the kit (two lines appended to evals/paraphrases.jsonl, then the offline self-test)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_06_01_do_it
Expected observation: 44 pairs; the last two are against lk-32
selftest OK - 44 pairs (25 same, 19 different) name real golden rows and differ from them; the curve counts hits and false hits per threshold; the recommendation is the lowest threshold with no false hit

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/07-evaluation/7.1-eval-dataset/Netsetos_GCP_Capstone_7.1_Eval_Dataset_WIX.html#L850

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False

# The lesson's actual kit commands, visible here in the same order.
COMMANDS = """python - <<'PY'
import json
from pathlib import Path
p = Path("evals/paraphrases.jsonl")
new = [{"id": "pp-43", "of": "lk-32", "question": "After how many days without use is an account switched off?",
        "same": True, "why": "reworded", "tenant": "acme"},
       {"id": "pp-44", "of": "lk-32", "question": "How often is production access reviewed?",
        "same": False, "why": "the same clause, another fact: quarterly, not 45 days", "tenant": "acme"}]
keep = [l for l in p.read_text(encoding="utf-8").splitlines() if l.strip() and json.loads(l)["id"] not in ("pp-43", "pp-44")]
p.write_text("\\n".join(keep + [json.dumps(r, ensure_ascii=False) for r in new]) + "\\n", encoding="utf-8", newline="\\n")
print(len(keep) + len(new), "pairs; the last two are against lk-32")
PY
python evals/cache_threshold.py --selftest
"""


def demonstrate(session):
    """Run Paraphrase pairs at this checkpoint.

    The answer cache of Module 9 serves an earlier answer when a new question's embedding has a cosine similarity of at least 0.95 with an earlier one. That number was chosen, not measured. paraphrases.jsonl is what measures it. Each pair rewords a golden question. A pair marked same asks the same fact in other words, so a cache hit would be right. A pair marked different is a few words away with a different answer: E3 against E2, minimum against maximum, probation against confirmed. A cache hit there is a wrong answer served fast. cache_threshold.py embeds both sides and prints, for each candidate threshold, the hit rate on the same pairs and the false-hit rate on the different ones. The cache stays off until a threshold has no false hit on this set. The labels are yours to get right: the self-test checks that each pair names a real golden row and differs from its question, not that its label is true. Add two pairs against lk-32. One asks the same fact in other words. The other asks the clause's other fact, the kind of near miss a loose threshold would answer with 45 days.

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (two lines appended to evals/paraphrases.jsonl, then the offline self-test).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    # Preserve the kit CLI's arguments, conditions and observation order.
    session.shell(COMMANDS)


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
