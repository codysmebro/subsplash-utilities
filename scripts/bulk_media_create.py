"""Bulk-create empty Subsplash media items for a given app key.

Creates N empty media items so you have IDs ready for bulk-edit workflows.
Could be extended to attach metadata or files from external sources.

Usage:
    python scripts/bulk_media_create.py <count> [--title "Custom Title"]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api import BASE_URL, get_app_key, session


def bulk_create(count: int, title: str) -> None:
    url = f"{BASE_URL}/media/v1/media-items"
    app_key = get_app_key()
    api = session()

    data = {"app_key": app_key, "title": title}

    created = 0
    for i in range(count):
        response = api.post(url, json=data)
        if response.status_code == 201:
            created += 1
            print(f"[{i + 1}/{count}] Media item created")
        else:
            print(
                f"[{i + 1}/{count}] Failed — "
                f"{response.request.method} {response.url} "
                f"status {response.status_code}"
            )

    print(f"\nDone. Created {created}/{count} media items.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk-create Subsplash media items")
    parser.add_argument("count", type=int, help="Number of media items to create")
    parser.add_argument(
        "--title",
        default="Bulk Created",
        help='Title for each media item (default: "Bulk Created")',
    )
    args = parser.parse_args()
    bulk_create(args.count, args.title)
