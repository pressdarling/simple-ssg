"""HTML minification functionality for Simple-SSG.

This module provides a simple, regex-based HTML minifier. Its purpose is to
reduce the file size of the generated HTML by removing unnecessary whitespace
and comments, which can lead to faster page loads.

The minification is not intended to be as comprehensive as dedicated tools like
html-minifier, but it provides a good balance of simplicity and effectiveness
for the needs of this project.
"""

import re


def minify_html(html: str) -> str:
    """Performs a simple minification of an HTML string.

    This function applies a series of regular expression substitutions to
    reduce the size of the HTML content. The process includes:
    1. Removing HTML comments (while preserving conditional IE comments).
    2. Collapsing consecutive whitespace characters into a single space.
    3. Removing whitespace between tags (e.g., `> <` becomes `><`).
    4. Trimming leading and trailing whitespace from the entire document.

    Note: This is a lightweight, regex-based minifier and not a full HTML
    parser. It may not be safe for all HTML, especially if it contains
    `<code>` or `<pre>` tags with significant whitespace.

    Args:
        html: The HTML content to be minified.

    Returns:
        The minified HTML content as a string. If an error occurs, the
        original HTML is returned.
    """
    try:
        # Remove comments (except conditional comments for IE)
        html = re.sub(
            r"<!--(?![\s\S]*?\[if.*?\])[\s\S]*?-->", "", html, flags=re.DOTALL
        )

        # Remove unnecessary whitespace
        html = re.sub(r"\s+", " ", html)
        html = re.sub(r">\s+<", "><", html)

        # Trim whitespace around specific tags
        for tag in [
            "html",
            "head",
            "body",
            "div",
            "p",
            "section",
            "header",
            "footer",
            "nav",
            "main",
            "article",
            "aside",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "ul",
            "ol",
            "li",
        ]:
            html = re.sub(f"<{tag}>" + r"\s+", f"<{tag}>", html)
            html = re.sub(r"\s+" + f"</{tag}>", f"</{tag}>", html)

        return html.strip()
    except Exception as e:
        print(f"Error minifying HTML: {str(e)}")
        return html
