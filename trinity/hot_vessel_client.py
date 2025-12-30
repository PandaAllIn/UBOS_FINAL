from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any, Dict, Mapping
from urllib import error, request
from urllib.parse import urljoin


LOGGER = logging.getLogger(__name__)


@dataclass(slots=True)
class VesselResponse:
    """Represents the outcome of an interaction with a hot vessel API."""

    ok: bool
    text: str = ""
    raw: Dict[str, Any] | None = None
    error: str | None = None


class HotVesselClient:
    """Lightweight HTTP client for resident hot-vessel API servers."""

    def __init__(
        self,
        base_url: str,
        *,
        prompt_field: str,
        endpoint: str = "/query",
        response_field: str = "response",
        default_payload: Mapping[str, Any] | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.prompt_field = prompt_field
        self.endpoint = endpoint
        self.response_field = response_field
        self.default_payload = dict(default_payload or {})
        self.timeout = timeout

    # ------------------------------------------------------------------ public helpers
    def query(self, prompt: str, payload: Mapping[str, Any] | None = None) -> VesselResponse:
        """Execute a text query against the resident."""

        body: Dict[str, Any] = dict(self.default_payload)
        if payload:
            body.update(payload)
        body[self.prompt_field] = prompt

        try:
            raw = self._post_json(self.endpoint, body)
        except Exception as exc:  # pragma: no cover - network guard
            message = getattr(exc, "reason", None) or str(exc)
            LOGGER.warning("Hot vessel request failed (%s): %s", self.base_url, message)
            return VesselResponse(ok=False, text="", raw=None, error=message)

        if not isinstance(raw, dict):  # pragma: no cover - defensive
            LOGGER.warning("Unexpected payload from %s: %r", self.base_url, raw)
            return VesselResponse(ok=False, text="", raw=None, error="Malformed response from hot vessel")

        error_text = raw.get("error")
        text_value = raw.get(self.response_field) or ""
        ok = error_text is None
        if not text_value and ok:
            text_value = ""

        return VesselResponse(
            ok=ok,
            text=text_value if ok else "",
            raw=raw,
            error=str(error_text) if error_text else None,
        )

    # ------------------------------------------------------------------ internal helpers
    def _post_json(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        data = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=data, method="POST")
        req.add_header("Content-Type", "application/json")
        try:
            with request.urlopen(req, timeout=self.timeout) as resp:
                charset = resp.headers.get_content_charset() or "utf-8"
                body = resp.read().decode(charset)
        except error.HTTPError as exc:
            payload = exc.read().decode("utf-8", errors="ignore")
            LOGGER.debug("Hot vessel HTTP error %s: %s", exc.code, payload)
            raise
        return json.loads(body) if body else {}


__all__ = ["HotVesselClient", "VesselResponse"]
