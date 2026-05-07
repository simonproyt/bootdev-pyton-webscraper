import unittest

from crawl import (
    get_first_paragraph_from_html,
    get_heading_from_html,
    normalize_url,
)


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

    def test_get_heading_from_html_basic(self):
        input_body = '<html><body><h1>Test Title</h1></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Test Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_falls_back_to_h2(self):
        input_body = '<html><body><h2>Secondary Title</h2></body></html>'
        actual = get_heading_from_html(input_body)
        expected = "Secondary Title"
        self.assertEqual(actual, expected)

    def test_get_heading_from_html_returns_empty_without_heading(self):
        input_body = '<html><body><div>No heading here</div></body></html>'
        actual = get_heading_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_main_priority(self):
        input_body = '''<html><body>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
        </body></html>'''
        actual = get_first_paragraph_from_html(input_body)
        expected = "Main paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_falls_back_without_main(self):
        input_body = '<html><body><p>First paragraph.</p><p>Second paragraph.</p></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = "First paragraph."
        self.assertEqual(actual, expected)

    def test_get_first_paragraph_from_html_returns_empty_without_paragraph(self):
        input_body = '<html><body><div>No paragraphs here</div></body></html>'
        actual = get_first_paragraph_from_html(input_body)
        expected = ""
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
