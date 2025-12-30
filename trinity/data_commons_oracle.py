"""Lightweight Data Commons wrapper for Trinity oracles."""
from __future__ import annotations

import logging
import os
from typing import Any, Dict, Optional

import requests

LOGGER = logging.getLogger("trinity.data_commons")


import datacommons_pandas as dcp
import datacommons as dc

LOGGER = logging.getLogger("trinity.data_commons")


class DataCommonsOracle:
    """Thin HTTP client for the public Data Commons API."""

    def __init__(self, api_key: Optional[str] = None, *, base_url: str | None = None, session: Optional[requests.Session] = None) -> None:
        self.api_key = api_key or os.getenv("DATA_COMMONS_API_KEY")
        dc.set_api_key(self.api_key)

    # ------------------------------------------------------------------ public API
    def query_demographics(self, dcid: str, stat_var: str = "Count_Person") -> str:
        try:
            df = dcp.build_time_series_dataframe([dcid], stat_var)
            if df.empty:
                return f"No Data Commons series available for {dcid}."
            latest_date = df.columns[-1]
            latest_value = df.iloc[0, -1]
            return f"Population for {dcid} latest value: {latest_value} (as of {latest_date})."
        except Exception as e:
            return f"Data Commons demographics unavailable for {dcid}: {e}"

    def query_economics(self, dcid: str, stat_var: str = "GDP_PerCapita_PPP") -> str:
        try:
            df = dcp.build_time_series_dataframe([dcid], stat_var)
            if df.empty:
                return f"No Data Commons series available for {dcid}."
            latest_date = df.columns[-1]
            latest_value = df.iloc[0, -1]
            return f"Economic indicator for {dcid} latest value: {latest_value} (as of {latest_date})."
        except Exception as e:
            return f"Data Commons economics unavailable for {dcid}: {e}"

    def resolve_place(self, name: str) -> str:
        try:
            places = dc.resolve_entities([name], "Place")
            if not places:
                return f"Unable to resolve place '{name}' via Data Commons."
            return f"Resolved '{name}' to {places[0]}."
        except Exception as e:
            return f"Unable to resolve place '{name}' via Data Commons: {e}"

