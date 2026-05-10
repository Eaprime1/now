# Terminus Miners

Content intelligence tools for the `now` terminus.
Gather stats, track lexemes, audit state, archive messages.

---

## Tools

### lexeme.py — Word & Lexeme Tracker

Mines every word across the repo. Tracks frequency, location, first use.
Exact copies of source docs preserved for analysis. Links to glossary concept.

```bash
# terminal report, top 40 words
python3 lexeme.py

# save to JSON + CSV for spreadsheet/database
python3 lexeme.py --json lexeme.json --csv lexeme.csv

# archive exact snapshots of all docs
python3 lexeme.py --snapshots ./snapshots/

# find all locations of a specific word
python3 lexeme.py --word terminus

# include .claude/ and hidden dirs
python3 lexeme.py --hidden

# mine specific extensions only
python3 lexeme.py --ext .md .txt
```

### audit.py — Content Audit

Full structural audit: content states, duplicates, broken links, missing anchors, file stats.
The sovereign perspective on what's actually in `now`.

```bash
# summary audit
python3 audit.py

# verbose — show all files with states
python3 audit.py --verbose

# save as JSON
python3 audit.py --json audit.json
```

**State detection** — reads content and path for state signals:
| State | Signal |
|-------|--------|
| `shipped` | File contains "state: shipped", "✅ ship" |
| `ready` | "state: ready", "ready to ship" |
| `review` | "state: review" |
| `building` | "in progress", "wip" |
| `holding` | "not_now", "concept-queue" |
| `legacy` | In `legacy/` path |
| `duplicate` | In `_duplicates/` path |
| `raw` | No state signal found |

---

## GitHub Actions

Both miners run automatically on push to `main` via `.github/workflows/miners.yml`.
Output committed to `.miners/` directory (snapshots gitignored for size).

---

## Data Flow

```
repo docs → lexeme.py → .miners/lexeme_YYYYMMDD.json
                      → .miners/lexeme_YYYYMMDD.csv (for spreadsheet/Sheets)
                      → .miners/snapshots_YYYYMMDD/ (exact copies)

repo docs → audit.py  → .miners/audit_YYYYMMDD.json
                      → terminal report
```

The JSON outputs are designed for linking to a glossary spreadsheet or database.
Every word is tracked with its locations — foundation for the lexeme→glossary pipeline.

---

## The Lexeme → Glossary Pipeline (planned)

```
lexeme.py (mine)
  → lexeme.json (all words + locations)
  → filter: high-frequency + domain-specific
  → glossary.csv (term, definition, first_file, count)
  → Google Sheets / Notion database
  → back-link from docs to glossary entries
```
