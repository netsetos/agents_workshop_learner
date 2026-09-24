"""Lesson 16.1 / s4: The clip built, the transcript withdrawn, the video heard

Summary and purpose:
Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call: Last, read the video's rows from acme's index, and hold them against the ground truth:

HTML instruction: bash — run in the operator shell, in the kit (reads only)
Category: required. Read the matching README checkpoint before Run.
Prerequisites: demo_04_03_definition
Expected observation: 5 segments of townhall_2026_q1.mp4 in acme's index, against the ground truth's 5 turns:
  segment t0-22     00:00-00:22   22 s  over Meera 00:00
      Meera, the CEO, opens the FY2026 town hall over a first slide saying the video is synthetic, welcoming s...
  segment t22-58    00:22-00:58   36 s  over Arjun 00:22
      Arjun, the CFO, walks through the revenue table on slide two: India grew from 412 to 508 crore, up 23.3 ...
  segment t58-70    00:58-01:10   12 s  over Meera 00:58
      Meera says headcount closed at 4,180, up from 3,742, and attrition came down to 11.4 per cent from 14.9 ...
  segment t70-93    01:10-01:33   23 s  over Arjun 01:10
      Arjun says capital expenditure was 78 crore for the year: 31 crore went into the Hyderabad plant expansi...
  segment t93-105   01:33-01:45   12 s  over Meera 01:33
      Meera thanks Arjun and says questions are open on the portal unti

Evidence: the active lesson session records this attempt and command output.
A completed process is not proof that every sample value matches your lane.
Source: https://github.com/netsetos/agents_workshop/blob/main/lessons/16-multimodal/16.1-video-clip/Netsetos_GCP_Capstone_16.1_Video_Clip_WIX.html#L599

"""
from workshop_helpers.session import DemoSession

# Change only for a deliberate replay after inspecting this step's effects.
REPEAT = False


def demonstrate(session):
    """Run Definition at this checkpoint.

    Then the video goes up as a new document. make reindex copies it into acme's uploads and waits for the worker's line. The worker's media branch describes it in one Gemini call: Last, read the video's rows from acme's index, and hold them against the ground truth:

    Args: session is the active lesson run, with validated settings and saved prerequisites.
    Operations: bash — run in the operator shell, in the kit (reads only).
    Returns: None; observations are printed or saved by the lesson code.
    Failures propagate to the session; inspect its failed attempt before continuing.
    """
    import json, os
    from google.cloud import firestore
    from google.cloud.firestore_v1.base_query import FieldFilter
    P = os.environ["PROJECT"]
    URI = f"gs://{P}-uploads/acme/townhall_2026_q1.mp4"
    db = firestore.Client(project=P)
    rows = [d.to_dict() for d in db.collection("chunks").where(filter=FieldFilter("tenant_id", "==", "acme"))
            .where(filter=FieldFilter("source_uri", "==", URI)).where(filter=FieldFilter("current", "==", True)).stream()]
    truth = json.load(open("evals/corpus/acme/townhall_2026_q1.segments.json", encoding="utf-8"))["segments"]
    mmss = lambda s: f"{int(s) // 60:02d}:{int(s) % 60:02d}"
    print(f"{len(rows)} segments of townhall_2026_q1.mp4 in acme's index, against the ground truth's {len(truth)} turns:")
    for r in sorted(rows, key=lambda r: r["start"]):
        heard = [f"{t['speaker']} {mmss(t['start'])}" for t in truth if min(t["end"], r["end"]) - max(t["start"], r["start"]) > 1]   # a second of the turn or more
        print(f"  {r['kind']} {r['locator']:9} {mmss(r['start'])}-{mmss(r['end'])} {r['end'] - r['start']:4.0f} s  over {', '.join(heard) or 'nobody'}")
        print(f"      {r['text'][:104]}...")
    longest = max(r["end"] - r["start"] for r in rows)
    bad = [r["locator"] for r in rows if not 0 <= r["start"] < r["end"]]
    video_end = truth[-1]["end"]
    print(f"checks: longest {longest:.0f} s (the prompt asks for at most 60) -> {'PASS' if longest <= 60 else 'FAIL'}; "
          f"start before end in every row -> {'PASS' if not bad else 'FAIL ' + ', '.join(bad)}; "
          f"last end {mmss(max(r['end'] for r in rows))} against the speech's end {mmss(video_end)}")
    said = next(t for t in truth if "5.2 per cent" in t["text"])
    hit = [r["locator"] for r in rows if r["start"] <= said["end"] and r["end"] >= said["start"] and "5.2 per cent" in r["text"]]
    print(f"the EMEA line: {said['speaker']} says '5.2 per cent' in the turn at {mmss(said['start'])}-{mmss(said['end'])}; "
          f"the segment that quotes it: {', '.join(hit) or 'none'}")


def main():
    """Resume this lesson and execute only this checkpoint in the IDE interpreter."""
    with DemoSession(__file__, live=True, repeat=REPEAT) as session:
        demonstrate(session)


if __name__ == "__main__":
    main()
