"""Ensure the crawler does not contact unscoped targets. All tests are offline."""
import unittest
from unittest.mock import Mock, patch

from app import TorCrawler


VALID_HOST = "a" * 56 + ".onion"


class CrawlerSafetyTests(unittest.TestCase):
    def test_reject_invalid_url_before_http_request(self):
        crawler = TorCrawler()
        with patch.object(crawler.session, "get") as get:
            result = crawler.crawl_url("http://example.com/" + VALID_HOST, ["example"])
        self.assertEqual(result, [])
        get.assert_not_called()

    def test_redirect_is_not_followed(self):
        crawler = TorCrawler()
        response = Mock(status_code=302, text="")
        with patch.object(crawler.session, "get", return_value=response) as get:
            result = crawler.crawl_url("http://" + VALID_HOST, ["example"])
        self.assertEqual(result, [])
        get.assert_called_once()
        self.assertFalse(get.call_args.kwargs["allow_redirects"])

    def test_only_onion_links_are_crawled(self):
        crawler = TorCrawler()
        hostname = "a" * 56 + ".onion"
        # No keyword matches: no persistence is performed.
        html = (
            '<a href="https://example.com/">outside</a>'
            + '<a href="http://' + hostname + '/next">inside</a>'
        )
        with patch.object(crawler.session, "get", return_value=Mock(status_code=200, text=html)) as get:
            crawler.crawl_url("http://" + hostname, ["unmatched-keyword"])
        called_urls = [c.args[0] for c in get.call_args_list]
        self.assertEqual(called_urls, ["http://" + hostname, "http://" + hostname + "/next"])


if __name__ == "__main__":
    unittest.main()
