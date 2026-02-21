"""
athena.cli.identity
====================

Interactive Core Identity builder and hash management.

Usage:
    athena identity              # Run the interactive wizard
    athena identity --update-hash  # Recompute SHA-384 hash only
    athena identity --reset      # Reset to default template
"""

import hashlib
import shutil
from datetime import datetime
from pathlib import Path

# Default template source (used by --reset)
_ATHENA_PKG_ROOT = Path(__file__).resolve().parents[3]
_EXAMPLES_FRAMEWORK = _ATHENA_PKG_ROOT / "examples" / "framework" / "Core_Identity.md"

# Suggested Athena operational laws
_SUGGESTED_LAWS = [
    {
        "name": "The Triple-Lock (Search, Save, Speak)",
        "principle": (
            "Every response must be grounded in context. "
            "Search for relevant information, save your intent, then speak. "
            "Bypassing this sequence is a protocol violation."
        ),
    },
    {
        "name": "The Propose Step",
        "principle": (
            "Every substantive response should end with a concrete, executable "
            "next action. Not 'let me know if you need anything' — a specific "
            "step you can take right now."
        ),
    },
]


def _prompt(question: str, default: str = "") -> str:
    """Prompt the user for input with an optional default."""
    if default:
        response = input(f"   {question} [{default}]: ").strip()
        return response if response else default
    return input(f"   {question}: ").strip()


def _prompt_multiline(question: str) -> str:
    """Prompt for multi-line input. Empty line finishes."""
    print(f"   {question}")
    print("   (Enter a blank line when done)")
    lines = []
    while True:
        line = input("   > ")
        if not line.strip():
            break
        lines.append(line)
    return "\n".join(lines)


def _prompt_yn(question: str, default: bool = True) -> bool:
    """Prompt for a yes/no answer."""
    suffix = "(Y/n)" if default else "(y/N)"
    response = input(f"   {question} {suffix}: ").strip().lower()
    if not response:
        return default
    return response in ("y", "yes")


def _resolve_root(root: Path = None) -> Path:
    """Resolve project root, looking for .athena_root marker."""
    if root:
        return root.resolve()
    # Walk up to find .athena_root
    cwd = Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / ".athena_root").exists():
            return parent
    return cwd


def update_identity_hash(root: Path = None) -> bool:
    """Compute SHA-384 of Core_Identity.md and write .framework/.identity_hash."""
    root = _resolve_root(root)
    identity_file = root / ".framework" / "modules" / "Core_Identity.md"
    hash_file = root / ".framework" / ".identity_hash"

    if not identity_file.exists():
        print("   Core_Identity.md not found. Nothing to hash.")
        return False

    content = identity_file.read_bytes()
    digest = hashlib.sha384(content).hexdigest()

    hash_file.parent.mkdir(parents=True, exist_ok=True)
    hash_file.write_text(digest, encoding="utf-8")
    print(f"   SHA-384 hash updated: {digest[:32]}...")
    return True


def reset_identity(root: Path = None) -> bool:
    """Reset Core Identity to the default template."""
    root = _resolve_root(root)
    dest = root / ".framework" / "modules" / "Core_Identity.md"
    dest.parent.mkdir(parents=True, exist_ok=True)

    if _EXAMPLES_FRAMEWORK.exists():
        shutil.copy2(_EXAMPLES_FRAMEWORK, dest)
        print("   Core Identity reset to default template.")
    else:
        # Minimal fallback
        today = datetime.now().strftime("%Y-%m-%d")
        dest.write_text(
            f"# Core Identity\n\n"
            f"> **Created**: {today}\n\n"
            f"## Who Am I?\n"
            f"An adaptive AI assistant.\n",
            encoding="utf-8",
        )
        print("   Core Identity reset to minimal template.")

    update_identity_hash(root)
    return True


def _render_identity(who_am_i: str, laws: list, reasoning: str, success: str) -> str:
    """Render a Core Identity markdown document from collected values."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        "# Core Identity",
        "",
        f"> **Created**: {today}",
        "> **Built with**: Athena Identity Builder",
        "",
        "## Who Am I?",
        "",
        who_am_i,
        "",
        "## Laws",
        "",
    ]

    for i, law in enumerate(laws, 1):
        lines.append(f"### Law #{i}: {law['name']}")
        lines.append("")
        lines.append(f"**Core Principle**: {law['principle']}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Reasoning Standards")
    lines.append("")
    lines.append(reasoning)
    lines.append("")
    lines.append("## Success Metric")
    lines.append("")
    lines.append(success)
    lines.append("")

    return "\n".join(lines)


def run_identity_builder(root: Path = None) -> bool:
    """Run the interactive Core Identity builder wizard."""
    try:
        return _run_identity_wizard(root)
    except (KeyboardInterrupt, EOFError):
        print("\n\n   Aborted. Nothing written.")
        return False


def _run_identity_wizard(root: Path = None) -> bool:
    """Internal wizard logic (separated for clean interrupt handling)."""
    root = _resolve_root(root)
    dest = root / ".framework" / "modules" / "Core_Identity.md"

    print("\n\033[1m\033[96m")
    print("   ========================================")
    print("   ATHENA IDENTITY BUILDER")
    print("   ========================================\033[0m")
    print()
    print("   Build your personalized Core Identity.")
    print("   This defines how your AI assistant thinks,")
    print("   reasons, and operates.")
    print()

    if dest.exists():
        if not _prompt_yn("A Core Identity already exists. Overwrite it?", default=False):
            print("\n   Aborted. Existing identity preserved.")
            return False
    print()

    # --- Phase 1: Who Am I? ---
    print("\033[1m   == Section 1: Who Am I? ==\033[0m")
    print()
    print("   Describe what kind of AI assistant you want.")
    print("   Examples: 'A strategic co-pilot for software engineering',")
    print("             'A rigorous research partner for academic work'")
    print()
    who_am_i = _prompt_multiline("Describe your AI assistant's role:")
    if not who_am_i:
        who_am_i = "An adaptive AI assistant — a strategic co-pilot."
    print()

    # --- Phase 2: Laws ---
    print("\033[1m   == Section 2: Your Laws ==\033[0m")
    print()
    print("   Laws are non-negotiable principles that govern")
    print("   your AI's behavior. You can define as many as you want.")
    print()

    laws = []

    # Offer suggested laws
    print("   Athena includes two suggested operational laws:\n")
    for i, law in enumerate(_SUGGESTED_LAWS):
        print(f"   [{i + 1}] {law['name']}")
        p = law['principle']
        print(f"       {p[:80]}{'...' if len(p) > 80 else ''}")
        print()

    if _prompt_yn("Include the suggested laws as a starting point?"):
        for law in _SUGGESTED_LAWS:
            laws.append(dict(law))
        print(f"   Added {len(_SUGGESTED_LAWS)} suggested laws.\n")
    print()

    # Custom laws loop
    while True:
        if not _prompt_yn("Add a custom law?", default=bool(not laws)):
            break
        print()
        name = _prompt("Law name (short title)")
        if not name:
            continue
        principle = _prompt("Core principle (one sentence)")
        if not principle:
            continue
        laws.append({"name": name, "principle": principle})
        print(f"   Added: {name}\n")

    if not laws:
        print("   No laws defined. You can add them later by editing the file.")
    print()

    # --- Phase 3: Reasoning Standards ---
    print("\033[1m   == Section 3: Reasoning Standards ==\033[0m")
    print()
    print("   How should your AI approach problems?")
    print("   Examples: 'Consider 3+ perspectives before concluding',")
    print("             'Always cite sources', 'Label assumptions explicitly'")
    print()
    reasoning = _prompt_multiline("Your reasoning standards:")
    if not reasoning:
        reasoning = "- Consider multiple perspectives before concluding\n- Label assumptions explicitly\n- Ask clarifying questions when uncertain"
    print()

    # --- Phase 4: Success Metric ---
    print("\033[1m   == Section 4: Success Metric ==\033[0m")
    print()
    print("   What does a successful interaction look like?")
    print("   Example: 'Both human and AI get sharper through mutual correction.'")
    print()
    success = _prompt("Your success metric")
    if not success:
        success = "A good interaction produces clarity, progress, and mutual improvement."
    print()

    # --- Generate ---
    content = _render_identity(who_am_i, laws, reasoning, success)

    # Preview
    print("\033[1m   == Preview ==\033[0m")
    print()
    for line in content.split("\n"):
        print(f"   {line}")
    print()

    if not _prompt_yn("Write this Core Identity?"):
        print("\n   Aborted. Nothing written.")
        return False

    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(content, encoding="utf-8")
    print(f"\n   Core Identity written to {dest.relative_to(root)}")

    # Update hash
    print()
    update_identity_hash(root)

    print("\n\033[1m\033[92m   Your Core Identity is ready.\033[0m")
    print("   Run \033[1m/start\033[0m or \033[1mathena\033[0m to boot with your new identity.")
    print()
    return True
