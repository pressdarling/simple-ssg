"""
SEO enhancement functionality for Simple-SSG.
"""

import os
import re

def generate_sitemap(config):
    """
    Generate a sitemap.xml file.
    
    Parameters:
    - config: Configuration object with sitemap settings
    """
    try:
        print("Generating sitemap.xml...")
        base_url = config.base_url.rstrip('/')
        output_dir = config.output_dir
        
        sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
        sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        
        # Add homepage
        sitemap += f'  <url>\n    <loc>{base_url}/</loc>\n    <priority>1.0</priority>\n  </url>\n'
        
        # Add each HTML page
        for root, _, files in os.walk(output_dir):
            for file in files:
                if file.endswith('.html') and file != 'index.html' and file != '404.html':
                    rel_path = os.path.relpath(os.path.join(root, file), output_dir)
                    url_path = rel_path.replace('\\', '/')  # Handle Windows paths
                    
                    # Set priority based on depth
                    depth = url_path.count('/')
                    priority = 0.8 if depth == 0 else 0.6 if depth == 1 else 0.4
                    
                    sitemap += f'  <url>\n    <loc>{base_url}/{url_path}</loc>\n    <priority>{priority}</priority>\n  </url>\n'
        
        sitemap += '</urlset>'
        
        # Write sitemap
        with open(os.path.join(output_dir, 'sitemap.xml'), 'w', encoding='utf-8') as f:
            f.write(sitemap)
            
        print(f"Sitemap generated at {output_dir}/sitemap.xml")
    except Exception as e:
        print(f"Error generating sitemap: {str(e)}")

def create_robots_txt(config):
    """
    Create a robots.txt file.
    
    Parameters:
    - config: Configuration object with robots.txt settings
    """
    try:
        print("Creating robots.txt...")
        base_url = config.base_url.rstrip('/')
        output_dir = config.output_dir
        
        robots_content = f"""User-agent: *
Allow: /
Sitemap: {base_url}/sitemap.xml
"""
        with open(os.path.join(output_dir, 'robots.txt'), 'w', encoding='utf-8') as f:
            f.write(robots_content)
            
        print(f"robots.txt created at {output_dir}/robots.txt")
    except Exception as e:
        print(f"Error creating robots.txt: {str(e)}")

def create_htaccess(config):
    """
    Create an .htaccess file for Apache servers.
    
    Parameters:
    - config: Configuration object with .htaccess settings
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
        with open(os.path.join(output_dir, '.htaccess'), 'w', encoding='utf-8') as f:
            f.write(htaccess_content)
            
        print(f".htaccess file created at {output_dir}/.htaccess")
    except Exception as e:
        print(f"Error creating .htaccess: {str(e)}")

def update_meta_tags(html, page_title, description, base_url, page_path):
    """
    Update meta tags in HTML for SEO.
    
    Parameters:
    - html: HTML content
    - page_title: Title of the page
    - description: Description of the page
    - base_url: Base URL of the site
    - page_path: Path to the page
    
    Returns:
    - HTML content with updated meta tags
    """
    try:
        # Update title
        if '<title>' in html and page_title:
            html = re.sub(r'<title>.*?</title>', f'<title>{page_title}</title>', html)
        
        # Update description
        if '<meta name="description" content="' in html and description:
            html = re.sub(r'<meta name="description" content="[^"]*"', 
                         f'<meta name="description" content="{description}"', 
                         html)
        
        # Update Open Graph tags
        if '<meta property="og:title" content="' in html and page_title:
            html = re.sub(r'<meta property="og:title" content="[^"]*"', 
                         f'<meta property="og:title" content="{page_title}"', 
                         html)
        
        if '<meta property="og:description" content="' in html and description:
            html = re.sub(r'<meta property="og:description" content="[^"]*"', 
                         f'<meta property="og:description" content="{description}"', 
                         html)
        
        if '<meta property="og:url" content="' in html and base_url and page_path:
            html = re.sub(r'<meta property="og:url" content="[^"]*"', 
                         f'<meta property="og:url" content="{base_url}/{page_path}"', 
                         html)
        
        # Update Twitter Card tags
        if '<meta name="twitter:title" content="' in html and page_title:
            html = re.sub(r'<meta name="twitter:title" content="[^"]*"', 
                         f'<meta name="twitter:title" content="{page_title}"', 
                         html)
        
        if '<meta name="twitter:description" content="' in html and description:
            html = re.sub(r'<meta name="twitter:description" content="[^"]*"', 
                         f'<meta name="twitter:description" content="{description}"', 
                         html)
        
        # Update canonical URL
        if '<link rel="canonical" href="' in html and base_url and page_path:
            html = re.sub(r'<link rel="canonical" href="[^"]*"', 
                         f'<link rel="canonical" href="{base_url}/{page_path}"', 
                         html)
        
        return html
    except Exception as e:
        print(f"Error updating meta tags: {str(e)}")
        return html
