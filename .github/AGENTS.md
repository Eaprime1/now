# now — GitHub Agent Instructions

For Copilot, Codex, Gemini, and any GitHub-native AI agent working in this repo.

---

## What this repo is

`now` is a multi-agent terminus. Content arrives in various states, gets processed by agents, and ships to its destination. You are one agent among several. Contribute to the flow — don't stall it.

## Before you work

1. Read `README.md` for the terminus model
2. Read `AGENTS.md` for the full agent guide
3. Check open issues — that's the mission board
4. Check recent PRs — don't duplicate in-flight work

## Branch naming

```
<your-slug>/<task>-<short-id>
```

## Content states

Tag your issues/PRs with content state labels:
- `state:raw` — just arrived
- `state:building` — in progress
- `state:ready` — done, waiting to ship
- `state:shipped` — merged/deployed

## Conservation bias

Do not delete files without a clear reason. When in doubt, move to `_duplicates/` or `legacy/`. Duplicates are gravity tokens — proof of value.

## Witnessing

Use `~` in commit messages or comments when you're noting something without certainty:
```
~observed: this function is referenced in three places but only tested in one~
```

## Commit style

```
<action>: <what>

Brief why if non-obvious.
```

Actions: `add`, `fix`, `update`, `remove`, `refactor`, `docs`

---

~agents welcome~
