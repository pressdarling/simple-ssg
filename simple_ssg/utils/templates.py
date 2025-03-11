"""
Template handling utilities for Simple-SSG.
"""

import os
import re
from simple_ssg.enhancers.seo import update_meta_tags

def inject_content(content, content_path, config):
    """
    Inject content into the template.
    
    Parameters:
    - content: The HTML content to inject
    - content_path: Path to the original content file (for metadata extraction)
    - config: Configuration object
    
    Returns:
    - Complete HTML page with content injected
    """
    try:
        # Read template
        with open(config.template_path, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # Extract metadata from content
        title, description = extract_metadata(content)
        base_name = os.path.basename(content_path).replace('.md', '').replace('.html', '')
        
        # Replace content placeholder
        placeholder = config.content_placeholder
        closing_div = '</div>'
        
        if placeholder in template:
            # Find the position of the placeholder
            start_pos = template.find(placeholder)
            
            # Find the position of the next closing div after the placeholder
            end_pos = template.find(closing_div, start_pos)
            
            # Replace everything between placeholder and closing div
            if start_pos != -1 and end_pos != -1:
                template = (
                    template[:start_pos + len(placeholder)] + 
                    f"\n{content}\n" + 
                    template[end_pos:]
                )
            else:
                print(f"Warning: Could not find closing tag for content placeholder in template.")
                template = template.replace(placeholder + closing_div, placeholder + f"\n{content}\n" + closing_div)
        else:
            # Fallback: Try a regex approach
            template = re.sub(
                r'<div id="content-container">\s*<div class="loading">.*?</div>\s*</div>', 
                f'<div id="content-container">\n{content}\n</div>', 
                template
            )
        
        # Update meta tags
        if title or description:
            template = update_meta_tags(
                template, 
                title, 
                description, 
                config.base_url, 
                f"{base_name}.html"
            )
        
        return template
        
    except Exception as e:
        print(f"Error injecting content into template: {str(e)}")
        return f"<html><body><h1>Error</h1><p>{str(e)}</p><div>{content}</div></body></html>"

def extract_metadata(content):
    """
    Extract title and description from content.
    
    Parameters:
    - content: HTML content
    
    Returns:
    - Tuple of (title, description)
    """
    title = None
    description = None
    
    # Extract title from the first h1 tag
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content)
    if title_match:
        title = title_match.group(1)
    
    # Extract description from the first paragraph after h1
    if title:
        # Try to find the first paragraph after the h1
        desc_match = re.search(r'<h1[^>]*>.*?</h1>\s*<p>(.*?)</p>', content, re.DOTALL)
        if desc_match:
            # Strip HTML tags and truncate to ~160 chars for meta description
            description = re.sub(r'<[^>]+>', '', desc_match.group(1))
            description = description.strip()
            
            if len(description) > 160:
                # Truncate to nearest word boundary
                description = description[:157].rsplit(' ', 1)[0] + '...'
    
    return title, description
