#!/usr/bin/env python3
"""Validate an HTML fragment for conservative WeChat editor compatibility."""

from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path


BANNED_TAGS = {
    "script", "style", "link", "iframe", "form", "input", "button",
    "video", "audio", "canvas", "object", "embed", "textarea", "select",
}
TEXT_TAGS = {"p", "span", "section", "div", "blockquote", "li", "strong", "em"}


class FragmentInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.errors: list[dict[str, str]] = []
        self.warnings: list[dict[str, str]] = []
        self.tags: dict[str, int] = {}
        self.text_parts: list[str] = []
        self.inline_styled_text_tags = 0
        self.text_tags = 0
        self.image_count = 0

    def issue(self, severity: str, code: str, message: str) -> None:
        target = self.errors if severity == "error" else self.warnings
        target.append({"code": code, "message": message})

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        self.tags[tag] = self.tags.get(tag, 0) + 1
        attr = {key.lower(): value or "" for key, value in attrs}

        if tag in BANNED_TAGS:
            self.issue("error", "banned-tag", f"Remove <{tag}> from the article fragment.")

        for key, value in attr.items():
            if key.startswith("on"):
                self.issue("error", "event-handler", f"Remove JavaScript attribute {key} from <{tag}>.")
            if key in {"class", "id"}:
                self.issue("warning", "selector-dependency", f"<{tag}> uses {key}; the final fragment should not depend on selectors.")
            if key in {"href", "src"} and value.strip().lower().startswith("javascript:"):
                self.issue("error", "javascript-url", f"Remove JavaScript URL from <{tag}>.")

        style = attr.get("style", "").lower()
        if tag in TEXT_TAGS:
            self.text_tags += 1
            if style:
                self.inline_styled_text_tags += 1

        fragile_patterns = {
            "css-variable": r"var\s*\(",
            "viewport-unit": r"\d(?:vw|vh|vmin|vmax)\b",
            "interactive-css": r"(?:animation|transition)\s*:",
            "sticky-position": r"position\s*:\s*(?:fixed|sticky)",
        }
        for code, pattern in fragile_patterns.items():
            if re.search(pattern, style):
                self.issue("warning", code, f"<{tag}> contains fragile CSS: {code}.")

        if tag == "img":
            self.image_count += 1
            src = attr.get("src", "").strip()
            alt = attr.get("alt", "").strip()
            if not src:
                self.issue("error", "missing-image-src", "An <img> element has no src.")
            elif src.startswith(("/", "file:", "../", "./")):
                self.issue("warning", "local-image", f"Image source is preview-only and must be uploaded before publishing: {src}")
            elif src.startswith("http://"):
                self.issue("warning", "insecure-image", f"Prefer an uploaded or HTTPS image source: {src}")
            if not alt:
                self.issue("warning", "missing-image-alt", "Add meaningful alt text to every image.")
            required = ("width:100%", "max-width:100%", "height:auto", "display:block")
            normalized = style.replace(" ", "")
            missing = [item for item in required if item not in normalized]
            if missing:
                self.issue("warning", "responsive-image", "Image style should include width:100%; max-width:100%; height:auto; display:block.")

    def handle_data(self, data: str) -> None:
        if data.strip():
            self.text_parts.append(data.strip())


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="HTML article fragment to validate")
    parser.add_argument("--json", dest="json_path", type=Path, help="Write the report as JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not args.input.is_file():
        print(f"ERROR: file not found: {args.input}", file=sys.stderr)
        return 2

    source = args.input.read_text(encoding="utf-8")
    inspector = FragmentInspector()
    try:
        inspector.feed(source)
        inspector.close()
    except Exception as exc:  # HTMLParser can surface malformed entities or nesting edge cases.
        inspector.issue("error", "parse-failure", f"Could not parse HTML: {exc}")

    readable_text = "".join(inspector.text_parts)
    if len(readable_text) < 30:
        inspector.issue("error", "too-little-text", "The article contains less than 30 readable characters.")
    if not any(tag in inspector.tags for tag in ("h1", "h2")):
        inspector.issue("warning", "missing-heading", "No h1 or h2 heading was found; confirm title hierarchy visually.")
    if inspector.text_tags and inspector.inline_styled_text_tags / inspector.text_tags < 0.5:
        inspector.issue("warning", "sparse-inline-styles", "Fewer than half of text containers have inline styles.")

    report = {
        "file": str(args.input.resolve()),
        "valid": not inspector.errors,
        "summary": {
            "errors": len(inspector.errors),
            "warnings": len(inspector.warnings),
            "characters": len(readable_text),
            "images": inspector.image_count,
        },
        "errors": inspector.errors,
        "warnings": inspector.warnings,
    }

    if args.json_path:
        args.json_path.parent.mkdir(parents=True, exist_ok=True)
        args.json_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    status = "PASS" if report["valid"] else "FAIL"
    print(f"{status}: {report['summary']['errors']} error(s), {report['summary']['warnings']} warning(s), "
          f"{report['summary']['characters']} text character(s), {report['summary']['images']} image(s)")
    for issue in inspector.errors:
        print(f"ERROR [{issue['code']}] {issue['message']}")
    for issue in inspector.warnings:
        print(f"WARN  [{issue['code']}] {issue['message']}")
    return 0 if report["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
