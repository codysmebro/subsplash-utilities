# Subsplash Utilities

A collection of Python scripts for working with the Subsplash Core API.

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and fill in your credentials:

   ```bash
   cp .env.example .env
   ```

   You'll need your Subsplash API client ID and secret. A bearer token is fetched automatically via the client credentials grant at runtime.

## Scripts

### Bulk Media Create

Creates N empty media items for a given app key. Useful for generating IDs to use in bulk-edit workflows.

```bash
python scripts/bulk_media_create.py 50
python scripts/bulk_media_create.py 100 --title "Sermon Upload"
```

Requires `SUBSPLASH_APP_KEY` in your `.env` (plus the client credentials for auth).

### Bulk Media Delete

Deletes media items by UUID from a CSV file (first column). Built for cleaning up hidden/orphaned media items that show in bulk-edit CSV exports but not the Dashboard.

```bash
python scripts/bulk_media_delete.py data/items_to_delete.csv
```

The CSV should have UUIDs in the first column (header row is auto-detected and skipped).

## Adding New Scripts

1. Create a new file in `scripts/`.
2. Use the shared API client from `lib/api.py`:

   ```python
   import sys
   from pathlib import Path

   sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

   from lib.api import BASE_URL, session, get_app_key
   ```

3. Put input data files (CSVs, etc.) in `data/` — that directory is gitignored.
