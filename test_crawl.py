import unittest

from crawl import (
    extract_page_data,
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

    def test_extract_page_data_basic(self):
        input_url = "https://crawler-test.com"
        input_body = '''<html><body>
            <h1>Test Title</h1>
            <p>This is the first paragraph.</p>
            <a href="/link1">Link 1</a>
            <img src="/image1.jpg" alt="Image 1">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com",
            "heading": "Test Title",
            "first_paragraph": "This is the first paragraph.",
            "outgoing_links": ["https://crawler-test.com/link1"],
            "image_urls": ["https://crawler-test.com/image1.jpg"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_h2_heading_and_main_paragraph(self):
        input_url = "https://crawler-test.com/page"
        input_body = '''<html><body>
            <h2>Secondary Title</h2>
            <p>Outside paragraph.</p>
            <main>
                <p>Main paragraph.</p>
            </main>
            <a href="relative/link2">Link 2</a>
            <img src="images/image2.png" alt="Image 2">
        </body></html>'''
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com/page",
            "heading": "Secondary Title",
            "first_paragraph": "Main paragraph.",
            "outgoing_links": ["https://crawler-test.com/relative/link2"],
            "image_urls": ["https://crawler-test.com/images/image2.png"],
        }
        self.assertEqual(actual, expected)

    def test_extract_page_data_handles_missing_elements(self):
        input_url = "https://crawler-test.com/empty"
        input_body = '<html><body><div>No relevant content</div></body></html>'
        actual = extract_page_data(input_body, input_url)
        expected = {
            "url": "https://crawler-test.com/empty",
            "heading": "",
            "first_paragraph": "",
            "outgoing_links": [],
            "image_urls": [],
        }
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
