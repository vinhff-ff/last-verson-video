"""
designer.py - Phase 3 (step 3)

Maps the script lines (10-15) to a Scene JSON. Each line is either:
  - a plain string  -> fallback: deterministic fixed template by index (legacy)
  - a dict {"char": "A"|"B"|"both", "text": "..."} -> visuals follow the tag,
    so the character points at exactly the person that line talks about.
    This supports both block-style scripts (all-A then all-B) and alternating
    A/B comparison lines, whichever the external AI chose. No cart character.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Legacy index-based template (used only when lines are plain strings).
def _visual_for(index: int, total: int) -> dict:
    if index == 0:
        return {"image": "A",    "character": "pointLeftUp", "animation": "showA"}
    if index == 1:
        return {"image": "B",    "character": "pointRight",  "animation": "showB"}
    if index == 2:
        return {"image": "both", "character": "confused",    "animation": "compare"}
    if index % 2 == 1:
        return {"image": "A",    "character": "pointLeft",   "animation": "showA"}
    return {"image": "B",    "character": "pointRight",  "animation": "showB"}


def _visual_for_char(char: str, first_a: bool, first_b: bool) -> dict:
    if char == "both":
        return {"image": "both", "character": "confused", "animation": "compare"}
    if char == "A":
        pose = "pointLeftUp" if first_a else "pointLeft"
        return {"image": "A", "character": pose, "animation": "showA"}
    if char == "B":
        return {"image": "B", "character": "pointRight", "animation": "showB"}
    raise ValueError(f"Invalid char label {char!r} (expected A/B/both)")


DEFAULT_DURATION = 4  # placeholder only; TTS measures & overwrites real durations

MIN_LINES = 10
MAX_LINES = 15


def design_scenes(script_lines: list) -> dict:
    """Attach visual directives to each script line -> Scene JSON.

    Accepts 10-15 lines. Each line is a string (legacy index template) or a
    dict {"char", "text"} (content-driven visuals).
    """
    if not (MIN_LINES <= len(script_lines) <= MAX_LINES):
        raise ValueError(
            f"Script has {len(script_lines)} lines, expected between "
            f"{MIN_LINES} and {MAX_LINES}"
        )

    scenes = []
    total = len(script_lines)
    all_strings = all(isinstance(ln, str) for ln in script_lines)

    if all_strings:
        for index, line in enumerate(script_lines):
            visuals = _visual_for(index, total)
            scenes.append({**visuals, "text": line, "duration": DEFAULT_DURATION})
    else:
        first_a = first_b = True
        for item in script_lines:
            if not isinstance(item, dict):
                raise ValueError(
                    "Each script line must be either a string or a dict "
                    '{"char": "A"|"B"|"both", "text": "..."}'
                )
            char = str(item.get("char", "")).strip()
            text = item.get("text")
            if char not in ("A", "B", "both"):
                raise ValueError(f"Invalid char {char!r} (expected A/B/both)")
            if not isinstance(text, str) or not text.strip():
                raise ValueError("Missing non-empty 'text' in script line")
            visuals = _visual_for_char(char, first_a, first_b)
            if char == "A":
                first_a = False
            elif char == "B":
                first_b = False
            scenes.append({**visuals, "text": text.strip(), "duration": DEFAULT_DURATION})

    return {"duration": DEFAULT_DURATION * len(scenes), "scenes": scenes}