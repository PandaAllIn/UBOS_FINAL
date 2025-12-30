from __future__ import annotations

import pytest
from unittest.mock import MagicMock, patch
from trinity.wolfram_alpha_oracle import WolframAlphaOracle


@pytest.fixture
def oracle() -> WolframAlphaOracle:
    return WolframAlphaOracle(api_key="test_key")


def test_query_success(oracle: WolframAlphaOracle):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "queryresult": {
            "success": True,
            "pods": [
                {
                    "title": "Result",
                    "subpods": [
                        {
                            "plaintext": "42"
                        }
                    ]
                }
            ]
        }
    }

    with patch("requests.Session.get", return_value=mock_response):
        result = oracle.query("what is the meaning of life?")
        assert "Result: 42" in result


def test_query_failure(oracle: WolframAlphaOracle):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad request"

    with patch("requests.Session.get", return_value=mock_response):
        result = oracle.query("invalid query")
        assert "Wolfram Alpha error 400" in result
