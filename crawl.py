from urllib.parse import urlparse


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
