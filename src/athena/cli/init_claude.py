"""
athena.cli.init_claude
======================

Claude Code workspace scaffolding.
Called by `athena init --ide claude` to create a complete Claude Code integration:
  - CLAUDE.md (project instructions)
  - .claude/settings.json (SessionStart hook + permissions)
  - .claude/agents/ (6 COS review agents)
  - .claude/skills/ (/start, /end, /save slash commands)
  - .claude/rules/ (session discipline + framework protection)
  - .mcp.json (Athena MCP server auto-configuration)
"""

import shutil
from pathlib import Path

# Template sources
_TEMPLATES_DIR = Path(__file__).resolve().parents[1] / "templates"
_CLAUDE_TEMPLATES = _TEMPLATES_DIR / "claude"
_AGENT_TEMPLATES = _CLAUDE_TEMPLATES / "agents"

# COS agent files to copy
_COS_AGENTS = [
    "cos-architect.md",
    "cos-guardian.md",
    "cos-operator.md",
    "cos-skeptic.md",
    "cos-compliance.md",
    "cos-strategist.md",
]


def _copy_file(src: Path, dest: Path, label: str) -> None:
    """Copy a single file if it doesn't already exist in the workspace."""
    if dest.exists():
        print(f"   ⏭️  {label} (already exists)")
        return
    if not src.exists():
        print(f"   ⚠️  {label} (source not found, skipped)")
        return
    shutil.copy2(src, dest)
    print(f"   ✅ {label}")


def _write_if_missing(path: Path, content: str, label: str) -> None:
    """Write content to a file if it doesn't already exist."""
    if path.exists():
        print(f"   ⏭️  {label} (already exists)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"   ✅ {label}")


def create_claude_config(root: Path) -> None:
    """Create comprehensive Claude Code configuration.

    Scaffolds CLAUDE.md, hooks, COS agents, skills, rules, and MCP config.
    All files use skip-if-exists guards to be idempotent.
    """
    claude_dir = root / ".claude"
    claude_dir.mkdir(exist_ok=True)

    # 1. CLAUDE.md
    claude_md_path = root / "CLAUDE.md"
    if not claude_md_path.exists():
        template_path = _TEMPLATES_DIR / "CLAUDE_ATHENA.md"
        if template_path.exists():
            shutil.copy2(template_path, claude_md_path)
        else:
            claude_md_path.write_text("# Athena Integration\n\nRun `athena` to boot.\n")
        print("   ✅ CLAUDE.md")
    else:
        print("   ⏭️  CLAUDE.md (already exists)")

    # 2. .claude/settings.json (hooks + permissions)
    _copy_file(
        _CLAUDE_TEMPLATES / "settings.json",
        claude_dir / "settings.json",
        ".claude/settings.json (hooks + permissions)",
    )

    # 3. COS Agents → .claude/agents/
    agents_dir = claude_dir / "agents"
    agents_dir.mkdir(exist_ok=True)
    print("\n   📦 COS agents...")
    for agent in _COS_AGENTS:
        _copy_file(
            _AGENT_TEMPLATES / agent,
            agents_dir / agent,
            f".claude/agents/{agent}",
        )

    # 4. Skills → .claude/skills/
    print("\n   📦 Skills...")
    for skill_name in ("start", "end", "save", "identity"):
        src = _CLAUDE_TEMPLATES / "skills" / skill_name / "SKILL.md"
        dest = claude_dir / "skills" / skill_name / "SKILL.md"
        dest.parent.mkdir(parents=True, exist_ok=True)
        _copy_file(src, dest, f".claude/skills/{skill_name}/SKILL.md")

    # 5. Rules → .claude/rules/
    rules_dir = claude_dir / "rules"
    rules_dir.mkdir(exist_ok=True)
    print("\n   📦 Rules...")
    for rule_file in ("athena-session.md", "athena-framework.md"):
        _copy_file(
            _CLAUDE_TEMPLATES / "rules" / rule_file,
            rules_dir / rule_file,
            f".claude/rules/{rule_file}",
        )

    # 6. .mcp.json (Athena MCP server)
    _copy_file(
        _CLAUDE_TEMPLATES / "mcp.json",
        root / ".mcp.json",
        ".mcp.json (Athena MCP server)",
    )
