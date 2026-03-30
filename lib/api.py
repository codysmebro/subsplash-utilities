import os
import sys

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "https://core.subsplash.com"

_cached_token: str | None = None


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        print(f"Error: {name} is not set.")
        print("Set it in your .env file or export it in your shell.")
        sys.exit(1)
    return value


def get_app_key() -> str:
    return _require_env("SUBSPLASH_APP_KEY")


def _fetch_token() -> str:
    """Exchange client credentials for a bearer token via the Subsplash token endpoint."""
    global _cached_token
    if _cached_token:
        return _cached_token

    client_id = _require_env("SUBSPLASH_CLIENT_ID")
    client_secret = _require_env("SUBSPLASH_CLIENT_SECRET")

    response = requests.post(
        f"{BASE_URL}/tokens/v1/token",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )

    if response.status_code != 200:
        print(f"Error: token request failed with status {response.status_code}")
        print(response.text)
        sys.exit(1)

    token = response.json().get("access_token")
    if not token:
        print("Error: token response did not contain access_token")
        print(response.json())
        sys.exit(1)

    _cached_token = token
    return token


def session() -> requests.Session:
    """Create an authenticated requests.Session for the Subsplash Core API."""
    s = requests.Session()
    s.headers.update({
        "Content-Type": "application/json",
        "Authorization": f"Bearer {_fetch_token()}",
    })
    return s
