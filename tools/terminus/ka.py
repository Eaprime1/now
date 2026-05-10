#!/usr/bin/env python3
"""
Ka Level Analyzer — now terminus
Ka = accumulated energy/gravity of a concept or document.
Not time-based — weight-based: iterations, connections, attention, feedback.
When Ka reaches threshold → concept routes to next stage automatically.
"""

import subprocess, re, math, datetime, argparse, os, sys, shlex
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

BOLD  = '\033[1m'
DIM   = '\033[2m'
GREEN = '\033[32m'
YELLOW= '\033[33m'
RED   = '\033[31m'
CYAN  = '\033[36m'
RESET = '\033[0m'

NO_COLOR = not sys.stdout.isatty() or os.environ.get('NO_COLOR')
def c(color, text): return text if NO_COLOR else f"{color}{text}{RESET}"

def sh(cmd, cwd=REPO):
    args = cmd if isinstance(cmd, list) else shlex.split(cmd)
    r = subprocess.run(args, capture_output=True, text=True, cwd=cwd)
    return r.stdout.strip()

# ── Ka scoring components (each 0-25 = 100 total) ────────────────────────────

def score_weight(path: Path) -> tuple[float, str]:
    """Physical weight: file size."""
    size = path.stat().st_size
    score = min(math.log1p(size) / math.log(100_000) * 25, 25)
    note = f"{size:,} bytes"
    return round(score, 1), note

def score_iterations(path: Path) -> tuple[float, str]:
    """Iteration count: git commits touching this file."""
    rel = str(path.relative_to(REPO))
    raw = sh(['git', 'log', '--oneline', '--', rel])
    count = len([l for l in raw.splitlines() if l]) if raw else 0
    score = min(count / 20 * 25, 25)
    return round(score, 1), f"{count} commits"

def score_connections(path: Path) -> tuple[float, str]:
    """Connections: internal links + references from other files."""
    try:
        content = path.read_text(errors='ignore')
    except:
        return 0.0, "unreadable"

    # links within this doc
    outbound = len(re.findall(r'\[.+?\]\((?!http).+?\)', content))

    # how many other .md files link to this one
    stem = path.stem
    name = path.name
    inbound_raw = sh(['grep', '-rl', '--include=*.md', '-e', name, '-e', stem, '.'])
    inbound = len([l for l in inbound_raw.splitlines() if l.strip()])

    total = outbound + inbound
    score = min(total / 15 * 25, 25)
    return round(score, 1), f"{outbound} out, {inbound} in"

def score_recency(path: Path) -> tuple[float, str]:
    """Recency: recent attention = high energy."""
    mtime = path.stat().st_mtime
    age_days = (datetime.datetime.now().timestamp() - mtime) / 86400
    if age_days < 1:
        score, note = 25.0, "today"
    elif age_days < 7:
        score, note = 20.0, f"{age_days:.0f}d ago"
    elif age_days < 30:
        score, note = 12.0, f"{age_days:.0f}d ago"
    elif age_days < 90:
        score, note = 5.0, f"{age_days:.0f}d ago"
    else:
        score, note = 0.0, f"{age_days:.0f}d ago"
    return round(score, 1), note

# ── routing thresholds ────────────────────────────────────────────────────────

THRESHOLDS = [
    (80, 'LAUNCH',        GREEN,  'Ready to ship or graduate to next repo'),
    (60, 'REVIEW',        CYAN,   'High energy — queue for review/routing decision'),
    (40, 'BUILDING',      YELLOW, 'Accumulating — keep working'),
    (20, 'RAW',           DIM,    'Low energy — needs attention or concept-queue'),
    ( 0, 'HOLDING',       RED,    'Minimal energy — candidate for concept-queue'),
]

def ka_state(score):
    for threshold, label, color, desc in THRESHOLDS:
        if score >= threshold:
            return label, color, desc
    return 'HOLDING', RED, 'Minimal energy'

# ── analyze ───────────────────────────────────────────────────────────────────

def analyze_file(path: Path) -> dict:
    w_score, w_note = score_weight(path)
    i_score, i_note = score_iterations(path)
    c_score, c_note = score_connections(path)
    r_score, r_note = score_recency(path)
    total = w_score + i_score + c_score + r_score
    state, color, desc = ka_state(total)
    return {
        'path': path,
        'ka': round(total, 1),
        'state': state,
        'state_color': color,
        'components': {
            'weight':      (w_score, w_note),
            'iterations':  (i_score, i_note),
            'connections': (c_score, c_note),
            'recency':     (r_score, r_note),
        }
    }

def collect_docs(repo: Path, include_hidden=False) -> list[Path]:
    paths = []
    for path in repo.rglob('*.md'):
        parts = path.relative_to(repo).parts
        if not include_hidden and any(p.startswith('.') for p in parts):
            continue
        if '_duplicates' in parts or 'legacy' in parts:
            continue
        paths.append(path)
    return paths

# ── display ───────────────────────────────────────────────────────────────────

def bar(val, max_val=100, width=16, full='█', empty='░'):
    filled = round(width * val / max_val) if max_val else 0
    filled = max(0, min(filled, width))
    pct = val / max_val if max_val else 0
    color = GREEN if pct > 0.7 else (YELLOW if pct > 0.4 else RED)
    return c(color, full * filled) + c(DIM, empty * (width - filled))

def print_summary(results: list, verbose=False):
    if not results:
        print("No documents found.")
        return

    max_ka = max(r['ka'] for r in results) or 100
    print()
    print(c(BOLD, f"  Ka Level Report — {len(results)} documents".ljust(60)))
    print(c(DIM, '  ' + '─' * 70))
    print(f"  {'Document':<38} {'Ka':>5}  {'State':<10}  {'W':>4} {'I':>4} {'C':>4} {'R':>4}")
    print(c(DIM, '  ' + '─' * 70))

    for r in results:
        name = str(r['path'].relative_to(REPO))[-38:].ljust(38)
        b = bar(r['ka'], max_val=max_ka, width=12)
        comps = r['components']
        state_str = c(r['state_color'], r['state'].ljust(10))
        w = comps['weight'][0]
        i = comps['iterations'][0]
        co = comps['connections'][0]
        re_ = comps['recency'][0]
        print(f"  {c(DIM, name)}  {b}  {c(CYAN, str(r['ka']).rjust(5))}  "
              f"{state_str}  {w:>4} {i:>4} {co:>4} {re_:>4}")

        if verbose:
            print(f"    {c(DIM, 'weight:')} {comps['weight'][1]}  "
                  f"{c(DIM, 'iter:')} {comps['iterations'][1]}  "
                  f"{c(DIM, 'conn:')} {comps['connections'][1]}  "
                  f"{c(DIM, 'recency:')} {comps['recency'][1]}")

    print(c(DIM, '  ' + '─' * 70))
    print(f"\n  {'Columns: Ka=total, W=weight, I=iterations, C=connections, R=recency (each 0-25)'}")

    # routing recommendations
    print()
    print(c(BOLD, '  Routing Recommendations'))
    print(c(DIM, '  ' + '─' * 50))
    for _, label, color, desc in THRESHOLDS:
        matching = [r for r in results if r['state'] == label]
        if matching:
            print(f"  {c(color, label.ljust(10))} {desc}")
            for r in matching[:3]:
                print(f"    → {r['path'].relative_to(REPO)}")
            if len(matching) > 3:
                print(f"    → ... and {len(matching)-3} more")
    print()

# ── entry ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import json as _json
    parser = argparse.ArgumentParser(description='Ka Level Analyzer — now terminus')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show component breakdown per doc')
    parser.add_argument('--hidden', action='store_true', help='Include hidden (.claude etc) docs')
    parser.add_argument('--threshold', '-t', type=float, default=0,
                        help='Only show docs with Ka >= this value')
    parser.add_argument('--file', '-f', help='Analyze a single specific file')
    parser.add_argument('--json', metavar='PATH', help='Save results as JSON (no terminal output)')
    args = parser.parse_args()

    if args.file:
        p = Path(args.file)
        if not p.is_absolute():
            p = REPO / p
        result = analyze_file(p)
        print()
        print(c(BOLD, f"  Ka Analysis: {p.name}"))
        print(c(DIM, '  ' + '─' * 50))
        print(f"  Total Ka:  {c(CYAN, str(result['ka']))} / 100")
        print(f"  State:     {c(result['state_color'], result['state'])}")
        for comp, (score, note) in result['components'].items():
            b = bar(score, max_val=25, width=12)
            print(f"  {comp.ljust(12)}  {b}  {score:>4}  {c(DIM, note)}")
        print()
    else:
        docs = collect_docs(REPO, include_hidden=args.hidden)
        results = [analyze_file(p) for p in docs]
        if args.threshold:
            results = [r for r in results if r['ka'] >= args.threshold]
        results.sort(key=lambda x: x['ka'], reverse=True)

        if args.json:
            payload = [
                {'path': str(r['path'].relative_to(REPO)), 'ka': r['ka'],
                 'state': r['state'],
                 'components': {k: {'score': v[0], 'note': v[1]}
                                for k, v in r['components'].items()}}
                for r in results
            ]
            Path(args.json).write_text(_json.dumps(payload, indent=2))
            print(c(GREEN, f"  ✓ Ka JSON saved: {args.json}"))
        else:
            print_summary(results, verbose=args.verbose)
