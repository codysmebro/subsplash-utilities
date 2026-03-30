"""Bulk-delete Subsplash media items by UUID from a CSV file.

Reads UUIDs from the first column of a CSV and sends DELETE requests
for each one. Useful for cleaning up hidden or orphaned media items
that appear in bulk-edit exports but not the Dashboard.

Usage:
    python scripts/bulk_media_delete.py <csv_file>
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from lib.api import BASE_URL, session


def bulk_delete(csv_path: str) -> None:
    url = f"{BASE_URL}/media/v1/media-items"
    api = session()

    with open(csv_path, "r") as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row]

    if not rows:
        print("CSV is empty, nothing to delete.")
        return

    has_header = not rows[0][0].replace("-", "").isalnum()
    items = rows[1:] if has_header else rows

    deleted = 0
    total = len(items)

    for i, row in enumerate(items, 1):
        uuid = row[0].strip()
        if not uuid:
            continue

        response = api.delete(f"{url}/{uuid}")
        if response.status_code in (200, 204):
            deleted += 1
            print(f"[{i}/{total}] Deleted {uuid}")
        else:
            print(f"[{i}/{total}] Failed to delete {uuid} — status {response.status_code}")

    print(f"\nDone. Deleted {deleted}/{total} media items.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk-delete Subsplash media items from CSV")
    parser.add_argument("csv_file", help="Path to CSV file with UUIDs in the first column")
    args = parser.parse_args()
    bulk_delete(args.csv_file)
