from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


def normalize_url(url: str) -> str:
    """Normalize a URL for comparison purposes.

    The normalized URL strips the scheme, drops a trailing slash from the path,
    removes fragments, and preserves the host, path, and query string.
    """
    if not isinstance(url, str):
        raise TypeError("URL must be a string")

    parsed = urlparse(url)
    if not parsed.netloc:
        parsed = urlparse("http://" + url)

    netloc = parsed.netloc.lower()
    if netloc.endswith(":80"):
        netloc = netloc[:-3]
    elif netloc.endswith(":443"):
        netloc = netloc[:-4]

    path = parsed.path or ""
    if path.endswith("/"):
        path = path[:-1]

    normalized = f"{netloc}{path}"
    if parsed.query:
        normalized = f"{normalized}?{parsed.query}"

    return normalized


def get_heading_from_html(html: str) -> str:
    """Return the <h1> text or fallback to <h2> text from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    heading = soup.find("h1")
    if heading:
        return heading.get_text(strip=True)

    fallback = soup.find("h2")
    return fallback.get_text(strip=True) if fallback else ""


def get_first_paragraph_from_html(html: str) -> str:
    """Return the first <p> within <main>, or first <p> in the document if no <main>."""
    soup = BeautifulSoup(html, "html.parser")
    main_tag = soup.find("main")
    if main_tag:
        paragraph = main_tag.find("p")
        if paragraph:
            return paragraph.get_text(strip=True)
        return ""

    paragraph = soup.find("p")
    return paragraph.get_text(strip=True) if paragraph else ""


def extract_page_data(html: str, page_url: str) -> dict:
    """Extract structured page metadata from HTML."""
    soup = BeautifulSoup(html, "html.parser")
    heading = get_heading_from_html(html)
    first_paragraph = get_first_paragraph_from_html(html)

    outgoing_links = []
    for link_tag in soup.find_all("a", href=True):
        href = link_tag["href"].strip()
        if href:
            outgoing_links.append(urljoin(page_url, href))

    image_urls = []
    for img_tag in soup.find_all("img", src=True):
        src = img_tag["src"].strip()
        if src:
            image_urls.append(urljoin(page_url, src))

    return {
        "url": page_url,
        "heading": heading,
        "first_paragraph": first_paragraph,
        "outgoing_links": outgoing_links,
        "image_urls": image_urls,
    }
