"""
HTML minification functionality for Simple-SSG.
"""

import re

def minify_html(html):
    """
    Simple HTML minification.
    
    Parameters:
    - html: HTML content to minify
    
    Returns:
    - Minified HTML content
    """
    try:
        # Remove comments (except conditional comments for IE)
        html = re.sub(r'<!--(?![\s\S]*?\[if.*?\])[\s\S]*?-->', '', html, flags=re.DOTALL)
        
        # Remove unnecessary whitespace
        html = re.sub(r'\s+', ' ', html)
        html = re.sub(r'>\s+<', '><', html)
        
        # Trim whitespace around specific tags
        for tag in ['html', 'head', 'body', 'div', 'p', 'section', 'header', 
                    'footer', 'nav', 'main', 'article', 'aside', 'h1', 'h2', 
                    'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li']:
            html = re.sub(f'<{tag}>\s+', f'<{tag}>', html)
            html = re.sub(f'\s+</{tag}>', f'</{tag}>', html)
        
        return html.strip()
    except Exception as e:
        print(f"Error minifying HTML: {str(e)}")
        return html
