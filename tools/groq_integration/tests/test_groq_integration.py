import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

FILE_PATH = Path(__file__).resolve()
POTENTIAL_ROOTS = [FILE_PATH.parents[2], FILE_PATH.parents[1], FILE_PATH.parents[3]]
ROOT = None
for candidate in POTENTIAL_ROOTS:
    if candidate and (candidate / "groq_integration").exists():
        ROOT = candidate
        break
if ROOT is None:
    ROOT = FILE_PATH.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from groq_integration.groq_client import GroqClient, GroqUnavailableError
    from groq_integration.dual_speed_brain import DualSpeedCognition
except ModuleNotFoundError:  # pragma: no cover - fallback for flat installs
    tools_candidate = ROOT / "groq_integration"
    if not tools_candidate.exists():
        tools_candidate = ROOT / "tools"
    if str(tools_candidate) not in sys.path:
        sys.path.insert(0, str(tools_candidate))
    try:
        from groq_integration.groq_client import GroqClient, GroqUnavailableError  # type: ignore
        from groq_integration.dual_speed_brain import DualSpeedCognition  # type: ignore
    except ModuleNotFoundError:
        from groq_client import GroqClient, GroqUnavailableError  # type: ignore
        from dual_speed_brain import DualSpeedCognition  # type: ignore


class _MockResponse:
    def __init__(self, text: str, tokens: int = 100) -> None:
        self.text = text
        self.usage = {"total_tokens": tokens}
        self.choices = [{"message": {"content": [{"type": "text", "text": text}]}}]

    def model_dump(self):
        return {"usage": self.usage, "choices": self.choices}


class GroqClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.patcher = mock.patch("groq_integration.groq_client.Groq")
        mock_groq = self.patcher.start()
        self.mock_client = mock.Mock()
        mock_groq.return_value = self.mock_client
        os.environ["GROQ_API_KEY"] = "test-key"
        self.client = GroqClient()

    def tearDown(self) -> None:
        self.patcher.stop()

    def test_fast_think_basic(self):
        self.mock_client.chat.completions.create.return_value = _MockResponse("hello world")
        result = self.client.fast_think("hi")
        self.assertEqual(result.strip(), "hello world")

    def test_fast_think_timeout(self):
        self.mock_client.chat.completions.create.side_effect = GroqUnavailableError("timeout")
        result = self.client.fast_think("hi")
        self.assertIn("timeout", result)

    def test_fast_think_retry(self):
        self.mock_client.chat.completions.create.side_effect = [
            Exception("temporary failure"),
            _MockResponse("retry success"),
        ]
        result = self.client.fast_think("hi")
        self.assertIn("retry", result)

    def test_web_search(self):
        self.mock_client.chat.completions.create.return_value = _MockResponse(
            '{"results": [{"title": "Example"}]}'
        )
        data = self.client.web_search("example query")
        self.assertIsInstance(data, dict)

    def test_wolfram(self):
        os.environ["WOLFRAM_APP_ID"] = "demo"
        self.mock_client.chat.completions.create.return_value = _MockResponse("42")
        result = self.client.wolfram("integrate x^2")
        self.assertEqual(result.strip(), "42")

    def test_error_handling_no_api_key(self):
        with mock.patch.dict(os.environ, {"GROQ_API_KEY": ""}):
            client = GroqClient(api_key="")
            self.assertFalse(client.is_available())
            message = client.fast_think("should fallback")
            self.assertIn("Groq client unavailable", message)


class DualSpeedCognitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.groq = mock.create_autospec(GroqClient, instance=True)
        self.groq.is_available.return_value = True
        self.temp_model = Path(tempfile.gettempdir()) / "mock-model.gguf"
        self.temp_model.write_bytes(b"mock")
        self.dual = DualSpeedCognition(self.groq, str(self.temp_model))
        self.dual.llama_cli = Path("/bin/echo")

    def tearDown(self) -> None:
        try:
            self.temp_model.unlink()
        except FileNotFoundError:
            pass

    def test_scout_mode(self):
        self.groq.fast_think.return_value = "fast"
        response = self.dual.scout("prompt")
        self.assertEqual(response, "fast")
        self.groq.fast_think.assert_called_once()

    def test_deliberate_mode(self):
        output = self.dual.deliberate("prompt")
        self.assertIn("prompt", output)

    def test_adaptive_mode(self):
        self.groq.fast_think.return_value = "scout result"
        result = self.dual.adaptive("question")
        self.assertIn("Fast scout", result)
        self.assertIn("Deep deliberation", result)

    def test_rate_limiting(self):
        self.dual.daily_limit = 1
        self.dual.api_calls_today = 1
        self.assertFalse(self.dual.should_use_groq())

    def test_fallback_when_groq_down(self):
        self.groq.is_available.return_value = False
        result = self.dual.scout("prompt")
        self.assertIn("prompt", result)


if __name__ == "__main__":
    unittest.main()
