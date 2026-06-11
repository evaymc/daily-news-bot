import os
import unittest
from unittest.mock import Mock, patch

os.environ.setdefault("GEMINI_API_KEY", "test-key")
os.environ.setdefault("TG_BOT_TOKEN", "test-token")
os.environ.setdefault("TG_CHAT_ID", "test-chat")

import main


class GeminiRetryTests(unittest.TestCase):
    def test_retries_on_503_and_succeeds(self):
        response = Mock(text="digest")
        retry_error = Exception("503 UNAVAILABLE")

        mock_generate = Mock(side_effect=[retry_error, response])
        mock_client = Mock()
        mock_client.models.generate_content = mock_generate

        with patch("main.genai.Client", return_value=mock_client), patch("main.time.sleep") as sleep_mock:
            result = main.call_gemini("prompt")

        self.assertEqual(result, "digest")
        self.assertEqual(mock_generate.call_count, 2)
        sleep_mock.assert_called_once_with(main.GEMINI_RETRY_SLEEP_SECONDS)

    def test_non_retryable_errors_are_raised_immediately(self):
        mock_generate = Mock(side_effect=RuntimeError("boom"))
        mock_client = Mock()
        mock_client.models.generate_content = mock_generate

        with patch("main.genai.Client", return_value=mock_client), patch("main.time.sleep") as sleep_mock:
            with self.assertRaises(RuntimeError):
                main.call_gemini("prompt")

        self.assertEqual(mock_generate.call_count, 1)
        sleep_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
