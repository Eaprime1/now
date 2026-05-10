# terminus tools

The serial layer interface for the `now` terminus.
Works in any terminal. No dependencies beyond Python stdlib (3.9+).

This is the BBS home screen — the foundation of the interface stack.

```
terminal (this) → richer terminal → hybrid GUI → full GUI
serial layer    → parallel       → AV          → HDMI
```

---

## Tools

### status.py — Terminus Dashboard

One-shot or watch-mode view of the terminus state.

```bash
# snapshot
python3 status.py

# live refresh every 30 seconds
python3 status.py --watch 30
```

Shows:
- Disk usage with bar graph
- Open missions (from ROADMAP.md)
- Ka levels — top documents by energy score
- Recent git activity with agent attribution
- Agent commit counts

### ka.py — Ka Level Analyzer

Scores every document in the repo on the Ka scale (0–100).

```bash
# full report
python3 ka.py

# verbose — shows component breakdown per doc
python3 ka.py --verbose

# single file deep-dive
python3 ka.py --file README.md

# only show high-energy docs
python3 ka.py --threshold 60

# include hidden dirs (.claude etc)
python3 ka.py --hidden
```

**Ka components (each 0–25):**

| Component | What it measures |
|-----------|-----------------|
| Weight | File size — physical presence |
| Iterations | Git commit count — how much it's been worked |
| Connections | Links in + links out — how connected it is |
| Recency | Last modified — recent attention = high energy |

**Ka states and routing:**

| Ka | State | Action |
|----|-------|--------|
| 80–100 | LAUNCH | Ready to ship or graduate to next repo |
| 60–79 | REVIEW | Queue for routing decision |
| 40–59 | BUILDING | Keep working |
| 20–39 | RAW | Needs attention or concept-queue |
| 0–19 | HOLDING | Candidate for concept-queue |

---

## The Philosophy

Ka is not time-based — it's weight-based.
A document that has been iterated 15 times, linked to from 8 places, and recently touched
has higher Ka than a document that's just old.

When Ka crosses a threshold, the content routes to its next stage automatically.
This is the stepping motor: the document always knows its one next step.

---

## Upgrade Path

These tools are the serial layer. Future layers will add:

- `--watch` mode + curses full-screen (parallel layer)
- Web dashboard via simple HTTP server (AV layer)
- Full GUI integration (HDMI layer)

Each layer wraps the previous one — the terminal always works.
