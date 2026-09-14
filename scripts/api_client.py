"""
api_client.py

Week 4 Tuesday deliverable: retrieve and process information from a
public API using HTTP requests.

Two integrations, both practical for an IT toolkit:
  1. get_public_ip()   - the machine's public IP (support tickets,
                          remote troubleshooting, VPN verification).
  2. get_repo_status()  - live status of a GitHub repository (open
                          issues, last commit, stars) — useful for
                          keeping an eye on your own project's health.
"""

import logging
from datetime import datetime

import requests

logger = logging.getLogger(__name__)

IPIFY_URL = "https://api.ipify.org?format=json"
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}"

REQUEST_TIMEOUT = 5  # seconds — fail fast rather than hang indefinitely


def get_public_ip():
    """
    Fetch this machine's public IP address.

    Returns a dict: {"ip": "...", "retrieved_at": "..."} on success,
    or {"error": "..."} on failure — never raises, so callers can
    always safely check the result without wrapping every call in
    try/except themselves.
    """
    try:
        response = requests.get(IPIFY_URL, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        result = {
            "ip": data.get("ip"),
            "retrieved_at": datetime.now().isoformat(timespec="seconds"),
        }
        logger.info(f"Public IP retrieved: {result['ip']}")
        return result

    except requests.exceptions.Timeout:
        logger.error("Timed out contacting IP lookup service.")
        return {"error": "Request timed out — check your internet connection."}
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to IP lookup service.")
        return {"error": "No internet connection available."}
    except requests.exceptions.RequestException as error:
        logger.error(f"IP lookup failed: {error}")
        return {"error": f"IP lookup failed: {error}"}


def get_repo_status(owner, repo):
    """
    Fetch and process live status of a GitHub repository.

    Returns a dict with the useful fields extracted from GitHub's much
    larger API response — this is the "processing" half of the
    requirement, not just a raw passthrough of the API's JSON.
    """
    url = GITHUB_API_URL.format(owner=owner, repo=repo)

    try:
        response = requests.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        result = {
            "repository": data.get("full_name"),
            "description": data.get("description"),
            "open_issues": data.get("open_issues_count"),
            "stars": data.get("stargazers_count"),
            "default_branch": data.get("default_branch"),
            "last_updated": data.get("updated_at"),
            "url": data.get("html_url"),
        }
        logger.info(f"Repo status retrieved for '{result['repository']}'.")
        return result

    except requests.exceptions.HTTPError as error:
        if response.status_code == 404:
            logger.error(f"Repository '{owner}/{repo}' not found.")
            return {"error": f"Repository '{owner}/{repo}' not found."}
        if response.status_code == 403:
            remaining = response.headers.get("X-RateLimit-Remaining", "0")
            logger.error(f"GitHub API rate limit exceeded (remaining: {remaining}).")
            return {"error": "GitHub API rate limit exceeded. Try again later."}
        logger.error(f"GitHub API error: {error}")
        return {"error": f"GitHub API error: {error}"}
    except requests.exceptions.Timeout:
        logger.error("Timed out contacting GitHub API.")
        return {"error": "Request timed out — check your internet connection."}
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to GitHub API.")
        return {"error": "No internet connection available."}
    except requests.exceptions.RequestException as error:
        logger.error(f"Repo status lookup failed: {error}")
        return {"error": f"Repo status lookup failed: {error}"}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    print("\n=== Public IP ===")
    ip_info = get_public_ip()
    print(ip_info)

    print("\n=== GitHub Repo Status ===")
    repo_info = get_repo_status("NtandoBadla", "python-utilities-pack")
    print(repo_info)