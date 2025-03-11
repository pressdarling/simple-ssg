"""
Markdown converter for Simple-SSG.
"""

import re
import markdown

def convert_markdown_to_html(md_content, config=None):
    """
    Convert Markdown content to HTML.
    
    Parameters:
    - md_content: The Markdown content to convert
    - config: Configuration object with conversion settings
    
    Returns:
    - HTML content
    """
    try:
        # Get markdown extensions from config or use defaults
        extensions = config.markdown_extensions if config else ['extra', 'tables', 'smarty']
        
        # Create Markdown processor with extensions
        md = markdown.Markdown(extensions=extensions)
        
        # Convert to HTML
        html = md.convert(md_content)
        
        # Process class annotations {.classname}
        html = process_class_annotations(html)
        
        return html
    except Exception as e:
        error_msg = f"Error converting markdown to HTML: {str(e)}"
        print(error_msg)
        return f"<p>{error_msg}</p>"

def process_class_annotations(html):
    """
    Process class annotations in the form of {.classname}.
    
    Parameters:
    - html: HTML content with class annotations
    
    Returns:
    - HTML content with class attributes
    """
    try:
        # Match {.classname} after HTML tags and add class attribute
        html = re.sub(r'(\<[^>]+\>)(\{\.([a-zA-Z0-9_-]+)\})', r'\1 class="\3"', html)
        
        # Handle multiple classes {.class1.class2}
        html = re.sub(r'(\<[^>]+\>)(\{\.([a-zA-Z0-9_.-]+)\})', 
                     lambda m: process_multiple_classes(m.group(1), m.group(3)), 
                     html)
        
        return html
    except Exception as e:
        print(f"Error processing class annotations: {str(e)}")
        return html

def process_multiple_classes(tag, classes_str):
    """
    Process multiple classes separated by dots in a class annotation.
    
    Parameters:
    - tag: The HTML tag
    - classes_str: String of classes separated by dots (e.g., 'class1.class2')
    
    Returns:
    - HTML tag with class attribute
    """
    classes = classes_str.split('.')
    class_attr = ' class="' + ' '.join(classes) + '"'
    
    # Add class attribute to tag
    if ' class="' in tag:
        # Append to existing class attribute
        tag = re.sub(r' class="([^"]*)"', lambda m: f' class="{m.group(1)} {" ".join(classes)}"', tag)
    else:
        # Add new class attribute
        tag = tag[:-1] + class_attr + tag[-1:]
    
    return tag
