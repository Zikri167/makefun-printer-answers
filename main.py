"""The Printer Finally Answers -- make.fun entry.

Writes a single line of printer-voice text to entry.txt in the output
directory. Standard library only. No file reads, no network, no clock,
no randomness.
"""

import os

ENTRY = "I have printed 41,209 sheets for you, and not one of them was a thank-you note."

OUTPUT_FILENAME = "entry.txt"

_ENV_VARS = ("OUTPUT_DIR", "_OUTPUT_DIR", "MAKEFUN_OUTPUT_DIR")


def validate(entry: str) -> None:
    """ENTRY must be one non-empty line of 1-240 characters."""
    if not isinstance(entry, str):
        raise TypeError("ENTRY must be a string")
    if not entry:
        raise ValueError("ENTRY must not be empty")
    if not entry.strip():
        raise ValueError("ENTRY must not be only whitespace")
    if entry != entry.strip():
        raise ValueError("ENTRY must not have leading or trailing whitespace")
    if len(entry) > 240:
        raise ValueError(f"ENTRY is {len(entry)} characters; maximum is 240")
    if "\n" in entry or "\r" in entry:
        raise ValueError("ENTRY must be exactly one line")


def find_output_dir() -> str:
    """Resolve the output directory: env vars first, then /output, ./output, ."""
    for var in _ENV_VARS:
        value = os.environ.get(var)
        if value and value.strip():
            return value.strip()
    for candidate in ("/output", "./output", "."):
        if os.path.isdir(candidate):
            return candidate
    return "."


def main() -> None:
    validate(ENTRY)
    out_dir = find_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_FILENAME)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    with open(path, "r", encoding="utf-8", newline="") as f:
        written = f.read()
    assert written == ENTRY, "entry.txt does not match ENTRY"
    assert "\n" not in written, "entry.txt must be a single line"
    # No trailing newline: the file must be exactly ENTRY, byte for byte.
    assert os.path.getsize(path) == len(ENTRY.encode("utf-8")), (
        "entry.txt byte size does not match ENTRY"
    )


if __name__ == "__main__":
    main()
