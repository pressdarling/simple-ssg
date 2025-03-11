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
    if md_content is None:
        return "<p>Error: Markdown content is None</p>"
        
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
    except AttributeError as e:
        error_msg = f"Error in configuration: {str(e)}"
        print(error_msg)
        return f"<p>{error_msg}</p>"
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
        # Much simpler approach that actually works:
        # Match patterns like: <h1>Test Heading</h1>{.test-class}
        # Regex explanation:
        # (<(\w+)[^>]*>    # Group 1: Captures opening tag like <h1> or <div class="something">
        #                   # Group 2: Captures just the tag name (h1, div, etc.)
        # (.*?)            # Group 3: Captures the content between tags
        # <\/\2>           # Closing tag that matches the opening tag
        # )\{\.([^}]+)\}   # Group 4: Captures the class name(s) without the {. and }
        
        # Pattern for matching tags with class annotations
        # This isn't a proper HTML parser, so it doesn't handle nested tags correctly
        # and can be confused by more complex HTML structures. Consider replacing
        # with a proper HTML parser like BeautifulSoup in a future version.
        pattern = r'(<(\w+)[^>]*>(.*?)<\/\2>)\{\.([^}]+)\}'
        
        # Process the replacement
        def replace_class(match):
            full_tag = match.group(1)  # The complete tag with content
            tag_name = match.group(2)  # Just the tag name (h1, div, etc.)
            content = match.group(3)   # The content between tags
            classes = match.group(4)   # The class names (test-class or class1.class2)
            
            # Handle multiple classes separated by dots
            class_list = classes.split('.')
            class_attr = f'class="{" ".join(class_list)}"'
            
            # Check if the tag already has a class attribute
            opening_tag_match = re.search(r'<' + tag_name + r'([^>]*?)(class=["\']([^"\']*)["\'](.*?))?>', full_tag)
            
            if opening_tag_match and opening_tag_match.group(2):
                # Tag has existing class attribute, need to merge
                existing_classes = opening_tag_match.group(3)
                prefix = opening_tag_match.group(1) or ''
                suffix = opening_tag_match.group(4) or ''
                
                # Create a new opening tag with merged classes
                new_opening = f'<{tag_name}{prefix}class="{existing_classes} {".join(class_list)}"{suffix}>'
                modified_tag = full_tag.replace(opening_tag_match.group(0), new_opening)
            else:
                # Tag doesn't have a class attribute, just add it
                modified_tag = re.sub(r'<' + tag_name + '([^>]*)>', 
                                 lambda m: f'<{tag_name}{m.group(1)} {class_attr}>', 
                                 full_tag)
            
            return modified_tag
        
        # Apply the replacement
        html = re.sub(pattern, replace_class, html)
        
        return html
    except Exception as e:
        print(f"Error processing class annotations: {str(e)}")
        return html



