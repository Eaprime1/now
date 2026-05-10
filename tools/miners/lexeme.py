#!/usr/bin/env python3
"""
Lexeme Miner — now terminus
Tracks every word in the repo: frequency, location, first/last seen.
The exact copy of each source doc is preserved for analysis.
Output: terminal report, JSON for glossary linking, CSV for spreadsheets.
"""

import re, json, csv, sys, os, datetime, argparse
from pathlib import Path
from collections import defaultdict, Counter

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent

BOLD  = '\033[1m'; DIM = '\033[2m'; CYAN = '\033[36m'
GREEN = '\033[32m'; YELLOW = '\033[33m'; RESET = '\033[0m'
NO_COLOR = not sys.stdout.isatty() or os.environ.get('NO_COLOR')
def c(col, txt): return txt if NO_COLOR else f"{col}{txt}{RESET}"

STOP_WORDS = {
    'a','an','the','and','or','but','in','on','at','to','for','of','with',
    'by','from','as','is','it','its','be','are','was','were','been','have',
    'has','had','do','does','did','will','would','could','should','may','might',
    'not','no','so','if','then','that','this','these','those','i','we','you',
    'he','she','they','my','your','our','his','her','their','what','which',
    'who','when','where','how','all','any','more','other','into','up','out',
    'also', 'can', 'about', 'than', 'just', 'each', 'there', 'here',
}

def tokenize(text: str) -> list[str]:
    """Extract clean word tokens from markdown text."""
    text = re.sub(r'```.*?```', ' ', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', ' ', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'[#*_~|>]', ' ', text)
    text = re.sub(r'https?://\S+', ' ', text)
    tokens = re.findall(r"[a-zA-Z][a-zA-Z'_-]{1,}", text)
    return [t.lower().strip("'-_") for t in tokens if len(t) > 1]

def collect_files(root: Path, include_hidden=False, extensions=('.md', '.txt', '.py', '.sh')) -> list[Path]:
    paths = []
    for ext in extensions:
        for path in root.rglob(f'*{ext}'):
            parts = path.relative_to(root).parts
            if not include_hidden and any(p.startswith('.') for p in parts):
                continue
            if '_duplicates' in parts:
                continue
            paths.append(path)
    return sorted(paths)

def mine(files: list[Path]) -> dict:
    """
    Returns:
      word_freq:  {word: total_count}
      word_locs:  {word: [(file_rel, line_no)]}
      file_stats: {file_rel: {words, unique, top5}}
      doc_snapshots: {file_rel: raw_text}
    """
    word_freq  = Counter()
    word_locs  = defaultdict(list)
    file_stats = {}
    doc_snapshots = {}

    for path in files:
        try:
            text = path.read_text(errors='ignore')
        except Exception:
            continue

        rel = str(path.relative_to(REPO))
        doc_snapshots[rel] = text

        tokens_in_file = Counter()
        for lineno, line in enumerate(text.splitlines(), 1):
            for word in tokenize(line):
                if word not in STOP_WORDS and not word.isdigit():
                    word_freq[word] += 1
                    tokens_in_file[word] += 1
                    word_locs[word].append((rel, lineno))

        file_stats[rel] = {
            'total_words': sum(tokens_in_file.values()),
            'unique_words': len(tokens_in_file),
            'top5': tokens_in_file.most_common(5),
            'char_count': len(text),
            'line_count': text.count('\n'),
        }

    return {
        'word_freq': word_freq,
        'word_locs': word_locs,
        'file_stats': file_stats,
        'doc_snapshots': doc_snapshots,
        'mined_at': datetime.datetime.now().isoformat(),
        'file_count': len(files),
    }

def report_terminal(data: dict, top_n=40):
    freq  = data['word_freq']
    stats = data['file_stats']
    total_words = sum(freq.values())

    print()
    print(c(BOLD, f"  Lexeme Report — {data['file_count']} files   {data['mined_at'][:19]}"))
    print(c(DIM,  f"  Total word occurrences: {total_words:,}   Unique lexemes: {len(freq):,}"))
    print()

    print(c(BOLD, f"  Top {top_n} Lexemes"))
    print(c(DIM,  '  ' + '─' * 60))
    bar_max = freq.most_common(1)[0][1] if freq else 1
    for word, count in freq.most_common(top_n):
        filled = round(20 * count / bar_max)
        b = c(CYAN, '█' * filled) + c(DIM, '░' * (20 - filled))
        pct = count / total_words * 100
        print(f"  {word:<20} {b}  {count:>5}  {c(DIM, f'{pct:.1f}%')}")

    print()
    print(c(BOLD, '  File Stats'))
    print(c(DIM,  '  ' + '─' * 70))
    print(f"  {'File':<45} {'words':>6} {'unique':>7} {'lines':>6}")
    print(c(DIM,  '  ' + '─' * 70))
    for rel, s in sorted(stats.items(), key=lambda x: x[1]['total_words'], reverse=True)[:20]:
        name = rel[-45:].ljust(45)
        print(f"  {c(DIM, name)}  {s['total_words']:>6,}  {s['unique_words']:>7,}  {s['line_count']:>6,}")
    print()

def save_json(data: dict, out_path: Path):
    payload = {
        'mined_at':   data['mined_at'],
        'file_count': data['file_count'],
        'top_100': dict(data['word_freq'].most_common(100)),
        'file_stats': data['file_stats'],
        'word_locations': {w: locs[:50] for w, locs in list(data['word_locs'].items())[:500]},
    }
    out_path.write_text(json.dumps(payload, indent=2))
    print(c(GREEN, f"  ✓ JSON saved: {out_path}"))

def save_csv(data: dict, out_path: Path):
    with open(out_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['word', 'count', 'first_file', 'first_line'])
        for word, count in data['word_freq'].most_common():
            locs = data['word_locs'].get(word, [])
            first_file, first_line = (locs[0] if locs else ('', ''))
            writer.writerow([word, count, first_file, first_line])
    print(c(GREEN, f"  ✓ CSV saved:  {out_path}"))

def save_snapshots(data: dict, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {'mined_at': data['mined_at'], 'files': []}
    for rel, text in data['doc_snapshots'].items():
        safe = rel.replace('/', '__').replace('\\', '__')
        dest = out_dir / safe
        dest.write_text(text)
        manifest['files'].append({'original': rel, 'snapshot': safe})
    (out_dir / 'MANIFEST.json').write_text(json.dumps(manifest, indent=2))
    print(c(GREEN, f"  ✓ Snapshots:  {out_dir}  ({len(data['doc_snapshots'])} files)"))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lexeme Miner — now terminus')
    parser.add_argument('--top', type=int, default=40, help='Top N lexemes to show')
    parser.add_argument('--json', metavar='PATH', help='Save full report as JSON')
    parser.add_argument('--csv',  metavar='PATH', help='Save word list as CSV')
    parser.add_argument('--snapshots', metavar='DIR', help='Save exact doc snapshots to dir')
    parser.add_argument('--word', '-w', help='Show all locations for a specific word')
    parser.add_argument('--hidden', action='store_true', help='Include hidden dirs')
    parser.add_argument('--ext', nargs='+', default=['.md','.txt','.py','.sh'],
                        help='File extensions to mine')
    args = parser.parse_args()

    exts = tuple(e if e.startswith('.') else f'.{e}' for e in args.ext)
    files = collect_files(REPO, include_hidden=args.hidden, extensions=exts)
    print(c(DIM, f"\n  Mining {len(files)} files..."), end='', flush=True)
    data = mine(files)
    print(c(GREEN, ' done'))

    if args.word:
        locs = data['word_locs'].get(args.word.lower(), [])
        print(f"\n  '{args.word}' appears {len(locs)} time(s):")
        for f, ln in locs[:30]:
            print(f"    {c(DIM, f)}:{ln}")
        if len(locs) > 30:
            print(f"    ... and {len(locs)-30} more")
    else:
        report_terminal(data, top_n=args.top)

    if args.json:
        save_json(data, Path(args.json))
    if args.csv:
        save_csv(data, Path(args.csv))
    if args.snapshots:
        save_snapshots(data, Path(args.snapshots))
