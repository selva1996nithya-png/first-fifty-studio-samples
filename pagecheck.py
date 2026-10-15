#!/usr/bin/env python3
"""Small, source-only HTML checker. Standard library only; no accounts or API costs."""
import argparse
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from urllib.request import Request, urlopen


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = []
        self.in_title = False
        self.meta = {}
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.in_title = True
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        if tag == "meta":
            self.meta[(attrs.get("name") or "").lower()] = attrs.get("content") or ""
        if tag == "a" and attrs.get("href") is not None:
            self.links.append((attrs["href"], self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, value):
        if self.in_title:
            self.title.append(value)


def inspect(html):
    page = Page()
    page.feed(html)
    findings = []
    for condition, issue, fix in [
        (not "".join(page.title).strip(), "Missing or blank page title", "Add an accurate title naming the business and service."),
        (not page.meta.get("description", "").strip(), "No nonempty meta description in source", "Write an accurate page summary. This does not guarantee a search snippet or ranking."),
        (not page.meta.get("viewport", "").strip(), "No viewport declaration in source", "Check mobile rendering, then add an appropriate viewport declaration if needed."),
    ]:
        if condition:
            findings.append({"issue": issue, "fix": fix})
    for href, line in page.links:
        if href.startswith("#") and len(href) > 1 and unquote(href[1:]) not in page.ids:
            findings.append({"issue": f"Fragment target absent from source: {href}", "line": line,
                             "fix": "Check in a browser; repair the target or link if JavaScript does not provide it."})
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--file", type=Path)
    source.add_argument("--url")
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        if args.file:
            html = args.file.read_text(encoding="utf-8-sig")
            location = str(args.file)
        else:
            parts = urlsplit(args.url)
            if parts.scheme not in {"http", "https"} or not parts.hostname or parts.username or parts.password:
                parser.error("Use a public http(s) URL without credentials.")
            request = Request(args.url, headers={"User-Agent": "PageCheck/1.0 (single-page HTML review)"})
            with urlopen(request, timeout=15) as response:
                if response.headers.get_content_type() != "text/html":
                    parser.error("The URL did not return HTML. No findings were generated.")
                raw = response.read(2_000_001)
                if len(raw) > 2_000_000:
                    parser.error("Page exceeds the 2 MB limit. No findings were generated.")
                html = raw.decode(response.headers.get_content_charset() or "utf-8", errors="replace")
                location = response.url
        report = {"source": location, "checked_at": datetime.now(timezone.utc).isoformat(),
                  "scope": "Initial HTML only. Findings require browser confirmation. No JavaScript, forms, payments, accessibility audit, or performance test.",
                  "findings": inspect(html)}
        output = json.dumps(report, indent=2, ensure_ascii=False) + "\n"
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(output, encoding="utf-8")
        print(output, end="")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Could not inspect page: {error}\n")


if __name__ == "__main__":
    main()
