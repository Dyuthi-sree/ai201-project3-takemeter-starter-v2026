"""
Collect public text posts from r/artificial using the PullPush archive.

Output:
    labels.csv

Columns:
    text  - Reddit post title and body
    label - left blank for you to complete
    note  - source URL for the Reddit post
"""

import csv
import time
from pathlib import Path

import requests


SUBREDDIT = "artificial"
TARGET_ROWS = 200
REQUEST_SIZE = 50
API_URL = "https://api.pullpush.io/reddit/search/submission/"
OUTPUT_FILE = Path("labels.csv")

HEADERS = {
    "User-Agent": "TakeMeter student dataset collector/1.0"
}


def clean_text(value: str) -> str:
    """Remove extra spaces and line breaks."""
    return " ".join((value or "").split())


def load_existing_texts() -> set[str]:
    """Load already-collected text so rerunning does not create duplicates."""
    if not OUTPUT_FILE.exists():
        return set()

    with OUTPUT_FILE.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return {
            clean_text(row.get("text", "")).lower()
            for row in reader
            if clean_text(row.get("text", ""))
        }


def existing_row_count() -> int:
    """Return the number of data rows already in labels.csv."""
    if not OUTPUT_FILE.exists():
        return 0

    with OUTPUT_FILE.open("r", encoding="utf-8", newline="") as file:
        return sum(1 for _ in csv.DictReader(file))


def collect_posts() -> list[dict]:
    """Collect posts until labels.csv will contain TARGET_ROWS rows."""
    current_count = existing_row_count()

    if current_count >= TARGET_ROWS:
        print(
            f"{OUTPUT_FILE} already contains {current_count} rows. "
            "Nothing more needs to be collected."
        )
        return []

    seen_texts = load_existing_texts()
    collected = []
    before = None

    while current_count + len(collected) < TARGET_ROWS:
        params = {
            "subreddit": SUBREDDIT,
            "size": REQUEST_SIZE,
            "sort": "desc",
            "sort_type": "created_utc",
        }

        if before is not None:
            params["before"] = before

        print(
            f"Requesting up to {REQUEST_SIZE} posts from "
            f"r/{SUBREDDIT}..."
        )

        try:
            response = requests.get(
                API_URL,
                params=params,
                headers=HEADERS,
                timeout=60,
            )

            if response.status_code == 429:
                print("Rate limited. Waiting 60 seconds before trying again...")
                time.sleep(60)
                continue

            response.raise_for_status()
            payload = response.json()

        except requests.RequestException as error:
            print(f"Request failed: {error}")
            print("Waiting 60 seconds before trying again...")
            time.sleep(60)
            continue
        except ValueError:
            print("The server returned data that was not valid JSON.")
            break

        posts = payload.get("data", [])

        if not posts:
            print("No additional posts were returned.")
            break

        oldest_timestamp = None

        for post in posts:
            created_utc = post.get("created_utc")

            if created_utc is not None:
                if oldest_timestamp is None:
                    oldest_timestamp = created_utc
                else:
                    oldest_timestamp = min(oldest_timestamp, created_utc)

            title = clean_text(post.get("title", ""))
            body = clean_text(post.get("selftext", ""))

            # Skip deleted, removed, empty, or extremely short posts.
            if body.lower() in {"[deleted]", "[removed]"}:
                body = ""

            text = clean_text(f"{title} {body}")

            if len(text) < 40:
                continue

            normalized_text = text.lower()

            if normalized_text in seen_texts:
                continue

            post_id = post.get("id", "")
            permalink = post.get("permalink", "")

            if permalink:
                if permalink.startswith("http"):
                    source_url = permalink
                else:
                    source_url = f"https://www.reddit.com{permalink}"
            elif post_id:
                source_url = (
                    f"https://www.reddit.com/r/{SUBREDDIT}/"
                    f"comments/{post_id}/"
                )
            else:
                source_url = f"https://www.reddit.com/r/{SUBREDDIT}/"

            collected.append(
                {
                    "text": text,
                    "label": "",
                    "note": source_url,
                }
            )
            seen_texts.add(normalized_text)

            if current_count + len(collected) >= TARGET_ROWS:
                break

        print(
            f"Collected {current_count + len(collected)} "
            f"of {TARGET_ROWS} total rows."
        )

        if oldest_timestamp is None:
            print("Could not find a timestamp for the next page.")
            break

        # PullPush uses this timestamp to request older posts next time.
        before = int(oldest_timestamp) - 1

        # Slow down requests to reduce the chance of another 429 response.
        time.sleep(10)

    return collected


def save_posts(rows: list[dict]) -> None:
    """Append new rows to labels.csv without removing existing work."""
    if not rows:
        return

    file_exists = OUTPUT_FILE.exists()
    needs_header = not file_exists or OUTPUT_FILE.stat().st_size == 0

    with OUTPUT_FILE.open(
        "a",
        encoding="utf-8",
        newline="",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["text", "label", "note"],
        )

        if needs_header:
            writer.writeheader()

        writer.writerows(rows)

    print(f"Added {len(rows)} new rows to {OUTPUT_FILE}.")
    print(f"{OUTPUT_FILE} now contains {existing_row_count()} rows.")


def main() -> None:
    print(f"Collecting public posts from r/{SUBREDDIT}...")
    posts = collect_posts()
    save_posts(posts)

    print()
    print("Collection finished.")
    print("The label column is intentionally blank.")
    print("Label the first 20 rows yourself before using AI assistance.")


if __name__ == "__main__":
    main()