#!/usr/bin/env python3
"""Register a newly written cache entry: validate it, update its index row, and (for figures)
update the page file's markers + frontmatter. Stdlib only.

Usage:
  python scripts/register.py figure   RM-005     # after writing kb/figures/RM-005.md
  python scripts/register.py faq      split-point-change   # after writing faq/split-point-change.md
  python scripts/register.py external filter-envelope      # after writing kb/external/filter-envelope.md
  python scripts/register.py lab      voice-file-format      # after writing kb/lab/voice-file-format.md
"""
import re
import sys

from kbcommon import KB, ROOT, SUMMARY_RE, cached_figure_titles, figure_file, mark_figures, page_path

sys.stdout.reconfigure(encoding="utf-8")
ROW_KEY_RE = re.compile(r"\[([^\]]+)\]\(\1\.md\)")  # every index row links its own file: [key](key.md)


def field(text, name):
    m = re.search(rf"^{name}:\s*(.+?)\s*$", text, re.M)
    return m.group(1) if m else None


def upsert_row(index_file, key, row):
    """Replace/insert the row linking `[key](key.md)`; keep rows sorted by key."""
    lines = index_file.read_text(encoding="utf-8").rstrip("\n").split("\n")
    sep = next(i for i, l in enumerate(lines) if l.startswith("|---"))
    head, rows = lines[:sep + 1], [l for l in lines[sep + 1:] if l.startswith("|")]
    keyed = {}
    for r in rows:
        m = ROW_KEY_RE.search(r)
        keyed[m.group(1) if m else r] = r
    keyed[key] = row
    index_file.write_text("\n".join(head + [keyed[k] for k in sorted(keyed)]) + "\n", encoding="utf-8", newline="\n")


def die(msg):
    print(f"ERROR: {msg}")
    sys.exit(1)


def register_figure(pid):
    f = figure_file(pid)
    pf = page_path(pid)
    if not f.exists():
        die(f"{f} does not exist")
    if not pf.exists():
        die(f"no page file {pf}")
    body = f.read_text(encoding="utf-8")
    page = pf.read_text(encoding="utf-8")
    expected = [x.split("-")[-1] for x in re.findall(r"[A-Z]{2}-\d{3}-f\d+", field(page, "figures") or "")]
    titles = cached_figure_titles(pid)
    missing = [x for x in expected if x not in titles]
    if missing:
        die(f"{f.name} lacks sections for {missing}; need '## fN — <title>' for every figure in the page frontmatter")
    summary = SUMMARY_RE.search(body)
    if not summary:
        die(f"{f.name} lacks a 'summary:' line")
    page = mark_figures(page, pid, titles)
    page = re.sub(r"^figure_cache: .*$", "figure_cache: done", page, count=1, flags=re.M)
    pf.write_text(page, encoding="utf-8", newline="\n")
    upsert_row(KB / "figures" / "INDEX.md", pid,
               f"| [{pid}]({pid}.md) | {', '.join(sorted(titles, key=lambda s: int(s[1:])))} | "
               f"{summary.group(1).replace('|', '/')} |")
    print(f"ok: {pid} registered ({len(titles)} figure sections); page markers updated")


def register_faq(slug):
    f = ROOT / "faq" / f"{slug}.md"
    if not f.exists():
        die(f"{f} does not exist")
    body = f.read_text(encoding="utf-8")
    q, cites = field(body, "question"), field(body, "citations")
    if not (q and cites):
        die(f"{f.name} needs 'question:' and 'citations:' lines")
    if not re.search(r"\[(OM|RM|DL) p\.\d+", body):
        die(f"{f.name} has no [OM p.N]/[RM p.N]/[DL p.N] citation in its body")
    upsert_row(ROOT / "faq" / "INDEX.md", slug,
               f"| {q.replace('|', '/')} | [{slug}]({slug}.md) | {cites.replace('|', '/')} |")
    print(f"ok: faq/{slug} registered")


EXTERNAL_STATUSES = ("found", "partial", "nothing-found")
EXTERNAL_FIELDS = ("topic", "status", "researched", "manual_gap", "queries", "summary")


def external_problems(body):
    """Return what is wrong with an external-research entry (empty list = valid). Shared with check_kb.py."""
    problems = [f"missing '{n}:' line" for n in EXTERNAL_FIELDS if not field(body, n)]
    status = field(body, "status")
    if status and status not in EXTERNAL_STATUSES:
        problems.append(f"status must be one of {EXTERNAL_STATUSES}")
    if field(body, "researched") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", field(body, "researched")):
        problems.append("researched must be YYYY-MM-DD")
    findings = re.findall(r"^\*\*\[E\d+\]\*\*.*$", body, re.M)
    if status in ("found", "partial"):
        if not findings:
            problems.append("status found/partial needs '**[E1]** …' finding lines")
        for line in findings:
            if not re.search(r"https?://", line):
                problems.append(f"finding without a URL: {line[:60]}")
    if not re.search(r"^## Manual baseline", body, re.M):
        problems.append("missing '## Manual baseline' section (what the manuals do/don't say, cited)")
    return problems


def register_external(slug):
    f = KB / "external" / f"{slug}.md"
    if not f.exists():
        die(f"{f} does not exist")
    body = f.read_text(encoding="utf-8")
    problems = external_problems(body)
    if problems:
        die(f"{f.name}: " + "; ".join(problems))
    cell = lambda n: field(body, n).replace("|", "/")
    upsert_row(KB / "external" / "INDEX.md", slug,
               f"| {cell('topic')} | [{slug}]({slug}.md) | {cell('status')} | {cell('researched')} | {cell('summary')} |")
    print(f"ok: external/{slug} registered ({field(body, 'status')})")


LAB_STATUSES = ("confirmed", "partial", "hypothesis")
LAB_FIELDS = ("topic", "status", "tested", "evidence", "summary")
LAB_FINDING_STATUSES = ("confirmed", "likely", "hypothesis", "unknown")


def lab_companions(body):
    """Companion files named on the optional 'files:' line (e.g. a field-map CSV next to the entry)."""
    return [x.strip() for x in (field(body, "files") or "").split(",") if x.strip()]


def lab_problems(body):
    """Return what is wrong with a lab entry (empty list = valid). Shared with check_kb.py."""
    problems = [f"missing '{n}:' line" for n in LAB_FIELDS if not field(body, n)]
    status = field(body, "status")
    if status and status not in LAB_STATUSES:
        problems.append(f"status must be one of {LAB_STATUSES}")
    if field(body, "tested") and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", field(body, "tested")):
        problems.append("tested must be YYYY-MM-DD")
    if not re.search(r"^## Manual baseline", body, re.M):
        problems.append("missing '## Manual baseline' section (what the manuals do/don't say, cited)")
    findings = re.split(r"(?m)^(?=\*\*\[L\d+\]\*\*)", body)[1:]
    if not findings:
        problems.append("needs '**[L1]** …' finding paragraphs")
    for para in findings:
        para = para.split("\n\n")[0]
        if not re.search(r"Status: (%s)" % "|".join(LAB_FINDING_STATUSES), para):
            problems.append(f"finding without 'Status: <{'/'.join(LAB_FINDING_STATUSES)}>': {para[:40]}")
    for name in lab_companions(body):
        if not (KB / "lab" / name).exists():
            problems.append(f"companion file kb/lab/{name} is missing")
    return problems


def register_lab(slug):
    f = KB / "lab" / f"{slug}.md"
    if not f.exists():
        die(f"{f} does not exist")
    body = f.read_text(encoding="utf-8")
    problems = lab_problems(body)
    if problems:
        die(f"{f.name}: " + "; ".join(problems))
    cell = lambda n: field(body, n).replace("|", "/")
    links = " · ".join([f"[{slug}]({slug}.md)"] + [f"[{n}]({n})" for n in lab_companions(body)])
    upsert_row(KB / "lab" / "INDEX.md", slug,
               f"| {cell('topic')} | {links} | {cell('status')} | {cell('tested')} | {cell('summary')} |")
    print(f"ok: lab/{slug} registered ({field(body, 'status')})")


if __name__ == "__main__":
    kinds = {"figure": register_figure, "faq": register_faq, "external": register_external, "lab": register_lab}
    if len(sys.argv) != 3 or sys.argv[1] not in kinds:
        print(__doc__)
        sys.exit(2)
    kinds[sys.argv[1]](sys.argv[2])
