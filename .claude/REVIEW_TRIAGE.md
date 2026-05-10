# Review Triage Guide

**For: hodie / today / primehaven repos**
**Purpose:** Decide quickly what to act on vs. acknowledge vs. skip

---

## The Three Buckets

```
~!  ACT NOW      → Fix before next merge
~~  ACKNOWLEDGE  → Log as issue, address later
~   SKIP         → Noted but not needed here
```

---

## Decision Flow

```
Review comment arrives
        │
        ▼
Does it break something?
   YES → ~! ACT NOW
   NO  ↓
        │
        ▼
Is it a real pattern issue?
   YES → ~~ ACKNOWLEDGE (create issue)
   NO  ↓
        │
        ▼
Is it style/preference?
   YES → ~ SKIP (acknowledge, move on)
```

---

## ACT NOW ~! (Fix before merging)

These matter - address immediately:

| Type | Example | Why |
|------|---------|-----|
| Hardcoded paths | `/home/eric/...` in scripts | Breaks on other machines |
| Security holes | API keys in code, unvalidated input | Actual risk |
| Broken links | README points to missing files | Confuses collaborators |
| Wrong structure | Docs describe paths that don't exist | Misleads AI/human sessions |
| Import errors | `import module_that_doesnt_exist` | Script fails |

**~!Example~!** - Fixed hardcoded paths in scripts

---

## ACKNOWLEDGE ~~ (Create issue, do later)

Real improvements, not urgent:

| Type | Example | Action |
|------|---------|--------|
| Missing docs | "Entity has no README" | Issue: add README |
| Outdated references | "This file moved" | Issue: update reference |
| Better organization | "These should be in one folder" | Issue: reorganize |
| Performance | "Script could be faster" | Issue: optimize |
| Consistency | "Different date formats used" | Issue: standardize |

**Pattern:** If you'd want to come back to it → create issue

---

## SKIP ~ (Note and move on)

Not worth your time right now:

| Type | Example | Why Skip |
|------|---------|----------|
| Style preferences | "Use double quotes not single" | No real impact |
| Generic suggestions | "Consider adding error handling" | Vague, not specific |
| Template boilerplate | SECURITY.md version numbers | Auto-generated noise |
| Hypothetical futures | "You might want to add X someday" | Not now |
| Duplicate comments | Same point raised multiple times | Act on it once |

---

## The SECURITY.md Situation

The one in your repo right now is **generic GitHub template** - not real:

```
| 5.1.x | ✅ |   ← These versions mean nothing here
| 5.0.x | ❌ |
```

**Suggested action:** Replace with something real, or delete it.
Do you want me to write a relevant one for this project?

---

## For Auto-Reviews (Claude)

**Claude Code Review** (`.github/workflows/`) runs on every PR.
**Pattern to use:**

1. Read the review summary first
2. Look for `~!` level issues → fix immediately
3. Scan for repeated themes → those are real patterns
4. Create 1-3 issues max per PR → don't chase everything
5. Close the review → move on

---

## Issue Labels to Create on GitHub

Go to: GitHub → Issues → Labels → New label

| Label | Color | Use For |
|-------|-------|---------|
| `act-now` | Red | Blocking issues |
| `acknowledge` | Yellow | Real but not urgent |
| `~witnessed~` | Gray | Noted, not acting |
| `cleanup` | Blue | Organization tasks |
| `primehaven` | Purple | Ecosystem-level work |

---

## Ruleset for Main (GitHub Settings)

**Settings → Rules → Rulesets → New ruleset**

```
Name: protect-main
Target branch: main

Enable:
✅ Require pull request
   - Required approvals: 1  (keeps main review-protected)
   - Dismiss stale reviews: YES

✅ Block force pushes

❌ Require deployments to succeed (add later)

Leave OFF for now:
❌ Required status checks (add later when CI stable)
❌ Require signed commits (adds friction)
❌ Require linear history (merge commits are fine)
```

---

~triage system ready~

€(review_triage_20260325)
