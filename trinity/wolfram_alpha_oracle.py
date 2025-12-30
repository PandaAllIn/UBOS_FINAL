"""Lightweight Wolfram Alpha wrapper for Trinity oracles."""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

import requests

LOGGER = logging.getLogger("trinity.wolfram_alpha_oracle")


class WolframAlphaOracle:
    """Thin HTTP client for the Wolfram Alpha API."""

    def __init__(self, api_key: Optional[str] = None, *, base_url: str | None = None, session: Optional[requests.Session] = None) -> None:
        self.api_key = api_key or os.getenv("WOLFRAM_ALPHA_APP_ID")
        self.base_url = (base_url or os.getenv("WOLFRAM_ALPHA_API_BASE", "https://api.wolframalpha.com/v2")).rstrip("/")
        self.session = session or requests.Session()

    def _request(self, endpoint: str, params: Dict[str, Any]) -> str:
        url = f"{self.base_url}{endpoint}"
        params["appid"] = self.api_key
        params["output"] = "json"
        try:
            response = self.session.get(url, params=params, timeout=10)
        except requests.RequestException as exc:
            LOGGER.warning("Wolfram Alpha request failed: %s", exc)
            return f"Wolfram Alpha request failed: {exc}"
        if response.status_code != 200:
            LOGGER.warning("Wolfram Alpha error %s: %s", response.status_code, response.text[:200])
            return f"Wolfram Alpha error {response.status_code}: {response.text[:200]}"
        
        try:
            data = response.json()
            if data.get("queryresult", {}).get("success"):
                pods = data.get("queryresult", {}).get("pods", [])
                result = []
                for pod in pods:
                    title = pod.get("title")
                    subpods = pod.get("subpods", [])
                    for subpod in subpods:
                        plaintext = subpod.get("plaintext")
                        if plaintext:
                            result.append(f"{title}: {plaintext}")
                return "\n".join(result)
            else:
                return "Wolfram Alpha query was not successful."
        except ValueError:
            LOGGER.warning("Wolfram Alpha returned non-JSON payload")
            return "Wolfram Alpha returned non-JSON payload"

    def query(self, query: str) -> str:
        """Query Wolfram Alpha."""
        return self._request("/query", {"input": query})
