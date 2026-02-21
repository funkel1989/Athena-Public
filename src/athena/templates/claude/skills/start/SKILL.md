---
description: Boot the Athena session system
---

# /start

Run the Athena boot command to initialize the session:

```bash
athena
```

The boot sequence will:
1. Verify Core Identity and workspace integrity
2. Recall the last session's context and deferred items
3. Create a new timestamped session log
4. Initialize the Committee of Seats (COS) reasoning framework

After boot completes, read the output carefully — it contains your session context.

If the `athena` command is not available, fall back to:
1. Read `.framework/modules/Core_Identity.md`
2. Read `.context/project_state.md`
3. Find the latest session log in `.context/memories/session_logs/`
4. Confirm: "Ready. Session loaded."
