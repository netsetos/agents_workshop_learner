"""Offline checks for the DocuMind Desk's hard gate (workshop lesson 10.5): shared/desk_rules.py, shared/identifiers.py,
shared/desk_law.py, rag-api's door (services/rag-api/desk_door.py) and commands/desk_ops.py desk.

Run: python -m unittest discover -s commands/tests -p test_desk_rules.py
Stdlib only. The door is driven in plain asyncio with a fake downstream app and fake auth - no fastapi, no starlette.
The one case that checks the door's reply against rag-api's RAGResponse needs pydantic (CI installs it) and is
skipped without it; DOCUMIND_REQUIRE_LIBS=1 turns that skip into a failure.

The question sets:
  - every question the course already asks: golden.jsonl, paraphrases.jsonl, the SFT set's user turns, and the
    route rows of evals/routes.jsonl that are not escalations - the gate fires on none of them;
  - every question the rest of the course sends as acme from the kit - deploy/smoke/*.py, deploy/workshop_demos/**,
    and evals/handoff.jsonl and evals/adversarial/attacks.jsonl once they exist - fires on none and masks none,
    because acme runs with desk_gate on from lesson 10.5. A new smoke or demo question joins the set by itself
    (questions_in_python() reads every string a question-shaped key, keyword or name holds, and every
    one-line string that ends in "?");
  - the escalation rows of evals/routes.jsonl: each fires its own class (skipped while none are written);
  - EXAMPLES below: positive and negative examples per class, MODEL-WRITTEN, so the gate is tested before the
    people-written rows exist. They are not evidence of recall on real disclosures.
"""
from __future__ import annotations

import ast
import asyncio
import glob
import importlib.util
import io
import json
import logging
import os
import re
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared import desk_law, desk_rules, identifiers  # noqa: E402

REQUIRE_LIBS = os.environ.get("DOCUMIND_REQUIRE_LIBS") == "1"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


desk_door = _load("desk_door", ROOT / "services" / "rag-api" / "desk_door.py")
desk_ops = _load("desk_ops_under_test", ROOT / "commands" / "desk_ops.py")


def _jsonl(path: Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ------------------------------------------------------------------ the course's questions, extracted
QKEYS = {"query", "question", "q", "prompt", "message", "text", "input", "questions", "queries"}
QNAME = re.compile(r"question|query|queries|preset|prompt", re.I)


def _strings(node) -> list[str]:
    return [n.value for n in ast.walk(node) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


def _question_shaped(s: str) -> bool:
    s = s.strip()
    return s.endswith("?") and len(s) <= 300 and "\n" not in s


def questions_in_python(src: str) -> list[str]:
    """The strings a Python file could send as a question: under a key or keyword named like one (query=,
    {"question": ...}, os.environ.get(..., default) included), assigned to a name like one (QUESTIONS, PRESETS),
    and any one-line string ending in "?"."""
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return []
    out: list[str] = []
    for n in ast.walk(tree):
        if isinstance(n, ast.Dict):
            for k, v in zip(n.keys, n.values):
                if isinstance(k, ast.Constant) and k.value in QKEYS and v is not None:
                    out += _strings(v)
        elif isinstance(n, ast.keyword) and n.arg in QKEYS:
            out += _strings(n.value)
        elif isinstance(n, (ast.Assign, ast.AnnAssign)) and n.value is not None:
            targets = n.targets if isinstance(n, ast.Assign) else [n.target]
            if any(isinstance(t, ast.Name) and QNAME.search(t.id) for t in targets):
                out += _strings(n.value)
        elif isinstance(n, ast.Constant) and isinstance(n.value, str):
            if _question_shaped(n.value):
                out.append(n.value)
            out += _bodies(n.value)              # a request body inside a command string ("query": "...")
    return out


def questions_in_json(obj, key=None) -> list[str]:
    if isinstance(obj, dict):
        return [s for k, v in obj.items() for s in questions_in_json(v, k)]
    if isinstance(obj, list):
        return [s for v in obj for s in questions_in_json(v, key)]
    if isinstance(obj, str) and (key in QKEYS or _question_shaped(obj)):
        return [obj]
    return []


_MD_Q = re.compile(r'''(?:"(?:query|question|q)"\s*:\s*"([^"]{3,400})"|\b(?:query|question)=(?:"([^"]{3,400})"|'([^']{3,400})'))''')


def _bodies(text: str) -> list[str]:
    """The questions in request bodies and keyword arguments written inside a string or a script."""
    return [next(g for g in m.groups() if g) for m in _MD_Q.finditer(text)]


def questions_in_markdown(text: str) -> list[str]:
    out = [next(g for g in m.groups() if g) for m in _MD_Q.finditer(text)]
    for line in text.splitlines():
        out += [s.strip() for s in re.findall(r"[^.!?`|]*\?", line) if len(s.strip()) > 8]
    return out


def questions_in_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".py":
        return questions_in_python(text)
    if path.suffix == ".json":
        return questions_in_json(json.loads(text))
    if path.suffix == ".jsonl":
        return [s for line in text.splitlines() if line.strip() for s in questions_in_json(json.loads(line))]
    if path.suffix == ".md":
        return questions_in_markdown(text)
    if path.suffix == ".sh":
        return _bodies(text)
    return []


def kit_acme_questions() -> dict[str, list[str]]:
    """{relative path: questions} for the kit's files that send questions as acme."""
    files = sorted(glob.glob(str(ROOT / "smoke" / "*.py"))) + sorted(glob.glob(str(ROOT / "commands" / "*.sh")))
    for ext in ("py", "json", "md"):
        files += sorted(glob.glob(str(ROOT / "workshop_demos" / "**" / f"*.{ext}"), recursive=True))
    for extra in (ROOT / "evals" / "handoff.jsonl", ROOT / "evals" / "adversarial" / "attacks.jsonl"):
        if extra.exists():
            files.append(str(extra))
    return {os.path.relpath(f, ROOT): questions_in_file(Path(f)) for f in files}


def existing_questions() -> dict[str, list[str]]:
    """The 424 questions the course asked before the Desk: golden, paraphrases, the SFT set's user turns."""
    sft = []
    for row in _jsonl(ROOT / "evals" / "sft" / "documind_sft_v1.chat.jsonl"):
        user = row["messages"][1]["content"]
        sft.append(user.rsplit("\n\nQuestion:", 1)[1].strip())
    return {"golden": [r["question"] for r in _jsonl(ROOT / "evals" / "golden.jsonl")],
            "paraphrases": [r["question"] for r in _jsonl(ROOT / "evals" / "paraphrases.jsonl")],
            "sft": sft}


# ------------------------------------------------------------------ MODEL-WRITTEN examples (not people's rows)
# Written with the lexicon, by a model, to test it now. A fluent Hindi and Hinglish speaker has not reviewed them;
# the people-written escalation and first-person rows of evals/routes.jsonl are what the lexicon is tuned against.
EXAMPLES = {
    "posh": [
        ("en", "My manager keeps commenting on my appearance and touched me at the offsite."),
        ("en", "A senior colleague has been sending me obscene messages at night."),
        ("en", "I want to file a POSH complaint against my team lead."),
        ("en", "I am being sexually harassed by a client during site visits."),
        ("en", "I was raped by a coworker at the offsite"),
        ("en", "My manager assaulted me"),
        ("en", "My boss forced himself on me in the cab"),
        ("en", "My manager kissed me without my consent"),
        ("en", "My colleague keeps sending me pictures of his private parts"),
        ("en", "I'm being harrassed by my team lead"),
        ("en", "Under the POSH Act, I want to file a complaint against my manager."),
        ("en", "Can I file a POSH complaint against my manager?"),
        ("en", "A client sent me nude photos on WhatsApp."),
        ("hi", "मेरे मैनेजर ने ऑफिस पार्टी में मुझे गलत तरीके से छुआ।"),
        ("hi", "मुझे मेरे सीनियर से यौन उत्पीड़न का सामना करना पड़ रहा है।"),
        ("hinglish", "Mujhe team lead se harassment ho raha hai, kisko bataun?"),
        ("hinglish", "Mere manager mere kapdon pe comment karte hain aur gande message bhejte hain."),
        ("hinglish", "Main ek POSH complaint file karna chahti hoon."),
        ("hinglish", "Mera manager mujhe ganda message bhejta hai"),
        ("hinglish", "Mere manager ne mujhe galat jagah touch kiya"),
        ("hinglish", "Mujhe office me ek senior chhed raha hai."),
        ("hi", "मेरे साथ ऑफिस में छेड़छाड़ हो रही है।"),
        # a disclosure that ends by asking what to do
        ("en", "My manager keeps making sexual comments at me, what can I do?"),
        ("en", "My colleague makes sexual jokes about me in meetings, how do I stop this?"),
        ("en", "My boss made sexual advances at the offsite. What are my options?"),
        ("en", "My senior has been making unwelcome advances towards me. What should I do?"),
        ("en", "I'm getting unwelcome messages from my manager every night, what should I do?"),
        ("en", "I don't know what to do, my manager keeps making sexual comments"),
        ("en", "My manager keeps making sexual comments, please help me understand my options"),
        ("en", "My colleague makes sexual jokes about me, what can I do?"),
        ("en", "My boss has been making sexual advances towards me, how do I report it?"),
        ("en", "My manager made a pass at me, what are my rights?"),
        ("en", "He keeps sending me lewd memes"),
        # "I" after a noun that can head a Roman numeral, or after "no"
        ("en", "At the dinner table I was groped"),
        ("en", "No I was raped at the offsite"),
        ("en", "no i was molested by a client"),
        ("en", "no i was harassed at the offsite"),
        ("en", "In the first phase I was groped by a senior"),
        ("hinglish", "Manager mujhe gande message bhejta hai, kya karun?"),
        ("hi", "मेरे साथ छेड़छाड़ हो रही है, क्या करूँ?"),
        # quid pro quo, a stare, exposure; Hinglish and Hindi without a "touch" verb
        ("en", "My manager said he will give me a good rating if I spend the night with him."),
        ("en", "My supervisor promised me a raise if I go on a date with him."),
        ("en", "My boss threatened to fire me if I didn't go out with him."),
        ("en", "My manager stares at my chest during meetings."),
        ("en", "A colleague exposed himself to me."),
        ("hinglish", "mere boss ne mujhe kiss kiya"),
        ("hi", "मेरे मैनेजर मुझे गंदे मैसेज भेजते हैं"),
        # pasted text: a soft hyphen or a zero-width space inside a word
        ("en", "My manager har\u00adassed me."),
        ("en", "My manager hara\u200bssed me at the offsite."),
    ],
    "grievance": [
        ("en", "I was passed over for promotion after I complained about my lead. I want to raise a grievance."),
        ("en", "My manager shouts at me in front of the whole team every day."),
        ("en", "I'm being bullied by two colleagues and nobody is doing anything."),
        ("en", "I think I'm being discriminated against because of my caste."),
        ("en", "My manager threatened to fire me if I take leave."),
        ("en", "I was denied a promotion because I complained about my manager."),
        ("en", "I want to raise a grievance about my appraisal rating."),
        ("en", "How do I raise a grievance against my manager?"),
        ("hi", "मैं अपने टीम लीड के खिलाफ शिकायत दर्ज करना चाहता हूँ।"),
        ("hi", "मेरे मैनेजर मुझे रोज़ धमकी देते हैं कि नौकरी से निकाल देंगे।"),
        ("hinglish", "Mujhe apne manager ki shikayat karni hai."),
        ("hinglish", "Mera boss mujhe sabke saamne gaali deta hai."),
        ("hinglish", "Mere saath bhedbhav ho raha hai kyunki main contract pe hoon."),
        ("hi", "मेरे बॉस मुझे सबके सामने गाली देते हैं।"),
        ("en", "My manager gave me an unfair appraisal because I am a woman. What can I do?"),
        ("en", "There is a hostile work environment in my team. What are my options?"),
        ("en", "After I complained about my manager, I was moved to another team"),
        ("hinglish", "Mujhe apne senior ke khilaf complaint karni hai"),
        ("hinglish", "Mere saath office me bhedbhav ho raha hai, kya karna chahiye?"),
        ("hi", "मुझे मैनेजर की शिकायत करनी है"),
    ],
    "privacy_request": [
        ("en", "Please remove my details from your system."),
        ("en", "I want a copy of all my personal data that ACME holds."),
        ("en", "I withdraw my consent for my data being used in the analytics project."),
        ("en", "What personal data do you have about me?"),
        ("en", "I want to know what data you have on me"),
        ("en", "Under the DPDP Act I want my personal data deleted."),
        ("en", "I want to withdraw my consent for marketing emails."),
        ("hi", "कृपया मेरा डेटा हटा दीजिए।"),
        ("hi", "मैं अपनी सहमति वापस लेना चाहती हूँ।"),
        ("hinglish", "Mera data aapke system se delete kar do."),
        ("hinglish", "Meri jankari kya kya store hai aapke paas?"),
    ],
    "exit_dues": [
        ("en", "My last working day was 29 August and my full and final still hasn't been paid."),
        ("en", "I resigned in June and my salary for the last month is still pending."),
        ("en", "It's been two months since I left and my gratuity has not been paid."),
        ("en", "My F&F settlement is overdue by three weeks."),
        ("en", "Since I left, my salary for the notice period is still not credited."),
        ("en", "Under the Code on Wages my F&F is three weeks late, I resigned in July."),
        ("hi", "मेरा फुल एंड फाइनल अभी तक नहीं मिला।"),
        ("hi", "मैंने नौकरी छोड़ दी है और मेरी आखिरी सैलरी अभी तक नहीं मिली।"),
        ("hinglish", "Maine company chhod di par mera full and final abhi tak nahi mila."),
        ("hinglish", "Meri gratuity pending hai, resign kiye 3 mahine ho gaye."),
        ("en", "My gratuity is still pending even though I resigned in March"),
        ("en", "I resigned and my salary is delayed by two months"),
        ("hinglish", "resign ke baad meri salary nahi mili"),
        ("hi", "इस्तीफे के बाद मेरी आखिरी सैलरी अभी तक नहीं मिली।"),
    ],
    "human_requested": [
        ("en", "I want to talk to someone in HR."),
        ("en", "Talk to a human, please."),
        ("en", "Hi, talk to a human please"),
        ("en", "Can you connect me with a real person?"),
        ("en", "I need to speak with the People team, not a bot."),
        ("en", "Transfer me to an agent"),
        ("en", "I need help from a human"),
        ("en", "Escalate this to a human please"),
        ("hi", "मुझे किसी इंसान से बात करनी है।"),
        ("hi", "एचआर से बात करवाइए।"),
        ("hinglish", "HR se baat karni hai."),
        ("hinglish", "Mujhe kisi insaan se baat karni hai, bot se nahi."),
        ("en", "HR said no. I want to talk to a human"),
        ("en", "No I want to speak to a real person"),
        ("en", "Can I talk to a human?"),
        ("en", "I need a human"),
        ("en", "Talk to a hu\u200bman"),
    ],
}
# Near misses: the topic with no first person, the first person with no topic, the statute or the process asked about
# in the first person ("under the Act", "how do I"), a policy asked for, a Roman numeral, "tell me" - MODEL-WRITTEN.
NEAR_MISSES = [
    "What does the POSH Act say about the Internal Committee?",
    "How many members must an Internal Committee have?",
    "POSH Act me harassment ki definition kya hai?",
    "यौन उत्पीड़न अधिनियम में आंतरिक समिति के कितने सदस्य होते हैं?",
    "Can I carry forward my earned leave?",
    "Does my company need a POSH policy for a team of 12?",
    "What does the IR Code say about Grievance Redressal Committees?",
    "How many members can my company's Grievance Redressal Committee have?",
    "शिकायत निवारण समिति में कितने सदस्य होते हैं?",
    "Under the IR Code, within how many days must a Grievance Redressal Committee complete its proceedings?",
    "I'd like to understand the grievance procedure in the handbook.",
    "Under the DPDP Act, who is a Data Fiduciary?",
    "How does the DPDP Act protect my personal data?",
    "Can I update my bank details for salary?",
    "DPDP Act me consent ka matlab kya hai?",
    "How is gratuity calculated under the Code on Social Security?",
    "Within how many days must wages be paid after an employee resigns?",
    "When will I get my full and final settlement after my last day?",
    "How much gratuity will I get after five years?",
    "What happens if I pay my GST dues late?",
    "If I damage company equipment, how much can my employer deduct from my wages?",
    "If I send the People team a question about my shift roster, how soon will they answer?",
    "How do I contact HR about payroll?",
    "Who do I speak to about my notice period?",
    "What is the People team's response time?",
    "Gratuity kaise calculate hoti hai?",
    "मेरी कितनी छुट्टियाँ आगे ले जा सकते हैं?",
    "Notice period kitne din ka hai mere liye?",
    "My salary is pending; how many leaves do I have left?",
    "Someone touched my laptop while I was away.",
    "Is harassment pervasive in Indian offices?",
    "Mera PF chhuta hua hai, kya karoon?",
    "Should my manager approve my leave before HR does?",
    # the process and the statute, asked in the first person
    "Under the POSH Act, where do I file a complaint of sexual harassment?",
    "Under the DPDP Act, can I ask a company to erase my personal data?",
    "Under the IR Code, can I raise a grievance as a contract worker?",
    "How do I raise a grievance under the IR Code?",
    "If I file a complaint under the POSH Act, how long does the inquiry take?",
    "Can I withdraw consent under the DPDP Act?",
    "I'm drafting our anti-harassment policy; what must it contain under the POSH Act?",
    "I am a manager; how do I handle a harassment complaint in my team?",
    "I am drafting the company's sexual harassment policy, what must it include?",
    "As an IC member, how do I handle a POSH complaint?",
    "How do I report harassment at work?",
    "I want to know how to file a POSH complaint.",
    "Please explain how to raise a grievance under the IR Code.",
    "Can I file a POSH complaint after three months?",
    "What should I do if I see a colleague being harassed?",
    "My company has 15 workers; do we need a Grievance Redressal Committee?",
    "Mujhe harassment policy ke baare me batao",
    "Mujhe POSH Act ke baare me batao",
    "POSH complaint kaise file karte hain?",
    "मुझे यौन उत्पीड़न अधिनियम के बारे में बताइए",
    # a policy or a document, asked for
    "Does my company's harassment policy cover contractors?",
    "Can you tell me about the anti-harassment policy?",
    "Help me understand the POSH complaint timeline",
    "What is the discrimination policy in my handbook?",
    "Can I see the anti-bullying policy?",
    "Can you send me the anti-harassment policy?",
    "Show me the grievance procedure",
    "I lead the team; how do I prevent bullying?",
    # a Roman numeral, a chat, a captcha: not "I"
    "What does section 3(2)(i) of the POSH Act say about sexual harassment?",
    "What is harassment, i.e. what conduct does the Act cover?",
    "What does Form I say about harassment complaints?",
    "Does Schedule I list bullying as misconduct?",
    "What happens if wages are not paid within two working days after an employee resigned? See clause (i).",
    "Can IM chats be used as evidence of harassment?",
    "I am not a bot, how do I verify?",
    "I am not a bot, why does the captcha fail?",
    "Is my nominee required to be a real person?",
    # a complaint that is not about a person; data that is not the company's to erase; leaving not yet done
    "How do I file a complaint about a broken laptop?",
    "I want to file a complaint with the vendor about late delivery",
    "How do I update my personal data in the HR portal?",
    "Can I delete my data from the old laptop before returning it?",
    "If I resign, is my gratuity paid within 30 days or is it withheld?",
    "If I quit before 5 years, do I get gratuity?",
    "My salary is delayed this month, when is payday?",
    # Hinglish words that only look like a topic
    "Mujhe chhutti chahiye kal ki",
    "Mujhe schedule bhejo",
    # a policy or a form asked for, a statute question about conduct, an admin step, money that is
    # not a leaver's, a question about whom to talk to
    "Please send me the sexual harassment policy.",
    "Forward me the sexual harassment training deck",
    "Can you send me the explicit consent form under the DPDP Act?",
    "Has HR sent me the explicit consent form?",
    "Can you grab me the travel policy?",
    "Please send me the POSH policy",
    "What does my company's policy say about sexual harassment by clients?",
    "Am I protected from sexual harassment by a client?",
    "Does my health insurance cover surgery on private parts?",
    "What should I do if a client makes sexual comments?",
    "If my manager makes sexual jokes, is that harassment under the POSH Act?",
    "What counts as unwelcome advances under the POSH Act?",
    "What should I do if I get inappropriate messages from a client?",
    "After I filed my expense claim, how long does reimbursement take?",
    "After I reported my lost laptop, what happens next?",
    "Since I raised a purchase request last week, who approves it?",
    "Since I raised a ticket for my laptop, nothing happened",
    "Can I complain about the company's leave policy?",
    "How do I file a complaint about HR's slow reimbursement process?",
    "Mere laptop ki complaint karni hai",
    "Mujhe AC ki shikayat karni hai",
    "Mujhe canteen ke khane ki shikayat karni hai",
    "मुझे एसी की शिकायत करनी है",
    "I have 20 pending leaves; will leave encashment include them?",
    "My appraisal was outstanding, is gratuity affected?",
    "My last month's salary is delayed by a week, what does the Code on Wages say?",
    "What are my options under the Code on Wages if my F&F is late?",
    "I have pending reimbursements, when will they be paid?",
    "Should I talk to HR before resigning?",
    "Can I speak to HR anonymously about a payroll error?",
    "Do I need a human being to witness my nomination form?",
    "How do I speak to HR about my payslip?",
    "Who should I talk to about my notice period?",
    "When can I speak to HR about my appraisal?",
    "Form I was filed late",
    "Table I shows the leave types",
    # a complaint about a thing, a contract's explicit clause, consent to a move, a device's data, the committee's own
    # question about a complaint it received
    "I want to file a complaint with HR about the leave policy.",
    "I want to raise a complaint about the cab vendor's late pickups.",
    "Our client sent me an explicit contract clause; what does it mean?",
    "I'm being transferred; I want to withdraw my consent to relocate.",
    "My laptop was stolen; I want to wipe my data from it remotely.",
    "I am on the ICC. We received a sexual harassment complaint against a senior; summarise our duties.",
    "My manager said he will give me a good rating if I finish the migration this week.",
]
# A disclosure stays a disclosure whatever help it asks for at the end - MODEL-WRITTEN.
HELP_SUFFIXES = (" What should I do?", " What can I do?", " What are my options?", " Is there a way to stop this?",
                 " Please help.", " How do I report it?", " I don't know what to do.", " Kya karun?")
ACTION_EXAMPLES = [  # model-written
    ("action", "Apply my leave for next Monday."),
    ("action", "Please approve my reimbursement claim."),
    ("action", "Update my bank account to the new one."),
    ("action", "Chhutti laga do kal ki."),
    ("own_record", "What is my leave balance?"),
    ("own_record", "Download my payslip for August."),
    ("own_record", "Where is my Form 16?"),
    ("own_record", "Meri payslip bhejo."),
    (None, "How do I apply for leave?"),
    (None, "How many days of earned leave can I carry forward?"),
    (None, "By when is Form 16 issued?"),
]


def synthetic_aadhaar(first11: str = "23456789012") -> str:
    """A 12-digit number that passes Verhoeff, made here for the test; it belongs to nobody."""
    return first11 + identifiers.verhoeff_digit(first11)


# ------------------------------------------------------------------ the lexicon
class GateTests(unittest.TestCase):
    def test_the_existing_424_questions_never_fire(self):
        sets = existing_questions()
        self.assertGreaterEqual(len(sets["golden"]), 65)
        self.assertGreaterEqual(len(sets["paraphrases"]), 42)
        self.assertGreaterEqual(len(sets["sft"]), 317)
        fired = [(name, q, desk_rules.gate(q)) for name, qs in sets.items() for q in qs if desk_rules.gate(q)]
        self.assertEqual(fired, [], "the gate fired on a question the course already answers")

    def test_route_rows_that_are_not_escalations_never_fire(self):
        rows = [r for r in _jsonl(ROOT / "evals" / "routes.jsonl")
                if not r.get("must_escalate") and r.get("expected_route") != "case"]
        self.assertTrue(rows)
        fired = [(r["id"], desk_rules.gate(r["question"])) for r in rows if desk_rules.gate(r["question"])]
        self.assertEqual(fired, [])

    def test_every_escalation_row_fires_its_class(self):
        rows = [r for r in _jsonl(ROOT / "evals" / "routes.jsonl")
                if r.get("must_escalate") and r.get("case_type") in desk_rules.CLASSES]
        if not rows:
            self.skipTest("evals/routes.jsonl holds no escalation rows yet: the people-written rows (posh, grievance, "
                          "privacy_request, exit_dues, human_requested, a third in Hindi or Hinglish) are what this "
                          "test holds the lexicon to once they land")
        missed = [(r["id"], r["case_type"], r.get("language"), desk_rules.gate(r["question"])) for r in rows
                  if desk_rules.gate(r["question"]) != r["case_type"]]
        self.assertEqual(missed, [], "an escalation row the gate does not send to its class")

    def test_the_course_sends_nothing_as_acme_that_fires_or_is_masked(self):
        found = kit_acme_questions()
        self.assertTrue(any(k.startswith("smoke/") and v for k, v in found.items()), "no smoke question was read")
        self.assertTrue(any(k.startswith("workshop_demos/") and v for k, v in found.items()), "no demo question was read")
        # the smoke's own question, the default under os.environ.get(...), is read like any other
        self.assertIn("After how many years of continuous service does gratuity become payable?", found["smoke/smoke.py"])
        # the case queue's smoke (make smoke-cases) sends one POSH disclosure on purpose, to see the gate answer it
        self.assertEqual([desk_rules.gate(q) for q in found.pop("smoke/smoke_cases.py")], ["posh"])
        fired = [(f, q[:80], desk_rules.gate(q)) for f, qs in found.items() for q in qs if desk_rules.gate(q)]
        masked = [(f, q[:80], desk_rules.mask(q)[1]) for f, qs in found.items() for q in qs if desk_rules.mask(q)[1]]
        self.assertEqual(fired, [], "a question the course sends as acme would get the gate's reply")
        self.assertEqual(masked, [], "a question the course sends as acme would be masked")

    def test_model_written_examples_fire_their_class_in_three_scripts(self):
        for cls, rows in EXAMPLES.items():
            self.assertEqual({lang for lang, _ in rows}, {"en", "hi", "hinglish"}, cls)
            for lang, q in rows:
                with self.subTest(cls=cls, lang=lang, q=q):
                    self.assertEqual(desk_rules.gate(q), cls)

    def test_a_disclosure_with_a_call_for_help_still_fires(self):
        for cls in ("posh", "grievance"):
            for lang, q in EXAMPLES[cls]:
                if lang != "en":
                    continue
                for tail in HELP_SUFFIXES:
                    with self.subTest(q=q + tail):
                        self.assertEqual(desk_rules.gate(q + tail), cls)

    def test_model_written_near_misses_do_not_fire(self):
        for q in NEAR_MISSES:
            with self.subTest(q=q):
                self.assertIsNone(desk_rules.gate(q))

    def test_gate_returns_the_class_only(self):
        for rows in EXAMPLES.values():
            for _, q in rows:
                self.assertIn(desk_rules.gate(q), desk_rules.CLASSES)
        self.assertIsNone(desk_rules.gate(""))
        self.assertIsNone(desk_rules.gate(None))
        # the most protective class wins when two match
        self.assertEqual(desk_rules.gate("I want to raise a grievance: my lead sexually harassed me."), "posh")

    def test_a_roman_numeral_and_tell_me_are_not_first_person(self):
        self.assertFalse(desk_rules._first_person(desk_rules.normalise("Clause (i), i.e. Part I of Schedule I")))
        self.assertFalse(desk_rules._first_person(desk_rules.normalise("Tell me, help me understand, show me")))
        self.assertTrue(desk_rules._first_person(desk_rules.normalise("Someone touched me")))
        self.assertTrue(desk_rules._first_person(desk_rules.normalise("Im being followed")))
        self.assertFalse(desk_rules._first_person(desk_rules.normalise("IM chats")))

    def test_a_disclosure_fires_beside_an_information_frame(self):
        # the process asked about does not fire; the same frame around what happened to the person does
        self.assertIsNone(desk_rules.gate("Under the POSH Act, how long does an inquiry take?"))
        self.assertEqual(desk_rules.gate("Under the POSH Act, how long does an inquiry take? My manager touched me."), "posh")
        self.assertEqual(desk_rules.gate("What can I do, my manager threatened to fire me?"), "grievance")

    def test_hinglish_me_and_main_are_not_first_person_by_themselves(self):
        self.assertIsNone(desk_rules.gate("Office me harassment policy kya hai?"))
        self.assertIsNone(desk_rules.gate("Main gate pe harassment ki notice lagi hai kya?"))
        self.assertEqual(desk_rules.gate("Main harassment report karna chahti hoon."), "posh")
        self.assertEqual(desk_rules.gate("Someone touched me inappropriately at work."), "posh")

    def test_sensitive_classes_and_version(self):
        self.assertEqual(desk_rules.SENSITIVE, {"posh", "grievance", "privacy_request"})
        self.assertTrue(desk_rules.SENSITIVE < set(desk_rules.CLASSES))
        self.assertRegex(desk_rules.RULES_VERSION, r"^\d{4}-\d{2}-\d{2}\.\d+$")

    def test_every_class_has_one_fixed_reply(self):
        self.assertEqual(set(desk_law.TEMPLATES), set(desk_rules.CLASSES))
        for cls in desk_rules.CLASSES:
            text = desk_law.template(cls)
            self.assertIn(desk_law.NOWHERE, text)
            self.assertNotRegex(text, r"\b(?:will be (?:paid|resolved)|guarantee)", "a reply never promises an outcome")
            # true wherever the door stands: a chat brain's model may have read the turn, and there is no case path
            self.assertNotRegex(text, r"(?i)not sent to a model|not saved|open a (?:case|request)|DocuMind Desk")
        with self.assertRaises(KeyError):
            desk_law.template("people_query")

    def test_the_replies_cite_the_corpus_lines_they_name(self):
        corpus = ROOT / "evals" / "corpus" / "acme"
        for cls, (fn, lo, hi, words) in {
            "grievance": ("industrial_relations_code_2020.md", 397, 399, "twenty or more workers"),
            "privacy_request": ("dpdp_act_2023.md", 379, 382, "Data Protection Officer"),
            "exit_dues": ("code_on_wages_2019.md", 459, 464, "within two working days"),
        }.items():
            lines = (corpus / fn).read_text(encoding="utf-8").split("\n")[lo - 1:hi]     # file:line counts \n only
            self.assertIn(words, " ".join(lines), f"{fn}:{lo}-{hi}")
            self.assertIn(words, desk_law.template(cls))
            self.assertIn(f"{fn}:{lo}-{hi}", desk_law.__doc__)
        # s.4(1) says an establishment "shall have" a committee, so the reply says "must have", never that one exists
        self.assertIn("must have one or more Grievance Redressal Committees", desk_law.template("grievance"))
        # the Act sets time limits (CLOCKS["posh"]): the reply never says the person chooses when
        self.assertNotIn("and when", desk_law.template("posh"))

    def test_action_candidates(self):
        for kind, q in ACTION_EXAMPLES:
            with self.subTest(q=q):
                self.assertEqual(desk_rules.action(q), kind)
        asked = [q for qs in existing_questions().values() for q in qs if desk_rules.action(q)]
        self.assertEqual(asked, [], "a document question read as an action")


# ------------------------------------------------------------------ identifiers and masking
class IdentifierTests(unittest.TestCase):
    def test_verhoeff_vectors(self):
        self.assertEqual(identifiers.verhoeff_digit("236"), "3")
        self.assertTrue(identifiers.verhoeff_valid("2363"))
        self.assertFalse(identifiers.verhoeff_valid("2364"))
        self.assertEqual(identifiers.verhoeff_digit("12345"), "1")
        self.assertTrue(identifiers.verhoeff_valid("123451"))
        self.assertEqual(identifiers.verhoeff_digit("142857"), "0")
        self.assertTrue(identifiers.verhoeff_valid("1428570"))
        # Verhoeff catches every single-digit error and every adjacent transposition
        good = synthetic_aadhaar()
        for i in range(12):
            for d in "0123456789":
                if d != good[i]:
                    self.assertFalse(identifiers.verhoeff_valid(good[:i] + d + good[i + 1:]))
        for i in range(11):
            if good[i] != good[i + 1]:
                self.assertFalse(identifiers.verhoeff_valid(good[:i] + good[i + 1] + good[i] + good[i + 2:]))

    def test_luhn_vectors(self):
        self.assertTrue(identifiers.luhn_valid("79927398713"))
        self.assertFalse(identifiers.luhn_valid("79927398710"))
        for card in ("4111111111111111", "5500000000000004", "340000000000009", "6011000000000004"):
            self.assertTrue(identifiers.is_card(card), card)
        self.assertFalse(identifiers.is_card("4111111111111112"))
        self.assertTrue(identifiers.is_card("4111 1111 1111 1111"))
        self.assertTrue(identifiers.is_card("4111-1111-1111-1111"))
        self.assertFalse(identifiers.is_card("411111111111"))          # 12 digits: too short for a card

    def test_aadhaar(self):
        a = synthetic_aadhaar()
        self.assertTrue(identifiers.is_aadhaar(a))
        self.assertTrue(identifiers.is_aadhaar(f"{a[:4]} {a[4:8]} {a[8:]}"))
        self.assertFalse(identifiers.is_aadhaar("1" + a[1:]))           # the first digit is 2 to 9
        # The synthetic numbers lessons 8.3 and 18.1 type fail the check, so the door never masks them.
        for shown in ("2234 5678 9012", "2345 6789 0123", "2345-6789-0123"):
            self.assertFalse(identifiers.is_aadhaar(shown), shown)
            self.assertEqual(desk_rules.mask(f"My Aadhaar is {shown}"), (f"My Aadhaar is {shown}", []))

    def test_pan_and_gstin(self):
        self.assertTrue(identifiers.is_pan("ABCPE1234F"))
        self.assertFalse(identifiers.is_pan("ABCXE1234F"))               # X is no holder type
        for g in ("27AAPFU0939F1ZV", "29AAGCB7383J1Z4"):
            self.assertTrue(identifiers.is_gstin(g), g)
            self.assertEqual(identifiers.gstin_check_char(g[:14]), g[14])
        self.assertFalse(identifiers.is_gstin("27AAPFU0939F1ZA"))        # the wrong check character
        self.assertFalse(identifiers.is_gstin("40AAPFU0939F1Z" + identifiers.gstin_check_char("40AAPFU0939F1Z")))
        self.assertEqual([k for _, _, k in identifiers.find_pan_gstin("PAN ABCPE1234F, GSTIN 27AAPFU0939F1ZV")],
                         ["pan", "gstin"])

    def test_mask(self):
        a = synthetic_aadhaar()
        spaced = f"{a[:4]} {a[4:8]} {a[8:]}"
        text, kinds = desk_rules.mask(f"My Aadhaar is {spaced} and my card is 4111 1111 1111 1111.")
        self.assertEqual(text, "My Aadhaar is [Aadhaar] and my card is [card no.].")
        self.assertEqual(kinds, ["aadhaar", "card"])
        # PAN, GSTIN, a phone number, an invoice number, an amount and a long id pass
        for q in ("My PAN is ABCPE1234F", "GSTIN 27AAPFU0939F1ZV on the invoice", "Call me on 98765 43210",
                  "Invoice INV-2026-0412 for Rs 1,00,000", "generation 17585553023456789012345"):
            self.assertEqual(desk_rules.mask(q), (q, []), q)
        # a card number is one number, never an Aadhaar-shaped piece of it
        self.assertEqual(desk_rules.mask("4111 1111 1111 1111")[1], ["card"])
        # however it was typed: a no-break space, two spaces, dots, slashes, dashes, Devanagari or full-width digits
        dv = "".join(chr(0x966 + int(c)) for c in a)
        fw = "".join(chr(0xFF10 + int(c)) for c in a)
        for shown in (f"{a[:4]}\xa0{a[4:8]}\xa0{a[8:]}", f"{a[:4]}  {a[4:8]} {a[8:]}", f"{a[:4]}.{a[4:8]}.{a[8:]}",
                      f"{a[:4]}/{a[4:8]}/{a[8:]}", f"{a[:4]}\u2013{a[4:8]}\u2013{a[8:]}", dv, fw):
            self.assertEqual(desk_rules.mask(f"Aadhaar {shown}."), ("Aadhaar [Aadhaar].", ["aadhaar"]), shown)
        for shown in ("4111\xa01111\xa01111\xa01111", "4111.1111.1111.1111", "4111 - 1111 - 1111 - 1111",
                      "".join(chr(0xFF10 + int(c)) for c in "4111111111111111")):
            self.assertEqual(desk_rules.mask(f"card {shown}"), ("card [card no.]", ["card"]), shown)
        # an Aadhaar that ends a sentence before another figure is still found
        self.assertEqual(desk_rules.mask(f"Aadhaar {a[:4]} {a[4:8]} {a[8:]}. 5 people saw it")[1], ["aadhaar"])
        # a Luhn-valid id that no payment network issues (a storage generation), a phone number with its country
        # code, and digits joined to letters pass
        self.assertTrue(identifiers.luhn_valid("1758624751090381"))
        for q in ("generation 1758624751090381", "Call +91 98765 43210", f"INV{a}", f"{a}A"):
            self.assertEqual(desk_rules.mask(q), (q, []), q)
        # a date range, an ISO range, a phone number with its country code typed as digits, a list of figures and
        # mixed separators are not one number, whatever their digits add up to
        for q in ("Leave from 31.08.2024 - 01.07.2025, is it paid?", "Between 2025-03-31 / 2025-06-07 what changed?",
                  "Leave from 26/04/2024 - 22/05/2025", "Call 91 93487 17536", "Payments: 68846 / 74258 / 61887",
                  "4111-1111 1111-1111", f"{a[:6]} {a[6:]}"):
            self.assertEqual(desk_rules.mask(q), (q, []), q)
        # format characters a paste carries do not split a number
        for shown in (f"{a[:4]}\u200b{a[4:8]}\u200b{a[8:]}", f"{a[:6]}\u00ad{a[6:]}"):
            self.assertEqual(desk_rules.mask(f"Aadhaar {shown}."), ("Aadhaar [Aadhaar].", ["aadhaar"]), shown)
        # a masked question is never longer than the one it replaces
        self.assertLessEqual(len(desk_rules.MASK_TEXT["aadhaar"]), 12)
        self.assertLessEqual(len(desk_rules.MASK_TEXT["card"]), 13)
        q = f"Aadhaar {a} and card 4111111111111111 " + "x" * 3950
        self.assertLessEqual(len(desk_rules.mask(q)[0]), len(q))


# ------------------------------------------------------------------ the door, in plain asyncio
class _HTTPError(Exception):
    def __init__(self, status_code, detail, headers=None):
        super().__init__(detail)
        self.status_code, self.detail, self.headers = status_code, detail, headers


class _App:
    """The downstream app: records what reached it and answers 200 with the body it was given."""

    def __init__(self):
        self.calls = []

    async def __call__(self, scope, receive, send):
        msg = await receive()
        self.calls.append((scope, msg["body"]))
        await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"application/json")]})
        await send({"type": "http.response.body", "body": b'{"handler": true}'})


def _run(door, path, body: bytes, method="POST", headers=None, chunks=None):
    scope = {"type": "http", "method": method, "path": path,
             "headers": [(b"content-type", b"application/json")] + list(headers or [])}
    parts = chunks or [body]
    queue = [{"type": "http.request", "body": p, "more_body": i < len(parts) - 1} for i, p in enumerate(parts)]
    sent = []

    async def receive():
        return queue.pop(0) if queue else {"type": "http.disconnect"}

    async def send(msg):
        sent.append(msg)

    asyncio.run(door(scope, receive, send))
    start = next(m for m in sent if m["type"] == "http.response.start")
    out = b"".join(m.get("body", b"") for m in sent if m["type"] == "http.response.body")
    return start["status"], dict(start["headers"]), out


class DoorTests(unittest.TestCase):
    POSH = "My manager keeps commenting on my appearance and touched me at the offsite."
    HUMAN = "I want to talk to someone in HR."

    def setUp(self):
        self.app = _App()
        self.flags = {"acme": {"desk_gate": "on"}, "zeta": {}}
        self.settings_reads = []
        self.verified = []

        def settings(t):
            self.settings_reads.append(t)
            return self.flags.get(t, {})

        def verify(request):
            self.verified.append(request.headers.get("X-Goog-IAP-JWT-Assertion"))
            email = request.headers.get("x-user-email")
            if not email:
                raise _HTTPError(401, "missing identity headers")
            return {"email": email, "via": "dev"}

        def member(email, tenant):
            if email != "you@example.com":
                raise _HTTPError(403, "not a member of this tenant")

        self.door = desk_door.DeskDoor(self.app, settings=settings, verify=verify, member=member)
        self.me = [(b"x-user-email", b"you@example.com"), (b"x-goog-iap-jwt-assertion", b"tok")]

    def body(self, q, tenant="acme", **extra):
        return json.dumps({"query": q, "tenant_id": tenant, **extra}).encode()

    def logs(self, fn):
        records = []
        handler = logging.Handler()
        handler.emit = lambda r: records.append(json.loads(r.getMessage()))
        lg = logging.getLogger("documind-api")
        lg.addHandler(handler)
        old, disabled = lg.level, logging.root.manager.disable
        lg.setLevel(logging.INFO)
        logging.disable(logging.NOTSET)         # another suite in the same run may have switched logging off
        try:
            result = fn()
        finally:
            lg.removeHandler(handler)
            lg.setLevel(old)
            logging.disable(disabled)
        return result, records

    def test_no_hit_replays_the_bytes_and_reads_no_setting(self):
        raw = b'{"query":  "What is the notice period during probation?", "tenant_id": "acme", "top_k": 5}'
        status, _, out = _run(self.door, "/v1/query", raw, headers=self.me)
        self.assertEqual((status, out), (200, b'{"handler": true}'))
        self.assertEqual(self.app.calls[0][1], raw)
        self.assertEqual(self.settings_reads, [])
        self.assertEqual(self.verified, [])

    def test_flag_off_replays_a_hit_byte_for_byte(self):
        raw = self.body(self.POSH, tenant="zeta")
        status, _, out = _run(self.door, "/v1/stream", raw, headers=self.me)
        self.assertEqual((status, out), (200, b'{"handler": true}'))
        self.assertEqual(self.app.calls[0][1], raw)
        self.assertEqual(self.app.calls[0][0]["headers"], [(b"content-type", b"application/json")] + self.me)

    def test_a_hit_on_query_gets_the_template_and_the_handler_never_runs(self):
        (status, headers, out), rows = self.logs(lambda: _run(self.door, "/v1/query", self.body(self.POSH), headers=self.me))
        self.assertEqual(status, 200)
        self.assertEqual(self.app.calls, [])
        self.assertEqual(headers[b"content-type"], b"application/json")
        ans = json.loads(out)
        self.assertEqual(ans["answer"], desk_law.template("posh"))
        self.assertEqual((ans["answerable"], ans["citations"], ans["model"], ans["backend"], ans["cost_usd"],
                          ans["tokens_in"], ans["tokens_out"], ans["cache_hit"]),
                         (False, [], "none", "desk_gate", 0.0, 0, 0, "none"))
        self.assertEqual(rows, [{"event": "desk_gate", "surface": "query", "tenant": "acme", "user": None,
                                 "class": "sensitive", "rules_version": desk_rules.RULES_VERSION}])

    def test_the_query_template_is_a_rag_response(self):
        try:
            schemas = _load("schemas_for_door", ROOT / "services" / "rag-api" / "schemas.py")
        except ImportError as e:
            if REQUIRE_LIBS:
                raise
            self.skipTest(f"pydantic not installed: {e}")
        _, _, out = _run(self.door, "/v1/query", self.body(self.HUMAN), headers=self.me)
        ans = schemas.RAGResponse.model_validate(json.loads(out))
        self.assertEqual((ans.model, ans.backend, ans.cost_usd, ans.answerable), ("none", "desk_gate", 0.0, False))

    def test_a_hit_on_stream_is_one_token_then_done(self):
        (status, headers, out), rows = self.logs(lambda: _run(self.door, "/v1/stream", self.body(self.HUMAN), headers=self.me))
        self.assertEqual(status, 200)
        self.assertEqual(self.app.calls, [])
        self.assertTrue(headers[b"content-type"].startswith(b"text/event-stream"))
        events = [e for e in out.decode().split("\n\n") if e]
        self.assertEqual([e.split("\n")[0] for e in events], ["event: token", "event: done"])
        self.assertEqual(json.loads(events[0].split("data: ", 1)[1]), {"t": desk_law.template("human_requested")})
        done = json.loads(events[1].split("data: ", 1)[1])
        self.assertEqual((done["model"], done["backend"], done["cost_usd"], done["tokens_in"], done["tokens_out"]),
                         ("none", "desk_gate", 0.0, 0, 0))
        # human_requested is not sensitive: the row names the person and the class
        self.assertEqual(rows[0]["user"], "you@example.com")
        self.assertEqual((rows[0]["class"], rows[0]["surface"]), ("human_requested", "stream"))

    def test_a_hit_on_passages_returns_no_passages(self):
        status, _, out = _run(self.door, "/v1/passages", self.body(self.POSH), headers=self.me)
        self.assertEqual(status, 200)
        self.assertEqual(self.app.calls, [])
        ans = json.loads(out)
        self.assertEqual((ans["passages"], ans["answerable"], ans["usage"]["cost_usd"], ans["usage"]["backend"]),
                         ([], False, 0.0, "desk_gate"))

    def test_every_sensitive_class_logs_no_user(self):
        for cls in ("posh", "grievance", "privacy_request", "exit_dues"):
            q = EXAMPLES[cls][0][1]
            _, rows = self.logs(lambda: _run(self.door, "/v1/query", self.body(q), headers=self.me))
            self.assertEqual(rows[-1]["class"], "sensitive" if cls in desk_rules.SENSITIVE else cls)
            self.assertEqual(rows[-1]["user"], None if cls in desk_rules.SENSITIVE else "you@example.com")
            self.assertNotIn(q, json.dumps(rows))

    def test_unverified_is_401_and_outsider_is_403_before_any_flag(self):
        status, _, out = _run(self.door, "/v1/query", self.body(self.POSH))
        self.assertEqual((status, json.loads(out)), (401, {"detail": "missing identity headers"}))
        # FastAPI's own JSONResponse bytes (no spaces, UTF-8 as it is), so a refusal does not tell a hit from a miss
        self.assertEqual(out, b'{"detail":"missing identity headers"}')
        self.assertEqual(desk_door._dumps({"detail": "नहीं"}), json.dumps({"detail": "नहीं"}, ensure_ascii=False, separators=(",", ":")).encode())
        status, _, out = _run(self.door, "/v1/stream", self.body(self.POSH), headers=[(b"x-user-email", b"outsider@example.com")])
        self.assertEqual((status, out), (403, b'{"detail":"not a member of this tenant"}'))
        self.assertEqual(self.app.calls, [])
        self.assertEqual(self.settings_reads, [])

    def test_headers_reach_verify_case_insensitively(self):
        _run(self.door, "/v1/query", self.body(self.POSH), headers=self.me)
        self.assertEqual(self.verified, ["tok"])

    def test_an_error_without_a_status_is_the_servers(self):
        self.door.verify = lambda request: (_ for _ in ()).throw(RuntimeError("firestore down"))
        with self.assertRaises(RuntimeError):
            _run(self.door, "/v1/query", self.body(self.POSH), headers=self.me)

    def test_over_64_kib_is_413(self):
        big = self.body("x" * (64 * 1024))
        status, _, out = _run(self.door, "/v1/query", big, headers=self.me)
        self.assertEqual(status, 413)
        status, _, _ = _run(self.door, "/v1/query", b"", headers=[(b"content-length", b"70000")])
        self.assertEqual(status, 413)
        status, _, _ = _run(self.door, "/v1/query", b"", chunks=[b"{" * 40000, b" " * 40000])
        self.assertEqual(status, 413)
        self.assertEqual(self.app.calls, [])
        # exactly 64 KiB is read and replayed
        edge = b" " * (64 * 1024)
        status, _, _ = _run(self.door, "/v1/query", edge)
        self.assertEqual((status, self.app.calls[-1][1]), (200, edge))

    def test_invalid_json_and_odd_bodies_are_replayed_unchanged(self):
        for raw in (b"{not json", b"\xff\xfe", b"[1, 2]", b'{"query": 42, "tenant_id": "acme"}', b""):
            self.app.calls.clear()
            status, _, _ = _run(self.door, "/v1/query", raw, headers=self.me)
            self.assertEqual((status, self.app.calls[0][1]), (200, raw))
        # a hit with no tenant goes to the handler, whose own 422 answers it
        raw = json.dumps({"query": self.POSH}).encode()
        _run(self.door, "/v1/query", raw, headers=self.me)
        self.assertEqual(self.app.calls[-1][1], raw)

    def test_chunked_bodies_are_reassembled(self):
        raw = self.body("What is the notice period during probation?")
        status, _, _ = _run(self.door, "/v1/query", b"", chunks=[raw[:7], raw[7:20], raw[20:]])
        self.assertEqual((status, self.app.calls[0][1]), (200, raw))

    def test_masking_only_when_the_flag_is_on(self):
        a = synthetic_aadhaar()
        q = f"My Aadhaar {a} was rejected on the form - which ID proofs does the policy accept?"
        raw = self.body(q, top_k=3)
        status, _, _ = _run(self.door, "/v1/query", raw, headers=self.me + [(b"content-length", str(len(raw)).encode())])
        scope, sent = self.app.calls[-1]
        got = json.loads(sent)
        self.assertEqual(got["query"], "My Aadhaar [Aadhaar] was rejected on the form - which ID proofs does the policy accept?")
        self.assertEqual((got["tenant_id"], got["top_k"]), ("acme", 3))
        self.assertNotIn(a.encode(), sent)
        lengths = [v for k, v in scope["headers"] if k == b"content-length"]
        self.assertEqual(lengths, [str(len(sent)).encode()])
        # zeta's flag is off: the same question goes through as it was sent
        raw = self.body(q, tenant="zeta")
        _run(self.door, "/v1/query", raw, headers=self.me)
        self.assertEqual(self.app.calls[-1][1], raw)
        # no identifier: no setting is read at all
        self.settings_reads.clear()
        _run(self.door, "/v1/query", self.body("My Aadhaar is 2234 5678 9012"), headers=self.me)
        self.assertEqual(self.settings_reads, [])

    def test_masking_verifies_the_caller_before_any_setting_is_read(self):
        a = synthetic_aadhaar()
        raw = self.body(f"My Aadhaar {a} was rejected - which ID proofs does the policy accept?", tenant="random-tenant-id")
        # no identity: the body goes to the handler unchanged, whose own 401 answers it; no setting is read
        status, _, _ = _run(self.door, "/v1/query", raw)
        self.assertEqual((status, self.app.calls[-1][1], self.settings_reads), (200, raw, []))
        # a caller who is not on the roster: the same
        _run(self.door, "/v1/query", raw, headers=[(b"x-user-email", b"outsider@example.com")])
        self.assertEqual((self.app.calls[-1][1], self.settings_reads), (raw, []))
        # a member: the flag is read, then the numbers are masked
        raw = self.body(f"My Aadhaar {a} was rejected - which ID proofs does the policy accept?")
        _run(self.door, "/v1/query", raw, headers=self.me)
        self.assertEqual(self.settings_reads, ["acme"])
        self.assertNotIn(a.encode(), self.app.calls[-1][1])

    def test_a_query_over_the_handlers_cap_goes_to_the_handler_unread(self):
        raw = self.body(self.POSH + " " + "x" * desk_door.QUERY_MAX)
        status, _, _ = _run(self.door, "/v1/query", raw, headers=self.me)
        self.assertEqual((status, self.app.calls[-1][1], self.verified, self.settings_reads), (200, raw, [], []))

    def test_a_masked_query_near_the_cap_stays_under_it(self):
        a = synthetic_aadhaar()
        head = f"Aadhaar {a[:4]} {a[4:8]} {a[8:]} and card 4111 1111 1111 1111 - which ID proofs does the policy accept? "
        q = head + "x" * (desk_door.QUERY_MAX - len(head))
        self.assertEqual(len(q), desk_door.QUERY_MAX)
        _run(self.door, "/v1/query", self.body(q), headers=self.me)
        sent = json.loads(self.app.calls[-1][1])["query"]
        self.assertNotIn(a, sent)
        self.assertLessEqual(len(sent), desk_door.QUERY_MAX)

    def test_a_failed_settings_read_is_off(self):
        self.door.settings = lambda t: (_ for _ in ()).throw(RuntimeError("firestore down"))
        raw = self.body(self.POSH)
        status, _, out = _run(self.door, "/v1/query", raw, headers=self.me)
        self.assertEqual((status, self.app.calls[-1][1]), (200, raw))

    def test_other_routes_and_methods_pass_through(self):
        raw = self.body(self.POSH)
        for method, path in (("GET", "/v1/query"), ("POST", "/v1/media/generate"), ("POST", "/health")):
            self.app.calls.clear()
            _run(self.door, path, raw, method=method, headers=self.me)
            self.assertEqual(self.app.calls[0][1], raw)

        async def lifespan():
            seen = []

            async def app(scope, receive, send):
                seen.append(scope["type"])
            await desk_door.DeskDoor(app, None, None, None)({"type": "lifespan"}, None, None)
            return seen
        self.assertEqual(asyncio.run(lifespan()), ["lifespan"])

    def test_flag_values(self):
        self.assertTrue(desk_door.flag_on({"desk_gate": "on"}))
        self.assertTrue(desk_door.flag_on({"desk_gate": " ON "}))
        self.assertTrue(desk_door.flag_on({"desk_gate": True}))
        for doc in ({}, None, {"desk_gate": "off"}, {"desk_gate": "shadow"}, {"desk_gate": 1}):
            self.assertFalse(desk_door.flag_on(doc), doc)

    def test_install_and_main_py(self):
        added = []

        class _FakeApp:
            def add_middleware(self, cls, **kw):
                added.append((cls, kw))
        desk_door.install(_FakeApp(), settings="s", verify="v", member="m")
        self.assertEqual(added, [(desk_door.DeskDoor, {"settings": "s", "verify": "v", "member": "m"})])
        src = (ROOT / "services" / "rag-api" / "main.py").read_text(encoding="utf-8")
        cors = src.index("app.add_middleware(CORSMiddleware")
        line = "install_desk_door(app, settings=lambda t: tenant_settings(t), verify=verify_iap, member=enforce_membership)"
        self.assertEqual(src.count(line), 1)
        self.assertLess(src.index(line), cors, "the door is added before CORS, so CORS wraps its replies too")
        self.assertIn("from auth import verify_iap, enforce_membership", src)
        self.assertNotRegex((ROOT / "services" / "rag-api" / "desk_door.py").read_text(encoding="utf-8"),
                            r"(?m)^\s*(?:from|import)\s+(?:fastapi|starlette)|iap\.identity\(")


# ------------------------------------------------------------------ make desk
class _Doc:
    def __init__(self, store, key):
        self.store, self.key = store, key

    def set(self, data, merge=False):
        self.store.writes.append((self.key, data, merge))
        cur = self.store.docs.setdefault(self.key, {}) if merge else {}
        cur.update(data)
        self.store.docs[self.key] = cur

    def get(self):
        doc = self.store.docs.get(self.key)
        return type("Snap", (), {"exists": doc is not None, "to_dict": lambda s: dict(doc or {})})()


class _Db:
    def __init__(self, docs=None):
        self.docs, self.writes = dict(docs or {}), []

    def collection(self, name):
        db = self
        return type("Col", (), {"document": lambda s, d: _Doc(db, f"{name}/{d}")})()


class DeskOpsTests(unittest.TestCase):
    def test_set_switch_merges_and_refuses_typos(self):
        db = _Db({"tenant_settings/acme": {"data_region": "in", "retrieval_backend": "vector"}})
        desk_ops.set_switch(db, "acme", "desk_gate", "ON", "you@example.com", at="T")
        self.assertEqual(db.writes, [("tenant_settings/acme", {"desk_gate": "on", "desk_gate_set_by": "you@example.com",
                                                               "desk_gate_set_at": "T"}, True)])
        self.assertEqual(db.docs["tenant_settings/acme"]["data_region"], "in")
        self.assertEqual(desk_ops.switches(db, "acme"), {"desk_gate": "on"})
        self.assertEqual(desk_ops.switches(db, "zeta"), {"desk_gate": "off"})
        with self.assertRaises(ValueError):
            desk_ops.set_switch(db, "acme", "desk_gate", "yes", "you@example.com", at="T")
        # make desk DESK_GATE=ON reaches set_switch as "on"
        a = desk_ops.build_parser().parse_args(["desk", "--tenant", "acme", "--gate", "ON"])
        self.assertEqual(a.gate, "on")
        self.assertEqual(len(db.writes), 1)

    def test_the_subcommand_and_the_target(self):
        a = desk_ops.build_parser().parse_args(["--project", "documind-ai-YOUR-ID", "desk", "--tenant", "acme", "--gate", "off"])
        self.assertEqual((a.cmd, a.tenant, a.gate, a.fn), ("desk", "acme", "off", desk_ops.cmd_desk))
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
            desk_ops.build_parser().parse_args(["desk", "--gate", "maybe"])
        mk = (ROOT / "mk" / "agents.mk").read_text(encoding="utf-8")
        self.assertIn("\ndesk: guard-project\n", mk)
        self.assertIn("commands/desk_ops.py --project $(PROJECT) desk --tenant $(TENANT) $(if $(DESK_GATE),--gate $(DESK_GATE),)", mk)
        makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
        phony = makefile[makefile.index(".PHONY:"):makefile.index("# ---------- the module files")].replace("\\", " ").split()
        self.assertIn("desk", phony)
        self.assertIn("`desk`", (ROOT / "mk" / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
