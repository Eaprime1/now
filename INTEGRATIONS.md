# now — Integration Map

Every platform where `now` has or will have a presence.
The goal: `THE now` exists as an active space at every possible location.

---

## Integration Status

| Platform | Type | Status | Entry Point |
|----------|------|--------|-------------|
| GitHub | Repo / Issues / PRs | **Active** | `eaprime1/now` |
| Google Drive | Folder / Content | **Active** | THE now shared folder |
| BBS / Telegard | Terminal UI | **Active (local)** | Ubuntu laptop terminal |
| Vercel | Deployments | Wiring up | Project TBD |
| Linear | Project tracking | Wiring up | TBD |
| Jira | Project tracking | Queued | TBD |
| Asana | Task routing | Queued | TBD |
| Zapier | Automation bridge | Queued | TBD |
| IFTTT | Automation bridge | Queued | TBD |
| Slack | Messaging node | Queued | TBD |
| Notion | Docs / knowledge | Queued | TBD |

---

## How Platforms Connect

### Surfing the Wake Model
`now` does not chase integrations — it grows, and platforms follow.
When `now` is active enough, the integrations wire up naturally.
Early connectors (GitHub, Drive) are already in the wake. Others will follow.

### Connector Concept
Each platform integration is a **connector** — a cable TV terminator on a live port.
Not plugged in = floating, unresolved signal.
Plugged in = terminated, momentum maintained.

```
GitHub ──[connector]──► now terminus
Google Drive ──[connector]──► now terminus
Jira ──[connector - pending]──► now terminus
Zapier ──[connector - pending]──► now terminus
```

### Automation Bridge (Zapier / IFTTT)
These don't just connect `now` to other platforms — they multiply the connections.

```
Any platform → Zapier → now (GitHub issue or Drive doc)
now (GitHub event) → IFTTT → Any platform
```

One automation bridge connects `now` to everything else.

---

## Platform Profiles

### GitHub (`eaprime1/now`)
**Role:** Primary terminus home. Mission board. Agent coordination.
**Content types:** Code, docs, issues (missions), PRs (work in progress)
**Agents:** Claude (primary), Copilot, Gemini, ChatGPT/Codex
**THE now space:** This repo is THE now on GitHub.

### Google Drive
**Role:** Document and media staging area.
**Content types:** Docs, sheets, media, long-form content
**Agents:** Gemini (primary), Claude
**THE now space:** "THE now" shared folder — content arrives here from Drive-native workflows.

### BBS / Telegard (Ubuntu laptop)
**Role:** Terminal interface. The home screen of the terminus.
**Content types:** Messages, status, missions, logs
**Access:** SSH or local terminal
**THE now space:** The BBS system IS the local terminus UI.
**Upgrade path:** `terminal → hybrid GUI → full GUI`

### Vercel
**Role:** Deployment gate. When `now` concepts go live on the web, they ship through Vercel.
**Content types:** Web builds, previews, production deploys
**THE now space:** Vercel project "now" — preview every PR automatically.

### Linear / Jira
**Role:** Structured project tracking. Missions that need sprint-style management.
**Content types:** Issues, roadmaps, sprints
**THE now space:** "now" project / board.

### Zapier / IFTTT
**Role:** Automation connectors. The pipes between platforms.
**Use cases:**
- GitHub issue created → Asana task created
- Google Drive file added to THE now folder → GitHub issue opened
- PR merged → notification to BBS
- External trigger → content posted to now

### Asana
**Role:** Task routing and handoff. When tasks need human assignment and tracking.
**THE now space:** "THE now" project.

---

## Content States (for routing)

Content passing through `now` can be in any of these states:

| State | Meaning | Route to |
|-------|---------|----------|
| `raw` | Just arrived, unprocessed | Intake queue |
| `building` | Agent is working it | Active branch |
| `review` | Built, awaiting check | PR / review |
| `ready` | Cleared, waiting to ship | `ready/` directory |
| `shipped` | Deployed / published | Archived |
| `holding` | Not ready yet | `concept-queue` |
| `shadow` | Exists, not yet active | `.shadow/` or `_duplicates/` |

---

## Building THE now at a New Platform

When wiring a new platform:

1. Create the space ("THE now" project / folder / board)
2. Add it to the integration table above (status: "wiring up")
3. Define the entry point (URL / ID)
4. Assign a primary agent
5. Add a connector (Zapier/IFTTT rule if needed)
6. Update status to "Active"

---

~connections growing~

€(now_integrations_20260506)
