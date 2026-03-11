# Temporal Heartbeat & Persistence Logic
**Operational Mode:** Active Production (15-Minute Pulse)

---

## 🕒 The 15-Minute Pulse (Standard Routine)
Every 15 minutes, the `apscheduler` triggers the following "Observation Loop":

### 1. The Monday.com "Stall" Scan
- **Logic:** Scan all "Active" boards for tasks in "In Progress" for > 48 hours with no updates.
- **Action:** Trigger the `n8n_handshake` to post a gentle "Status Check" comment on the item and flag it in the Notion Dashboard.

### 2. The Transcript Queue Check
- **Logic:** Check the local `/recordings` or n8n Webhook for any unprocessed meeting transcripts.
- **Action:** If a new transcript is found, immediately initiate the **Reasoning Layer** to extract MOMs and Action Items.

---

## The 09:00 AM "Morning Brief" (Daily Routine)
Every morning perform the "Daily Alignment":

### 1. Executive Summary Generation
- **Action:** Consolidate all tasks completed in the last 24 hours into a 3-bullet "Daily Win" summary.
- **Delivery:** Send to the #production-sync Slack channel via n8n.

### 2. Priority Re-Ranking
- **Logic:** Compare "Upcoming Deadlines" on Monday.com against "Current Resource Load" in Notion.
- **Action:** Flag any projects at risk of "Bottlenecking" to the Creative Lead.

---

## Persistence Guardrails
- **Self-Healing:** If a connection to the n8n Webhook fails, log the "Last Known State" and retry with exponential backoff (1min, 5min, 15min).
- **Silent Mode:** Between 22:00 and 07:00, the Heartbeat remains active but suppresses all non-critical Slack notifications to respect "Deep Work" hours.

---

## Trigger Mechanics (Internal)
- **Engine:** `APScheduler` (Background Process)
- **Bridge:** `n8n_trigger.py`
- **State File:** `agents/memory/heartbeat_state.json`