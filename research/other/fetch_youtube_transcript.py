#!/usr/bin/env python3d
"""Fetch a YouTube transcript and save it as Markdown."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError
from urllib.parse import parse_qs, quote, urlparse
from urllib.request import urlopen

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    CouldNotRetrieveTranscript,
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
)


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "youtube-transcripts"
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


@dataclass(frozen=True)
class VideoMetadata:
    title: str | None
    channel_name: str | None


def extract_video_id(value: str) -> str:
    """Return the video ID from a YouTube URL or raw 11-character ID."""
    raw = value.strip()
    if VIDEO_ID_RE.match(raw):
        return raw

    parsed = urlparse(raw)
    host = parsed.netloc.lower().removeprefix("www.")

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        query_id = parse_qs(parsed.query).get("v", [None])[0]
        if query_id and VIDEO_ID_RE.match(query_id):
            return query_id

        parts = [part for part in parsed.path.split("/") if part]
        for prefix in ("shorts", "embed", "live"):
            if len(parts) >= 2 and parts[0] == prefix and VIDEO_ID_RE.match(parts[1]):
                return parts[1]

    if host == "youtu.be":
        video_id = parsed.path.strip("/").split("/")[0]
        if VIDEO_ID_RE.match(video_id):
            return video_id

    raise ValueError("Input must be a valid YouTube video URL or 11-character video ID.")


def slugify(value: str, fallback: str) -> str:
    """Make a filesystem-friendly name while keeping it readable."""
    cleaned = re.sub(r"[^\w\s.-]", "", value, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", "-", cleaned.strip())
    cleaned = cleaned.strip(".-_")
    return cleaned or fallback


def fetch_metadata(video_id: str) -> VideoMetadata:
    """Fetch public title/channel metadata without an API key."""
    oembed_url = (
        "https://www.youtube.com/oembed"
        f"?url={quote(f'https://www.youtube.com/watch?v={video_id}', safe='')}"
        "&format=json"
    )

    try:
        with urlopen(oembed_url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, json.JSONDecodeError):
        return VideoMetadata(title=None, channel_name=None)

    return VideoMetadata(
        title=payload.get("title"),
        channel_name=payload.get("author_name"),
    )


def fetch_transcript_text(video_id: str, languages: list[str]) -> str:
    fetched_transcript = YouTubeTranscriptApi().fetch(video_id, languages=languages)
    lines = [snippet.text.strip() for snippet in fetched_transcript if snippet.text.strip()]
    return "\n".join(lines)


def build_markdown(video_id: str, metadata: VideoMetadata, transcript_text: str) -> str:
    title = metadata.title or video_id
    channel = metadata.channel_name or "Unknown Channel"

    return (
        f"# {title}\n\n"
        f"- Video ID: `{video_id}`\n"
        f"- Channel: {channel}\n"
        f"- URL: https://www.youtube.com/watch?v={video_id}\n\n"
        "## Transcript\n\n"
        f"{transcript_text}\n"
    )


def save_transcript(video_id: str, metadata: VideoMetadata, transcript_text: str, output_root: Path) -> Path:
    channel_dir = output_root / slugify(metadata.channel_name or "unknown-channel", "unknown-channel")
    channel_dir.mkdir(parents=True, exist_ok=True)

    file_stem = slugify(metadata.title or video_id, video_id)
    output_path = channel_dir / f"{file_stem}.md"
    output_path.write_text(build_markdown(video_id, metadata, transcript_text), encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube transcript and save it to research/youtube-transcripts.",
    )
    parser.add_argument("video", help="YouTube video URL or 11-character video ID")
    parser.add_argument(
        "--languages",
        nargs="+",
        default=["en"],
        help="Preferred transcript language codes in priority order. Default: en",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=DEFAULT_OUTPUT_ROOT,
        help=f"Directory for transcript folders. Default: {DEFAULT_OUTPUT_ROOT}",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    try:
        video_id = extract_video_id(args.video)
        metadata = fetch_metadata(video_id)
        transcript_text = fetch_transcript_text(video_id, args.languages)
        output_path = save_transcript(video_id, metadata, transcript_text, args.output_root)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    except (NoTranscriptFound, TranscriptsDisabled, VideoUnavailable, CouldNotRetrieveTranscript) as error:
        print(f"Error: transcript unavailable for this video. {error}", file=sys.stderr)
        return 1

    print(f"Success: transcript saved to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
