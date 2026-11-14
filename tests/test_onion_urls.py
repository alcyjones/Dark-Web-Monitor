"""Offline validation tests; never contact Tor or external services."""
import unittest
from app import is_valid_onion_url


VALID_HOST = "a" * 56 + ".onion"


class OnionUrlValidationTests(unittest.TestCase):
    def test_valid_v3_onion(self):
        self.assertTrue(is_valid_onion_url("http://" + VALID_HOST))
        self.assertTrue(is_valid_onion_url("https://" + VALID_HOST + "/path?q=1"))

    def test_reject_non_onion_and_host_spoofing(self):
        invalid = [
            "https://example.com/?next=" + VALID_HOST,
            "http://" + VALID_HOST + ".example.com",
            "http://example.com/" + VALID_HOST,
            "http://127.0.0.1:9050",
            "file:///etc/passwd",
            "http://short.onion",
            "http://user:password@" + VALID_HOST,
            "http://" + VALID_HOST + ":8080",
            "http://" + VALID_HOST + "/hello world",
            "http://" + VALID_HOST + "/#fragment",
            "",
            None,
        ]
        for value in invalid:
            with self.subTest(value=value):
                self.assertFalse(is_valid_onion_url(value))

    def test_reject_malformed(self):
        self.assertFalse(is_valid_onion_url("not a url"))
        self.assertFalse(is_valid_onion_url("http://["))
        self.assertFalse(is_valid_onion_url("http://" + "0" * 56 + ".onion"))


if __name__ == "__main__":
    unittest.main()
