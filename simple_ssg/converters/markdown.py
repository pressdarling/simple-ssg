"""Markdown converter for Simple-SSG.

This module provides the functionality to convert Markdown content into HTML.
It uses the `markdown` library and extends its functionality with a custom
post-processing step to handle special class annotations. This allows users
to add CSS classes to HTML elements directly from their Markdown files.
"""

import re
from typing import Optional

import markdown

from simple_ssg.config import SiteConfig


def convert_markdown_to_html(
    md_content: str, config: Optional[SiteConfig] = None
) -> str:
    """Converts a string of Markdown content to HTML.

    This function takes Markdown text, processes it using the `markdown`
    library with extensions specified in the configuration, and then runs a
    post-processing step to handle custom class annotations.

    Args:
        md_content: The Markdown content to be converted.
        config: The site configuration object, which contains settings like
                Markdown extensions.

    Returns:
        The converted HTML as a string. Returns an error message in a <p> tag
        if conversion fails.
    """
    if md_content is None:
        return "<p>Error: Markdown content is None</p>"

    try:
        # Get markdown extensions from config or use defaults
        extensions = (
            config.markdown_extensions if config else ["extra", "tables", "smarty"]
        )

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


def process_class_annotations(html: str) -> str:
    """Processes custom class annotations in generated HTML.

    This function finds patterns like `...</h1>{.classname}` and injects a
    `class="classname"` attribute into the preceding HTML tag. This allows for
    a simple, Markdown-friendly way to style elements.

    The regex used is a best-effort approach and may not handle all complex,
    nested HTML structures. It is designed to work with the typical output of
    a Markdown converter.

    Args:
        html: The HTML content to process.

    Returns:
        The HTML content with class attributes added to annotated tags.
    """
    try:
        # Regex to find a complete HTML tag followed by a class annotation.
        # Example: `<h1>Title</h1>{.title-class}`
        # Explanation:
        # (<(\w+)[^>]*>(.*?)<\/\2>) - Group 1: The full HTML tag and content.
        #   <(\w+)[^>]*>             - An opening tag, capturing the tag name in Group 2.
        #   (.*?)                    - The content inside the tag (non-greedy).
        #   <\/\2>                   - The matching closing tag.
        # \{\.([^}]+)\}              - Group 4: The class name(s) inside `{.}`.
        pattern = r"(<(\w+)[^>]*>(.*?)<\/\2>)\{\.([^}]+)\}"

        def replace_class(match: re.Match) -> str:
            """
            Callback function to replace the matched annotation with a class
            attribute.
            """
            full_tag_html = match.group(1)  # The complete tag with content, e.g., `<h1>...</h1>`
            tag_name = match.group(2)  # The tag name, e.g., `h1`
            class_names = match.group(4)  # The class name(s), e.g., `my-class.another`

            # Format the class attribute string
            class_list = class_names.split(".")
            class_attr = f'class="{" ".join(class_list)}"'

            # Find the opening tag to modify it.
            opening_tag_match = re.search(r"<\s*" + tag_name + r"[^>]*>", full_tag_html)
            if not opening_tag_match:
                return full_tag_html  # Should not happen with the current pattern

            opening_tag = opening_tag_match.group(0)
            modified_tag = ""

            # Check if the tag already has a class attribute
            if "class=" in opening_tag:
                # If it does, append the new classes to the existing ones.
                def append_classes(m: re.Match) -> str:
                    existing_classes = m.group(1)
                    return f'class="{existing_classes} {" ".join(class_list)}"'

                modified_tag = re.sub(r'class="([^"]*)"', append_classes, opening_tag)
            else:
                # Otherwise, add the new class attribute.
                modified_tag = opening_tag.replace(
                    f"<{tag_name}", f"<{tag_name} {class_attr}"
                )

            return full_tag_html.replace(opening_tag, modified_tag)

        # Apply the replacement for all annotations found
        html = re.sub(pattern, replace_class, html)

        return html
    except Exception as e:
        print(f"Error processing class annotations: {str(e)}")
        return html



