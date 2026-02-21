---
description: Close the Athena session and persist context
---

# /end

Run the Athena shutdown command:

```bash
athena --end
```

The shutdown sequence will:
1. Close the current session log with a summary
2. Update session status to "Closed"
3. Persist context for the next session

If the `athena` command is not available, fall back to:
1. Review all checkpoint entries from the current session log
2. Summarize Key Topics, Decisions Made, Action Items
3. Append the summary to the session log
4. Git add and commit the session log
5. Confirm: "Session closed and committed."
