from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path


API_BASE = "https://api.buttondown.com/v1"
SITE_NAME = "munyachipunza.com"
DEFAULT_FEED = Path(__file__).resolve().parents[1] / "blog-feed.xml"


@dataclass(frozen=True)
class FeedItem:
    title: str
    description: str
    link: str
    guid: str


def normalize_url(value: str) -> str:
    return value.strip().rstrip("/")


def item_text(item: ET.Element, tag: str) -> str:
    element = item.find(tag)
    return (element.text or "").strip() if element is not None else ""


def latest_feed_item(feed_path: Path) -> FeedItem:
    tree = ET.parse(feed_path)
    item = tree.find("./channel/item")
    if item is None:
        raise RuntimeError(f"No RSS items found in {feed_path}")

    return FeedItem(
        title=item_text(item, "title"),
        description=item_text(item, "description"),
        link=item_text(item, "link"),
        guid=item_text(item, "guid") or item_text(item, "link"),
    )


def request_json(method: str, path: str, api_key: str, payload: dict | None = None) -> dict:
    body = None
    headers = {
        "Authorization": f"Token {api_key}",
        "Content-Type": "application/json",
        "X-Buttondown-Live-Dangerously": "true",
    }
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(f"{API_BASE}{path}", data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Buttondown API returned {error.code}: {details}") from error

    return json.loads(raw) if raw else {}


def already_notified(api_key: str, item: FeedItem, subject: str) -> bool:
    query = urllib.parse.urlencode({"subject": subject, "ordering": "-creation_date"})
    data = request_json("GET", f"/emails?{query}", api_key)
    target_url = normalize_url(item.link)
    target_guid = normalize_url(item.guid)

    for email in data.get("results", []):
        metadata = email.get("metadata") or {}
        canonical_url = normalize_url(email.get("canonical_url") or "")
        metadata_guid = normalize_url(str(metadata.get("guid") or ""))

        if canonical_url == target_url or metadata_guid == target_guid:
            status = email.get("status", "unknown")
            print(f"Already notified for {item.title!r}; Buttondown email status is {status}.")
            return True

    return False


def build_body(item: FeedItem) -> str:
    description = item.description.rstrip(".")
    return "\n".join(
        [
            "<!-- buttondown-editor-mode: plaintext -->",
            "Hello,",
            "",
            f"I have just published a new reflection on {SITE_NAME}:",
            "",
            f"## [{item.title}]({item.link})",
            "",
            description + ".",
            "",
            f"[Read it here]({item.link})",
            "",
            f"You are receiving this because you subscribed for new reflections at {SITE_NAME}.",
        ]
    )


def build_payload(item: FeedItem, status: str) -> dict:
    subject = f"New reflection: {item.title}"
    return {
        "subject": subject,
        "body": build_body(item),
        "canonical_url": item.link,
        "description": item.description,
        "email_type": "public",
        "status": status,
        "metadata": {
            "source": "blog-feed.xml",
            "site": SITE_NAME,
            "guid": item.guid,
        },
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notify Buttondown subscribers about the latest RSS item.")
    parser.add_argument("--feed", type=Path, default=DEFAULT_FEED)
    parser.add_argument(
        "--status",
        choices=("draft", "about_to_send"),
        default=os.environ.get("BUTTONDOWN_EMAIL_STATUS", "about_to_send"),
        help="Use draft for a review-only run, or about_to_send to queue delivery.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=os.environ.get("BUTTONDOWN_DRY_RUN", "").lower() in {"1", "true", "yes"},
        help="Print the payload without calling Buttondown.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    item = latest_feed_item(args.feed)
    payload = build_payload(item, args.status)

    if args.dry_run:
        print(json.dumps(payload, indent=2))
        return 0

    api_key = os.environ.get("BUTTONDOWN_API_KEY")
    if not api_key:
        print("Missing BUTTONDOWN_API_KEY. Add it as a GitHub Actions secret before this can send.", file=sys.stderr)
        return 2

    if already_notified(api_key, item, payload["subject"]):
        return 0

    response = request_json("POST", "/emails", api_key, payload)
    print(
        "Created Buttondown email "
        f"{response.get('id', '(unknown id)')} with status {response.get('status', '(unknown status)')}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
