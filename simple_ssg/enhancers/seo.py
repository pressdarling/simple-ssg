"""SEO enhancement functionality for Simple-SSG.

This module provides functions to improve the search engine optimization (SEO)
of the generated static site. Its responsibilities include:
- Generating a `sitemap.xml` file to help search engines discover pages.
- Creating a `robots.txt` file to guide search engine crawlers.
- Generating a `.htaccess` file with common optimizations for Apache servers.
- Dynamically updating meta tags (e.g., title, description, canonical URL)
  in the HTML for each page.
"""

import os
import re

from simple_ssg.config import SiteConfig


def generate_sitemap(config: SiteConfig) -> None:
    """Generates a `sitemap.xml` file for the site.

    This function scans the output directory for `.html` files and creates a
    `sitemap.xml` file that lists them. The priority of each page is determined
    by its depth in the directory structure.

    Args:
        config: The site configuration object, which provides the `base_url`
                and `output_dir`.
    """
    try:
        print("Generating sitemap.xml...")
        base_url = config.base_url.rstrip("/")
        output_dir = config.output_dir

        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'

        # Add homepage
        sitemap += (
            f"  <url>\n    <loc>{base_url}/</loc>\n    "
            "<priority>1.0</priority>\n  </url>\n"
        )

        # Add each HTML page
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith(".html") and file not in ("index.html", "404.html"):
                    rel_path = os.path.relpath(os.path.join(root, file), output_dir)
                    url_path = rel_path.replace("\\", "/")  # Handle Windows paths

                    # Set priority based on depth
                    depth = url_path.count("/")
                    priority = 0.8 if depth == 0 else 0.6 if depth == 1 else 0.4

                    sitemap += (
                        f"  <url>\n    <loc>{base_url}/{url_path}</loc>\n    "
                        f"<priority>{priority}</priority>\n  </url>\n"
                    )

        sitemap += "</urlset>"

        # Write sitemap
        with open(os.path.join(output_dir, "sitemap.xml"), "w", encoding="utf-8") as f:
            f.write(sitemap)

        print(f"Sitemap generated at {output_dir}/sitemap.xml")
    except Exception as e:
        print(f"Error generating sitemap: {str(e)}")


def create_robots_txt(config: SiteConfig) -> None:
    """Creates a `robots.txt` file for the site.

    This file instructs search engine crawlers on how to index the site and
    provides a link to the sitemap.

    Args:
        config: The site configuration object, used to get the `base_url` and
                `output_dir`.
    """
    try:
        print("Creating robots.txt...")
        base_url = config.base_url.rstrip("/")
        output_dir = config.output_dir

        robots_content = f"""User-agent: *
Allow: /
Sitemap: {base_url}/sitemap.xml
"""
        with open(os.path.join(output_dir, "robots.txt"), "w", encoding="utf-8") as f:
            f.write(robots_content)

        print(f"robots.txt created at {output_dir}/robots.txt")
    except Exception as e:
        print(f"Error creating robots.txt: {str(e)}")


def create_htaccess(config: SiteConfig) -> None:
    """Creates a `.htaccess` file with common configurations for Apache servers.

    This file includes settings for handling 404 errors, enabling GZIP
    compression, and setting browser caching policies to improve performance.

    Args:
        config: The site configuration object, used to get the `output_dir`.
    """
    try:
        print("Creating .htaccess file...")
        output_dir = config.output_dir

        htaccess_content = """# Handle 404 errors
ErrorDocument 404 /404.html

# Enable GZIP compression
<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/plain text/xml text/css text/javascript application/javascript application/x-javascript
</IfModule>

# Set caching
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType image/jpg "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/gif "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType text/css "access plus 1 month"
  ExpiresByType application/pdf "access plus 1 month"
  ExpiresByType text/javascript "access plus 1 month"
  ExpiresByType application/javascript "access plus 1 month"
  ExpiresByType application/x-javascript "access plus 1 month"
  ExpiresByType application/x-shockwave-flash "access plus 1 month"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresDefault "access plus 2 days"
</IfModule>
"""
        with open(os.path.join(output_dir, ".htaccess"), "w", encoding="utf-8") as f:
            f.write(htaccess_content)

        print(f".htaccess file created at {output_dir}/.htaccess")
    except Exception as e:
        print(f"Error creating .htaccess: {str(e)}")


def update_meta_tags(
    html: str,
    page_title: str,
    description: str,
    base_url: str,
    page_path: str,
) -> str:
    """Updates SEO-related meta tags in an HTML string.

    This function uses regular expressions to find and replace key SEO tags
    in the HTML content, such as the title, meta description, Open Graph tags,
    Twitter Card tags, and the canonical URL.

    Args:
        html: The HTML content to be modified.
        page_title: The title of the page.
        description: The meta description for the page.
        base_url: The base URL of the site.
        page_path: The relative path of the page from the site root.

    Returns:
        The HTML content with updated meta tags.
    """
    try:
        # Update title
        if "<title>" in html and page_title:
            html = re.sub(r"<title>.*?</title>", f"<title>{page_title}</title>", html)

        # Update description
        if '<meta name="description" content="' in html and description:
            html = re.sub(
                r'<meta name="description" content="[^"]*"',
                f'<meta name="description" content="{description}"',
                html,
            )

        # Update Open Graph tags
        if '<meta property="og:title" content="' in html and page_title:
            html = re.sub(
                r'<meta property="og:title" content="[^"]*"',
                f'<meta property="og:title" content="{page_title}"',
                html,
            )

        if '<meta property="og:description" content="' in html and description:
            html = re.sub(
                r'<meta property="og:description" content="[^"]*"',
                f'<meta property="og:description" content="{description}"',
                html,
            )

        if '<meta property="og:url" content="' in html and base_url and page_path:
            html = re.sub(
                r'<meta property="og:url" content="[^"]*"',
                f'<meta property="og:url" content="{base_url}/{page_path}"',
                html,
            )

        # Update Twitter Card tags
        if '<meta name="twitter:title" content="' in html and page_title:
            html = re.sub(
                r'<meta name="twitter:title" content="[^"]*"',
                f'<meta name="twitter:title" content="{page_title}"',
                html,
            )

        if '<meta name="twitter:description" content="' in html and description:
            html = re.sub(
                r'<meta name="twitter:description" content="[^"]*"',
                f'<meta name="twitter:description" content="{description}"',
                html,
            )

        # Update canonical URL
        if '<link rel="canonical" href="' in html and base_url and page_path:
            html = re.sub(
                r'<link rel="canonical" href="[^"]*"',
                f'<link rel="canonical" href="{base_url}/{page_path}"',
                html,
            )

        return html
    except Exception as e:
        print(f"Error updating meta tags: {str(e)}")
        return html
