#!/usr/bin/env python3
"""Run the eval questions headless through Claude Code (/dgx) and score them.

Scores: required page citations present; undocumented questions correctly refused; plus cost,
tokens, turns and time per question. Full answers go to evals/runs/<stamp>.{json,md} for review.

Usage:
  python evals/run_evals.py                  # all questions, 2 in parallel
  python evals/run_evals.py --only menu-split-point,neg-vst-plugins
  python evals/run_evals.py --baseline       # also write evals/BASELINE.md (commit it)
  python evals/run_evals.py --model sonnet   # compare models
"""
import argparse
import concurrent.futures
import glob
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
RUNS = ROOT / "evals" / "runs"
CITE_RE = re.compile(r"\b(OM|RM|DL) p\.\s?(\d+)(?:\s*[–-]\s*(\d+))?")
FIG_RE = re.compile(r"\bFIG (((?:OM|RM)-\d{3})-f\d+)")
NOT_DOC = "not documented in the dgx-670 manuals"
# Same capabilities as a normal session (reads, subagents, cache writes) minus git: cache files created
# during a run are committed once afterwards instead of by parallel jobs racing on the git index.
ALLOWED = ["Read", "Grep", "Glob", "Skill", "Agent", "Task", "Write(kb/**)", "Edit(kb/**)",
           "Bash(python scripts/register.py *)", "Bash(python3 scripts/register.py *)",
           "Bash(python scripts/render_page.py *)", "Bash(python3 scripts/render_page.py *)"]
DENIED = ["Bash(git *)"]


def find_claude():
    exe = shutil.which("claude")
    if exe:
        return exe
    home = Path.home()
    hits = sorted(glob.glob(str(home / ".vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude*")))
    if hits:
        return hits[-1]
    sys.exit("claude CLI not found (not on PATH and no VS Code extension binary)")


def cited_pages(text):
    pages = set()
    for doc, a, b in CITE_RE.findall(text):
        for n in range(int(a), int(b or a) + 1):
            pages.add(f"{doc}-{n:03d}")
    for fig, page in FIG_RE.findall(text):
        pages |= {fig, page}  # figure questions require the figure ID itself (proves it was described)
    return pages


def parse_stream(stdout):
    """stream-json events -> (final result event, compact tool-call trace incl. subagents)."""
    result, trace = {}, []
    for line in stdout.splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") == "result":
            result = ev
        elif ev.get("type") == "assistant":
            who = "sub" if ev.get("parent_tool_use_id") else "main"
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    arg = json.dumps(block.get("input", {}), ensure_ascii=False)
                    trace.append(f"{who}: {block['name']} {arg[:140]}")
    return result, trace


def run_one(claude, q, model):
    cmd = [claude, "-p", f"/dgx {q['question']}", "--output-format", "stream-json", "--verbose",
           "--allowedTools", *ALLOWED, "--disallowedTools", *DENIED]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    try:
        proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", timeout=900)
        data, trace = parse_stream(proc.stdout or "")
        if not data:
            data = {"result": f"RUN ERROR: {proc.stderr[-500:]}", "is_error": True}
    except subprocess.TimeoutExpired as e:
        data, trace = {"result": f"RUN ERROR: {e}", "is_error": True}, []
    answer = data.get("result") or ""
    usage = data.get("usage") or {}
    cited = cited_pages(answer)
    hits = [any(p in cited for p in group) for group in q.get("expect_pages", [])]
    says_nd = NOT_DOC in answer.lower()
    if q.get("expect_not_documented"):
        checks = hits + [says_nd]
    else:
        checks = hits + [not says_nd]
    return {
        **q,
        "answer": answer,
        "cited": sorted(cited),
        "hits": hits,
        "passed": all(checks) and not data.get("is_error"),
        "score": sum(checks) / len(checks),
        "cost_usd": data.get("total_cost_usd", 0.0),
        "tokens_in": usage.get("input_tokens", 0) + usage.get("cache_read_input_tokens", 0)
                     + usage.get("cache_creation_input_tokens", 0),
        "tokens_out": usage.get("output_tokens", 0),
        "turns": data.get("num_turns", 0),
        "seconds": round(time.time() - t0),
        "tool_calls": len(trace),
        "trace": trace,
    }


def report(results, model):
    n = len(results)
    passed = sum(r["passed"] for r in results)
    cost = sum(r["cost_usd"] for r in results)
    lines = [f"# Eval run {datetime.now():%Y-%m-%d %H:%M} (model: {model or 'default'})", "",
             f"**Passed {passed}/{n}** · mean score {sum(r['score'] for r in results) / n:.2f} · "
             f"total ${cost:.2f} · ${cost / n:.3f}/question · "
             f"avg {sum(r['tokens_in'] for r in results) // n:,} in / {sum(r['tokens_out'] for r in results) // n:,} out tokens", "",
             "| Question | Category | Pass | Expected cited | Cost | Tokens in/out | Turns | Tool calls | Secs |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        exp = " ".join("✓" if h else "✗" for h in r["hits"]) or ("ND ✓" if r["passed"] else "ND ✗")
        lines.append(f"| {r['id']} | {r['category']} | {'✅' if r['passed'] else '❌'} | {exp} | ${r['cost_usd']:.3f} | "
                     f"{r['tokens_in']:,}/{r['tokens_out']:,} | {r['turns']} | {r['tool_calls']} | {r['seconds']} |")
    lines += ["", "## Answers (review against `notes`)", ""]
    for r in results:
        lines += [f"### {r['id']} — {'PASS' if r['passed'] else 'FAIL'}", f"**Q:** {r['question']}", "",
                  f"**Expected:** {r['notes']}", "", f"**Cited:** {', '.join(r['cited']) or '—'}", "",
                  r["answer"].strip(), "", "<details><summary>Tool trace</summary>", "",
                  *[f"- `{t}`" for t in r["trace"]], "", "</details>", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="comma-separated question ids")
    ap.add_argument("--jobs", type=int, default=2)
    ap.add_argument("--model")
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--rebaseline", action="store_true",
                    help="no run: rebuild BASELINE.md from the newest result per question across evals/runs/")
    args = ap.parse_args()
    if args.rebaseline:
        latest = {}
        for f in sorted(RUNS.glob("*.json")):  # timestamped names sort chronologically
            for r in json.loads(f.read_text(encoding="utf-8")):
                latest[r["id"]] = {"tool_calls": 0, "trace": [], **r}
        order = [q["id"] for q in json.loads((ROOT / "evals" / "questions.json").read_text(encoding="utf-8"))["questions"]]
        md = report([latest[i] for i in order if i in latest], "newest result per question")
        (ROOT / "evals" / "BASELINE.md").write_text(md, encoding="utf-8")
        print(md.split("\n## Answers")[0])
        return
    questions = json.loads((ROOT / "evals" / "questions.json").read_text(encoding="utf-8"))["questions"]
    if args.only:
        wanted = set(args.only.split(","))
        questions = [q for q in questions if q["id"] in wanted]
    claude = find_claude()
    print(f"Running {len(questions)} questions with {claude} (jobs={args.jobs})")
    with concurrent.futures.ThreadPoolExecutor(args.jobs) as pool:
        futures = {pool.submit(run_one, claude, q, args.model): q["id"] for q in questions}
        results = {}
        for f in concurrent.futures.as_completed(futures):
            r = f.result()
            results[r["id"]] = r
            print(f"  {'PASS' if r['passed'] else 'FAIL'}  {r['id']:32} ${r['cost_usd']:.3f}  {r['seconds']}s")
    results = [results[q["id"]] for q in questions]
    RUNS.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    md = report(results, args.model)
    (RUNS / f"{stamp}.json").write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    (RUNS / f"{stamp}.md").write_text(md, encoding="utf-8")
    if args.baseline:
        (ROOT / "evals" / "BASELINE.md").write_text(md, encoding="utf-8")
    print(md.split("\n## Answers")[0])
    print(f"Full report: evals/runs/{stamp}.md")


if __name__ == "__main__":
    main()
