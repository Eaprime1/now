#!/usr/bin/env python3
"""
Content Audit — now terminus
Full structural audit of repo content: states, Ka, word counts,
duplicate detection, missing metadata, orphan files.
The sovereign perspective on what's actually in now.
"""

import re, os, sys, json, datetime, hashlib, argparse
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

BOLD  = '\033[1m'; DIM = '\033[2m'; CYAN = '\033[36m'
GREEN = '\033[32m'; YELLOW = '\033[33m'; RED = '\033[31m'; RESET = '\033[0m'
NO_COLOR = not sys.stdout.isatty() or os.environ.get('NO_COLOR')
def c(col, txt): return txt if NO_COLOR else f"{col}{txt}{RESET}"

# ── content state detection ───────────────────────────────────────────────────
STATE_PATTERNS = {
    'shipped':  re.compile(r'state:\s*shipped|status.*shipped|✅.*ship', re.I),
    'ready':    re.compile(r'state:\s*ready|status.*ready|ready.*ship', re.I),
    'review':   re.compile(r'state:\s*review|status.*review', re.I),
    'building': re.compile(r'state:\s*building|in.progress|wip|work.in.progress', re.I),
    'holding':  re.compile(r'state:\s*holding|not.now|concept.queue', re.I),
    'raw':      re.compile(r'state:\s*raw', re.I),
}

def detect_state(text: str, path: Path) -> str:
    if '_duplicates' in str(path): return 'duplicate'
    if 'legacy' in str(path): return 'legacy'
    if 'holding' in str(path): return 'holding'
    for state, pat in STATE_PATTERNS.items():
        if pat.search(text):
            return state
    return 'raw'

def has_anchor(text: str) -> bool:
    return bool(re.search(r'€\([^)]+\)', text))

def has_date(text: str) -> bool:
    return bool(re.search(r'20\d\d-\d\d-\d\d', text))

def extract_links(text: str) -> list[str]:
    return re.findall(r'\[.+?\]\(([^)]+)\)', text)

def file_hash(path: Path) -> str:
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()
    except:
        return ''

# ── audit one file ────────────────────────────────────────────────────────────
def audit_file(path: Path) -> dict:
    try:
        text  = path.read_text(errors='ignore')
        stat  = path.stat()
    except Exception as e:
        return {'path': path, 'error': str(e)}

    links = extract_links(text)
    broken_links = [l for l in links if not l.startswith('http') and not (REPO / l).exists()]

    return {
        'path':         path,
        'rel':          str(path.relative_to(REPO)),
        'state':        detect_state(text, path),
        'size_bytes':   stat.st_size,
        'line_count':   text.count('\n'),
        'word_count':   len(text.split()),
        'char_count':   len(text),
        'has_anchor':   has_anchor(text),
        'has_date':     has_date(text),
        'link_count':   len(links),
        'broken_links': broken_links,
        'hash':         file_hash(path),
        'mtime':        stat.st_mtime,
        'mtime_str':    datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d'),
    }

# ── full audit ────────────────────────────────────────────────────────────────
def run_audit(include_hidden=False) -> dict:
    files = []
    for ext in ('.md', '.txt', '.py', '.sh', '.json', '.yml', '.yaml'):
        for path in REPO.rglob(f'*{ext}'):
            parts = path.relative_to(REPO).parts
            if not include_hidden and any(p.startswith('.') for p in parts):
                continue
            files.append(path)

    results  = [audit_file(p) for p in sorted(files)]
    by_state = defaultdict(list)
    for r in results:
        by_state[r.get('state', 'unknown')].append(r)

    hashes = defaultdict(list)
    for r in results:
        if r.get('hash'):
            hashes[r['hash']].append(r['rel'])
    duplicates = {h: paths for h, paths in hashes.items() if len(paths) > 1}

    missing_anchor = [r for r in results if r.get('state') not in ('legacy','duplicate') and not r.get('has_anchor')]
    broken = [r for r in results if r.get('broken_links')]

    return {
        'audit_at':   datetime.datetime.now().isoformat(),
        'total_files': len(results),
        'results':    results,
        'by_state':   dict(by_state),
        'duplicates': duplicates,
        'missing_anchor': missing_anchor,
        'broken_links': broken,
    }

# ── display ───────────────────────────────────────────────────────────────────
STATE_COLORS = {
    'shipped': GREEN, 'ready': CYAN, 'review': CYAN,
    'building': YELLOW, 'raw': DIM, 'holding': DIM,
    'legacy': DIM, 'duplicate': RED,
}

def print_audit(data: dict, verbose=False):
    print()
    print(c(BOLD, f"  Content Audit — {data['total_files']} files   {data['audit_at'][:19]}"))
    print()

    print(c(BOLD, '  State Summary'))
    print(c(DIM,  '  ' + '─' * 50))
    for state, items in sorted(data['by_state'].items()):
        col = STATE_COLORS.get(state, RESET)
        total_words = sum(r.get('word_count', 0) for r in items)
        print(f"  {c(col, state.ljust(12))}  {len(items):>4} files   {total_words:>8,} words")
    print()

    dups = data['duplicates']
    if dups:
        print(c(BOLD, f"  Duplicate Files  ({len(dups)} groups — gravity tokens)"))
        print(c(DIM,  '  ' + '─' * 50))
        for h, paths in list(dups.items())[:10]:
            print(f"  {c(DIM, h[:8])}  {len(paths)} copies:")
            for p in paths:
                print(f"    {c(YELLOW, p)}")
        if len(dups) > 10:
            print(f"  ... and {len(dups)-10} more groups")
        print()

    broken = data['broken_links']
    if broken:
        print(c(BOLD, f"  Broken Internal Links  ({len(broken)} files)"))
        print(c(DIM,  '  ' + '─' * 50))
        for r in broken[:8]:
            print(f"  {c(RED, r['rel'])}")
            for bl in r['broken_links'][:3]:
                print(f"    → {bl}")
        print()

    missing = data['missing_anchor']
    if missing:
        print(c(BOLD, f"  Missing €(anchor) Tags  ({len(missing)} files)"))
        print(c(DIM,  '  ' + '─' * 50))
        for r in missing[:10]:
            print(f"  {c(DIM, r['rel'])}")
        if len(missing) > 10:
            print(f"  ... and {len(missing)-10} more")
        print()

    if verbose:
        print(c(BOLD, '  All Files'))
        print(c(DIM,  '  ' + '─' * 80))
        print(f"  {'File':<50} {'state':<10} {'words':>6} {'lines':>6} {'date'}")
        print(c(DIM,  '  ' + '─' * 80))
        for r in sorted(data['results'], key=lambda x: x.get('word_count',0), reverse=True):
            if 'error' in r: continue
            col = STATE_COLORS.get(r['state'], RESET)
            name = r['rel'][-50:].ljust(50)
            print(f"  {c(DIM,name)}  {c(col, r['state'].ljust(10))}  "
                  f"{r['word_count']:>6,}  {r['line_count']:>6,}  {r['mtime_str']}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Content Audit — now terminus')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show all files')
    parser.add_argument('--hidden', action='store_true', help='Include hidden dirs')
    parser.add_argument('--json', metavar='PATH', help='Save audit as JSON')
    args = parser.parse_args()

    print(c(DIM, '\n  Auditing...'), end='', flush=True)
    data = run_audit(include_hidden=args.hidden)
    print(c(GREEN, ' done'))

    print_audit(data, verbose=args.verbose)

    if args.json:
        safe = {k: v for k, v in data.items() if k != 'results'}
        safe['results'] = [{k2: v2 for k2, v2 in r.items() if k2 != 'path'}
                           for r in data['results']]
        Path(args.json).write_text(json.dumps(safe, indent=2, default=str))
        print(c(GREEN, f"  ✓ JSON saved: {args.json}"))
