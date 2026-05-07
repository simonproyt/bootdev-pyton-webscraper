import unittest

from crawl import normalize_url


class TestCrawl(unittest.TestCase):
    def test_normalize_url_strips_scheme(self):
        input_url = "https://www.boot.dev/blog/path"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_strips_trailing_slashes(self):
        input_url = "http://www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_preserves_query(self):
        input_url = "https://www.boot.dev/blog/path/?page=1"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path?page=1"
        self.assertEqual(actual, expected)

    def test_normalize_url_drops_fragment(self):
        input_url = "https://www.boot.dev/blog/path#section"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_handles_url_without_scheme(self):
        input_url = "www.boot.dev/blog/path/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev/blog/path"
        self.assertEqual(actual, expected)

    def test_normalize_url_root_url(self):
        input_url = "https://www.boot.dev/"
        actual = normalize_url(input_url)
        expected = "www.boot.dev"
        self.assertEqual(actual, expected)

    def test_normalize_url_rejects_non_string(self):
        with self.assertRaises(TypeError):
            normalize_url(None)


if __name__ == "__main__":
    unittest.main()
