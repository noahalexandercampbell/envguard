from __future__ import annotations

from envguard.models import EnvDiff


def render_diff_table(diff: EnvDiff) -> str:
    lines = []
    if diff.missing:
        lines.append("# Missing")
        for name in diff.missing:
            lines.append(f"- {name}")
        lines.append("")
    if diff.extra:
        lines.append("# Extra")
        for name in diff.extra:
            lines.append(f"- {name}")
        lines.append("")
    if diff.blank:
        lines.append("# Blank")
        for name in diff.blank:
            lines.append(f"- {name}")
        lines.append("")
    if not lines:
        lines.append("# All required variables are present")
    return "\n".join(lines)
