"""HTML processing for Simple-SSG.

This module is responsible for handling `.html` files found in the content
directory. At present, it acts as a simple passthrough, meaning that the HTML
content is not modified.

This structure is in place to allow for future enhancements, such as HTML
linting, cleaning, or other forms of processing, providing a consistent
interface alongside other converters like the Markdown converter.
"""
from typing import Optional

from simple_ssg.config import SiteConfig


def convert_html_to_html(
    html_content: str, config: Optional[SiteConfig] = None
) -> str:
    """Processes HTML content.

    This function currently serves as a passthrough for HTML content, returning it
    without any modifications. It is designed to fit into the converter pipeline
    and can be extended to perform transformations on HTML files if needed in the
    future.

    Args:
        html_content: The HTML content to be processed.
        config: The site configuration object. This is included for API
                consistency with other converters but is not currently used.

    Returns:
        The unchanged HTML content.
    """
    # This is just a passthrough for HTML content.
    # Could add processing like removing comments or linting if desired.
    return html_content
