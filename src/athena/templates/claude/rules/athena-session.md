---
globs: "*"
description: Athena session management discipline
---

## Athena Session Discipline

This workspace uses the Athena SDK for session management and long-term memory.

### Session Lifecycle

1. **Boot**: Run `athena` (or `/start`) at the start of every session to load context and create a session log.
2. **Save**: Run `athena save "summary"` (or `/save`) after completing meaningful work.
3. **End**: Run `athena --end` (or `/end`) when the session is complete.

### Memory-First Principle

Before answering questions about past decisions, prior work, or project history:
- Check `.context/memories/session_logs/` for relevant session logs
- Check `.context/project_state.md` for current project status
- If Athena MCP is available, use `smart_search` to find relevant context

### Committee of Seats (COS)

For non-trivial decisions, spawn the appropriate COS agents from `.claude/agents/`:
- Simple changes: No committee needed
- Medium changes (new feature, refactor): Spawn 2-3 relevant agents
- Complex changes (architecture, security, deploy): Convene the full committee
