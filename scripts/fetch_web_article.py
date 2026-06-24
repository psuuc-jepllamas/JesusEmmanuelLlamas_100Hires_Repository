#!/usr/bin/env python3
"""Fetch a blog/article page and save the main content as Markdown.

The script prefers the `trafilatura` library when it is installed because it is
very good at isolating the main article text from a webpage. If that library is
not available, it falls back to a small standard-library extractor so the script
still works in a pinch.
"""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "research" / "other"


@dataclass(frozen=True)
class ArticleMetadata:
    title: str | None
    author: str | None
    published_date: str | None
    source_url: str


def slugify(value: str, fallback: str) -> str:
    """Make a filesystem-friendly slug while keeping it readable."""
    cleaned = re.sub(r"[^\w\s.-]", "", value, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", "-", cleaned.strip())
    cleaned = cleaned.strip(".-_")
    return cleaned or fallback


def fetch_html(url: str) -> str:
    """Download a webpage with a browser-like user agent."""
    request = Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/126.0.0.0 Safari/537.36"
            )
        },
    )
    with urlopen(request, timeout=30) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")


def html_to_text(html_text: str) -> str:
    """Flatten HTML into readable plain text for metadata fallbacks."""

    class TextOnlyParser(HTMLParser):
        block_tags = {"article", "div", "footer", "h1", "h2", "h3", "h4", "h5", "h6", "header", "li", "main", "p", "section", "tr"}
        skip_tags = {"script", "style", "noscript"}

        def __init__(self) -> None:
            super().__init__()
            self.parts: list[str] = []
            self._skip_depth = 0

        def handle_starttag(self, tag: str, attrs) -> None:
            if tag in self.skip_tags:
                self._skip_depth += 1
            elif tag in self.block_tags:
                self.parts.append("\n")

        def handle_endtag(self, tag: str) -> None:
            if tag in self.skip_tags and self._skip_depth > 0:
                self._skip_depth -= 1
            elif tag in self.block_tags:
                self.parts.append("\n")

        def handle_data(self, data: str) -> None:
            if self._skip_depth > 0:
                return
            text = html.unescape(data).strip()
            if text:
                self.parts.append(text)

    parser = TextOnlyParser()
    parser.feed(html_text)
    text = re.sub(r"[\t\r ]+", " ", " ".join(parser.parts))
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text


def normalize_published_date(value: str) -> str | None:
    """Normalize loose date strings into the repo's date style when possible."""
    cleaned = re.sub(r"\s+", " ", html.unescape(value)).strip().strip(".,")
    if not cleaned:
        return None

    formats = [
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S.%f%z",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d",
        "%b %d, %Y",
        "%B %d, %Y",
        "%d %b %Y",
        "%d %B %Y",
        "%b %d",
        "%B %d",
        "%d %b",
        "%d %B",
    ]

    for fmt in formats:
        try:
            parsed = datetime.strptime(cleaned, fmt)
        except ValueError:
            continue
        if "%Y" not in fmt:
            parsed = parsed.replace(year=datetime.now().year)
        return parsed.strftime("%d %b %Y")

    return cleaned


def extract_published_date(html_text: str) -> str | None:
    """Find a publish date from meta tags or visible page text."""
    meta_patterns = [
        r'<meta\s+[^>]*(?:name|property)=["\']article:published_time["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
        r'<meta\s+[^>]*(?:name|property)=["\']date["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
        r'<meta\s+[^>]*(?:name|property)=["\']pubdate["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
        r'<meta\s+[^>]*(?:name|property)=["\']publish_date["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
        r'<meta\s+[^>]*(?:name|property)=["\']timestamp["\'][^>]*content=["\']([^"\']+)["\'][^>]*>',
    ]
    for pattern in meta_patterns:
        match = re.search(pattern, html_text, flags=re.I)
        if match:
            return normalize_published_date(match.group(1))

    visible_text = html_to_text(html_text)
    visible_patterns = [
        r'Published:\s*([A-Z][a-z]{2,8}\s+\d{1,2}(?:,\s*\d{4})?)',
        r'Published:\s*(\d{1,2}\s+[A-Z][a-z]{2,8}(?:\s+\d{4})?)',
        r'Updated:\s*([A-Z][a-z]{2,8}\s+\d{1,2}(?:,\s*\d{4})?)',
        r'Date:\s*([A-Z][a-z]{2,8}\s+\d{1,2}(?:,\s*\d{4})?)',
        r'Date:\s*(\d{1,2}\s+[A-Z][a-z]{2,8}(?:\s+\d{4})?)',
    ]
    for pattern in visible_patterns:
        match = re.search(pattern, visible_text, flags=re.I)
        if match:
            return normalize_published_date(match.group(1))

    return None


def extract_metadata(html_text: str, url: str) -> ArticleMetadata:
    """Extract title, author, and publish date from common meta tags."""
    title = None
    author = None
    published_date = extract_published_date(html_text)

    title_match = re.search(r"<title[^>]*>(.*?)</title>", html_text, flags=re.I | re.S)
    if title_match:
        title = html.unescape(re.sub(r"\s+", " ", title_match.group(1))).strip()

    meta_pattern = re.compile(
        r'<meta\s+[^>]*(?:name|property)=["\']([^"\']+)["\'][^>]*content=["\']([^"\']*)["\'][^>]*>',
        flags=re.I,
    )
    for key, value in meta_pattern.findall(html_text):
        key_lower = key.lower().strip()
        value_clean = html.unescape(value.strip())
        if not author and key_lower in {"author", "article:author", "og:author", "twitter:creator"}:
            author = value_clean or None
        if not published_date and key_lower in {
            "article:published_time",
            "article:modified_time",
            "og:updated_time",
            "date",
            "pubdate",
            "publish_date",
            "timestamp",
        }:
            published_date = normalize_published_date(value_clean)

    if title:
        title = re.sub(r"\s*\|\s*.*$", "", title).strip()

    return ArticleMetadata(
        title=title,
        author=author,
        published_date=published_date,
        source_url=url,
    )


def extract_with_trafilatura(html_text: str) -> str | None:
    """Try the best available article extractor first."""
    try:
        import trafilatura
    except ImportError:
        return None

    extracted = trafilatura.extract(
        html_text,
        include_comments=False,
        include_tables=True,
        favor_precision=True,
        output_format="txt",
    )
    if extracted:
        return extracted.strip()
    return None


def extract_with_stdlib(html_text: str) -> str:
    """Minimal fallback extractor when no third-party parser is installed."""

    class TextCollector(HTMLParser):
        block_tags = {
            "article",
            "aside",
            "div",
            "footer",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "header",
            "li",
            "main",
            "p",
            "section",
            "tr",
        }

        skip_tags = {"script", "style", "noscript"}

        def __init__(self) -> None:
            super().__init__()
            self.parts: list[str] = []
            self._skip_depth = 0

        def handle_starttag(self, tag: str, attrs) -> None:
            if tag in self.skip_tags:
                self._skip_depth += 1
            elif tag in self.block_tags and self.parts and self.parts[-1] != "":
                self.parts.append("")

        def handle_endtag(self, tag: str) -> None:
            if tag in self.skip_tags and self._skip_depth > 0:
                self._skip_depth -= 1
            elif tag in self.block_tags and self.parts and self.parts[-1] != "":
                self.parts.append("")

        def handle_data(self, data: str) -> None:
            if self._skip_depth > 0:
                return
            text = html.unescape(data).strip()
            if text:
                self.parts.append(text)

    collector = TextCollector()
    collector.feed(html_text)

    lines: list[str] = []
    for part in collector.parts:
        if part == "":
            if lines and lines[-1] != "":
                lines.append("")
            continue
        lines.append(part)

    cleaned_lines: list[str] = []
    previous_blank = False
    for line in lines:
        if line == "":
            if not previous_blank:
                cleaned_lines.append("")
            previous_blank = True
        else:
            cleaned_lines.append(line)
            previous_blank = False

    return "\n".join(cleaned_lines).strip()


def extract_article_text(html_text: str) -> str:
    extracted = extract_with_trafilatura(html_text)
    if extracted:
        return extracted
    return extract_with_stdlib(html_text)


def build_markdown(metadata: ArticleMetadata, body_text: str) -> str:
    title = metadata.title or metadata.source_url
    header = f"# {title}\n\n"

    meta_lines = [f"- Source: {metadata.source_url}"]
    if metadata.published_date:
        meta_lines.append(f"- Date: {metadata.published_date}")
    if metadata.author:
        meta_lines.append(f"- Author: {metadata.author}")

    return (
        header
        + "\n".join(meta_lines)
        + "\n\n"
        "## Transcript\n\n"
        + body_text.strip()
        + "\n"
    )


def output_path_for(url: str, metadata: ArticleMetadata, output_root: Path) -> Path:
    parsed = urlparse(url)
    host_slug = slugify(parsed.netloc.removeprefix("www.") or "website", "website")
    source_title = metadata.title or parsed.path.strip("/") or "article"
    file_slug = slugify(source_title, "article")
    return output_root / host_slug / f"{file_slug}.md"


def resolve_repo_path(path: Path) -> Path:
    """Resolve relative paths against the repository root, not the current cwd."""
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a blog post or article and save it as Markdown.",
    )
    parser.add_argument("url", help="Webpage URL to extract")
    parser.add_argument(
        "--output",
        type=Path,
        help="Exact output file path. If omitted, the script chooses a path under research/other.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Root directory used when --output is not provided. Default: {DEFAULT_OUTPUT_ROOT}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        html_text = fetch_html(args.url)
        metadata = extract_metadata(html_text, args.url)
        body_text = extract_article_text(html_text)
    except (HTTPError, URLError, OSError) as error:
        print(f"Error: could not fetch the webpage. {error}", file=sys.stderr)
        return 1

    if not body_text.strip():
        print("Error: no article text could be extracted from the page.", file=sys.stderr)
        return 1

    markdown = build_markdown(metadata, body_text)

    if args.output:
        output_path = resolve_repo_path(args.output)
    else:
        output_path = output_path_for(args.url, metadata, resolve_repo_path(args.output_root))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Success: article saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
