#!/usr/bin/env python3
"""
now terminus — status dashboard
The serial layer. Works in any terminal, no dependencies beyond stdlib.
Serial → parallel → GUI upgrade path: this is the serial foundation.
"""

import subprocess, os, sys, re, math, datetime
from pathlib import Path

# ── locate repo root ──────────────────────────────────────────────────────────
HERE   = Path(__file__).resolve().parent
REPO   = HERE.parent.parent   # tools/terminus/ → now/

# ── ANSI (works on any ANSI-capable terminal; degrades cleanly otherwise) ────
BOLD   = '\033[1m'
DIM    = '\033[2m'
RED    = '\033[31m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
CYAN   = '\033[36m'
BLUE   = '\033[34m'
MAGENTA= '\033[35m'
RESET  = '\033[0m'

NO_COLOR = not sys.stdout.isatty() or os.environ.get('NO_COLOR')

def c(color, text):
    return text if NO_COLOR else f"{color}{text}{RESET}"

def sh(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=REPO)
    return r.stdout.strip()

# ── terminal width ────────────────────────────────────────────────────────────
def term_width():
    try:
        return os.get_terminal_size().columns
    except:
        return 80

def sep(char='─', label=''):
    w = term_width()
    if label:
        pad = (w - len(label) - 2) // 2
        return c(DIM, char * pad) + ' ' + c(BOLD, label) + ' ' + c(DIM, char * (w - pad - len(label) - 2))
    return c(DIM, char * w)

def bar(val, max_val=100, width=20, full='█', empty='░'):
    filled = round(width * val / max_val) if max_val else 0
    filled = max(0, min(filled, width))
    color = GREEN if val < 60 else (YELLOW if val < 85 else RED)
    return c(color, full * filled) + c(DIM, empty * (width - filled))

# ── data collectors ───────────────────────────────────────────────────────────

def disk_info():
    lines = sh("df -h /").splitlines()
    if len(lines) < 2:
        return []
    result = []
    for line in lines[1:]:
        parts = line.split()
        if len(parts) >= 6:
            result.append({
                'fs': parts[0], 'size': parts[1],
                'used': parts[2], 'avail': parts[3],
                'pct': int(parts[4].rstrip('%')), 'mount': parts[5]
            })
    return result

def git_log(n=8):
    raw = sh(f"git log --oneline -n {n} --format='%h|%ae|%s|%ar'")
    entries = []
    for line in raw.splitlines():
        parts = line.split('|', 3)
        if len(parts) == 4:
            sha, email, msg, age = parts
            # extract agent slug from email or commit message
            agent = email.split('@')[0][:12] if '@' in email else 'unknown'
            entries.append({'sha': sha, 'agent': agent, 'msg': msg[:55], 'age': age})
    return entries

def current_branch():
    return sh("git branch --show-current")

def open_missions():
    """Parse ROADMAP.md for unchecked [ ] items."""
    roadmap = REPO / 'ROADMAP.md'
    if not roadmap.exists():
        return []
    missions = []
    with open(roadmap) as f:
        for line in f:
            m = re.match(r'\s*-\s*\[\s*\]\s*(.+)', line)
            if m:
                missions.append(m.group(1).strip())
    return missions[:8]

def ka_scores(top=6):
    """Quick Ka estimation for .md files in the repo."""
    scores = []
    for path in REPO.rglob('*.md'):
        if any(p.startswith('.') for p in path.relative_to(REPO).parts):
            continue
        if '_duplicates' in str(path) or 'legacy' in str(path):
            continue
        try:
            size  = path.stat().st_size
            mtime = path.stat().st_mtime
            content = path.read_text(errors='ignore')

            size_score   = min(math.log1p(size) / math.log(50000) * 30, 30)
            link_count   = len(re.findall(r'\[.+?\]\(.+?\)', content))
            link_score   = min(link_count / 10 * 20, 20)
            age_days     = (datetime.datetime.now().timestamp() - mtime) / 86400
            recency      = 20 if age_days < 7 else (12 if age_days < 30 else (5 if age_days < 90 else 0))

            # git commit count for this file
            commit_proc = subprocess.run(
                ["git", "rev-list", "--count", "HEAD", "--", str(path.relative_to(REPO))],
                cwd=REPO,
                capture_output=True,
                text=True,
                check=False,
            )
            commit_raw = commit_proc.stdout.strip()
            commits    = int(commit_raw) if commit_raw.isdigit() else 0
            commit_score = min(commits / 15 * 30, 30)

            ka = size_score + link_score + recency + commit_score
            scores.append({'name': path.relative_to(REPO), 'ka': round(ka), 'commits': commits})
        except Exception:
            continue

    scores.sort(key=lambda x: x['ka'], reverse=True)
    return scores[:top]

def agent_activity():
    """Count commits per agent slug in recent history."""
    raw = sh("git log --format='%ae' -n 50")
    counts = {}
    for email in raw.splitlines():
        slug = email.split('@')[0][:14] if email else 'unknown'
        counts[slug] = counts.get(slug, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:5]

# ── render ────────────────────────────────────────────────────────────────────

def render():
    now = datetime.datetime.now().strftime('%Y-%m-%d  %H:%M:%S')
    branch = current_branch()
    w = term_width()

    print()
    title = f"  n o w  —  t e r m i n u s  "
    print(c(BOLD, title.center(w)))
    print(c(DIM, f"  {now}   branch: {branch}".center(w)))
    print()

    # ── disk ──────────────────────────────────────────────────────────────────
    print(sep(label='DISK'))
    for d in disk_info():
        b = bar(d['pct'])
        pct_color = GREEN if d['pct'] < 70 else (YELLOW if d['pct'] < 90 else RED)
        print(f"  {c(CYAN, d['mount']): <8}  {b}  {c(pct_color, str(d['pct'])+'%'): <5}"
              f"  {c(DIM, d['avail'])} free of {c(DIM, d['size'])}")

    # ── open missions ─────────────────────────────────────────────────────────
    print()
    print(sep(label='OPEN MISSIONS'))
    missions = open_missions()
    if missions:
        for m in missions:
            print(f"  {c(YELLOW, '○')}  {m}")
    else:
        print(f"  {c(GREEN, '✓')}  All roadmap items complete (or no ROADMAP.md)")

    # ── Ka levels ─────────────────────────────────────────────────────────────
    print()
    print(sep(label='Ka LEVELS  (document energy)'))
    ka = ka_scores()
    max_ka = ka[0]['ka'] if ka else 100
    for entry in ka:
        b = bar(entry['ka'], max_val=max(max_ka, 1), width=16)
        name = str(entry['name'])[-38:].ljust(38)
        print(f"  {c(DIM, name)}  {b}  {c(CYAN, str(entry['ka']).rjust(3))}  "
              f"{c(DIM, str(entry['commits'])+'c')}")

    # ── recent git activity ───────────────────────────────────────────────────
    print()
    print(sep(label='RECENT ACTIVITY'))
    for entry in git_log():
        agent = c(MAGENTA, entry['agent'].ljust(14))
        sha   = c(DIM, entry['sha'])
        age   = c(DIM, entry['age'].rjust(12))
        print(f"  {sha}  {agent}  {entry['msg'][:50]}  {age}")

    # ── agent activity ────────────────────────────────────────────────────────
    print()
    print(sep(label='AGENTS  (last 50 commits)'))
    for slug, count in agent_activity():
        b = bar(count, max_val=50, width=12)
        print(f"  {c(MAGENTA, slug.ljust(16))}  {b}  {c(CYAN, str(count))} commits")

    # ── footer ────────────────────────────────────────────────────────────────
    print()
    print(c(DIM, '  ~∰◊€π¿🌌∞~   terminus in momentum'.center(w)))
    print(c(DIM, sep()))
    print()

# ── entry ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='now terminus status dashboard')
    parser.add_argument('--watch', '-w', type=int, metavar='SECS',
                        help='refresh every N seconds (Ctrl+C to exit)')
    args = parser.parse_args()

    if args.watch:
        import time
        while True:
            print('\033[2J\033[H', end='')
            render()
            print(c(DIM, f"  refreshing every {args.watch}s — Ctrl+C to exit\n"))
            time.sleep(args.watch)
    else:
        render()
