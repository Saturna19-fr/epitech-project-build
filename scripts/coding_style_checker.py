#!/usr/bin/env python3

import re
import sys

DIAG_RE = re.compile(
    r"^(?P<file>[^:\s][^:]+\.(?:c|h))"
    r":(?P<line>\d+)"
    r":(?P<col>\d+)"
    r":\s*(?P<level>warning|error|note)"
    r":\s*(?P<message>.+)$"
)


def sanitize_annotation_message(message: str) -> str:
    return message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def annotate(level: str, filename: str, line: str, col: str, message: str) -> str:
    ghlevel = {"error": "error", "warning": "warning"}.get(level, "notice")
    msg = sanitize_annotation_message(message=message)
    return f"::{ghlevel} file={filename},line={line},col={col}::{msg}"


def strip_brackets(message: str) -> str:
    return re.sub(r"^(\[.*?\]\s*)+", "", message).strip()


def main():
    counter = {"warning": 0, "error": 0}

    for raw_line in sys.stdin:
        line = raw_line.rstrip()
        m = DIAG_RE.match(line)
        if m:
            level = m.group("level")
            filepath = m.group("file")
            lineno = m.group("line")
            col = m.group("col")
            message = strip_brackets(m.group("message").strip())

            print(annotate(level, filepath, lineno, col, message))

            if level in counter:
                counter[level] += 1

    total = counter["warning"] + counter["error"]
    if total:
        summary = f"{counter['error']} errors, {counter['warning']} warnings."
        print(f"::notice::{summary}")
    else:
        print("::notice::No warnings or errors found.")


if __name__ == "__main__":
    main()
