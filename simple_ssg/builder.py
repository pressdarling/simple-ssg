"""Core build functionality for Simple-SSG.

This module contains the main logic for building a static site. It orchestrates
the process of reading content, converting it to HTML, applying templates, and
writing the final output to the build directory. It is the central component
that brings together all other parts of the system, such as configuration,
converters, and enhancers.
"""

import os
import sys
import re
import shutil
from datetime import datetime
from typing import Optional, Dict, Any, List

from simple_ssg.converters.markdown import convert_markdown_to_html
from simple_ssg.utils.fs import ensure_dir, copy_static_assets
from simple_ssg.utils.templates import inject_content
from simple_ssg.enhancers.seo import (
    generate_sitemap,
    create_robots_txt,
    create_htaccess,
)
from simple_ssg.enhancers.minifier import minify_html
from simple_ssg.config import SiteConfig


def build_site(
    config_file: Optional[str] = None, config_dict: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Builds the static site based on the provided configuration.

    This is the main entry point for the site generation process. It loads the
    configuration, sets up the build environment, processes content files, and
    runs any specified enhancers.

    Args:
        config_file: The path to a YAML or JSON configuration file.
        config_dict: A dictionary containing configuration values.

    Returns:
        A dictionary containing statistics about the build process, such as
        the number of processed files, errors, and total build time.
    """
    # Load configuration
    config = SiteConfig(config_file, config_dict)

    print(f"Building site at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # Stats for reporting
    stats: Dict[str, Any] = {
        "processed": 0,
        "errors": 0,
        "start_time": datetime.now(),
    }

    try:
        # Set up build directory
        setup_build_dir(config)

        # Process content files
        content_files = get_content_files(config.content_dir)

        for content_path in content_files:
            if process_content_file(content_path, config):
                stats["processed"] += 1
            else:
                stats["errors"] += 1

        # Generate additional files
        if config.generate_sitemap:
            generate_sitemap(config)

        if config.generate_robots:
            create_robots_txt(config)

        if config.generate_htaccess:
            create_htaccess(config)

        # Calculate build time
        stats["end_time"] = datetime.now()
        stats["build_time"] = (
            stats["end_time"] - stats["start_time"]
        ).total_seconds()

        # Print build summary
        print_build_summary(stats, config)

        return stats

    except Exception as e:
        print(f"Error building site: {str(e)}")
        stats["errors"] += 1
        stats["end_time"] = datetime.now()
        stats["build_time"] = (
            stats["end_time"] - stats["start_time"]
        ).total_seconds()
        stats["fatal_error"] = str(e)
        return stats


def setup_build_dir(config: SiteConfig) -> None:
    """Sets up the build directory and copies static assets.

    This function prepares the output directory by cleaning it (if configured),
    creating it, and copying all static assets (e.g., CSS, JS, images) into it.

    Args:
        config: The site configuration object.

    Raises:
        SystemExit: If an error occurs during the setup process.
    """
    try:
        # Remove existing build directory if it exists
        if os.path.exists(config.output_dir):
            if config.clean_output:
                shutil.rmtree(config.output_dir)
            else:
                print(
                    f"Warning: Output directory {config.output_dir} exists "
                    "and clean_output=False. Files may be overwritten."
                )

        # Create build directory
        ensure_dir(config.output_dir)

        # Copy static assets
        copy_static_assets(config.static_dirs, config.output_dir)

        # Copy index.html if specified
        if config.index_path and os.path.exists(config.index_path):
            shutil.copy2(
                config.index_path, os.path.join(config.output_dir, "index.html")
            )

    except Exception as e:
        print(f"Error setting up build directory: {str(e)}")
        sys.exit(1)


def get_content_files(content_dir: str) -> List[str]:
    """Retrieves all content files from the specified directory.

    This function walks through the content directory and collects all files
    with `.md` or `.markdown` extensions, excluding any `README.md` files.

    Args:
        content_dir: The path to the directory containing content files.

    Returns:
        A list of paths to the content files.
    """
    content_files = []

    for root, _, files in os.walk(content_dir):
        for file in files:
            if file.endswith((".md", ".markdown")) and not file == "README.md":
                content_files.append(os.path.join(root, file))

    return content_files


def process_content_file(content_path: str, config: SiteConfig) -> bool:
    """Processes a single content file and generates the corresponding HTML file.

    This function reads a content file, converts it to HTML, injects it into
    the main template, and writes the final HTML to the output directory.

    Args:
        content_path: The path to the content file to process.
        config: The site configuration object.

    Returns:
        True if the file was processed successfully, False otherwise.
    """
    try:
        # Determine output path
        rel_path = os.path.relpath(content_path, config.content_dir)
        base_name = os.path.splitext(rel_path)[0]
        output_path = os.path.join(config.output_dir, f"{base_name}.html")

        # Create output directory if it doesn't exist
        ensure_dir(os.path.dirname(output_path))

        # Read content file
        try:
            with open(content_path, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError:
            print(
                f"Error: File {content_path} has encoding issues. "
                "Try saving as UTF-8."
            )
            return False

        # Determine converter based on file extension
        if content_path.endswith((".md", ".markdown")):
            # Fix image paths
            content = fix_image_paths(content, config)

            # Convert content to HTML
            html_content = convert_markdown_to_html(content, config)

            # Wrap sections if enabled
            if config.wrap_sections:
                html_content = wrap_sections(html_content, config)
        else:
            print(f"Warning: Unsupported file type: {content_path}")
            return False

        # Inject content into template
        page_html = inject_content(html_content, content_path, config)

        # Minify HTML if enabled
        if config.minify:
            page_html = minify_html(page_html)

        # Write to output file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page_html)

        print(
            f"Processed {os.path.basename(content_path)} "
            f"→ {os.path.basename(output_path)}"
        )
        return True

    except Exception as e:
        print(f"Error processing {content_path}: {str(e)}")
        return False


def fix_image_paths(content: str, config: SiteConfig) -> str:
    """Corrects image paths in the content based on configuration.

    This function replaces placeholder paths in image links with their final
    paths, making them work correctly in the generated site.

    Args:
        content: The string content to process.
        config: The site configuration object.

    Returns:
        The content with image paths corrected.
    """
    # Replace relative image paths with paths to the image directory
    if config.image_path_replacements:
        for orig, repl in config.image_path_replacements.items():
            content = content.replace(orig, repl)

    return content


def wrap_sections(html: str, config: SiteConfig) -> str:
    """Wraps HTML content in <section> tags based on heading levels.

    This function automatically wraps content under `<h1>` and `<h2>` tags
    with `<section>` elements, applying CSS classes from the configuration.
    This is useful for styling and structuring the final page.

    Args:
        html: The HTML content to process.
        config: The site configuration object.

    Returns:
        The HTML content with sections wrapped.
    """
    try:
        # Find h1 sections and wrap them
        html = re.sub(
            r"(<h1.*?</h1>)([\s\S]*?)(?=<h2|$)",
            lambda m: f'<section class="{config.h1_section_class}">'
            f"{m.group(1)}{m.group(2)}</section>",
            html,
        )

        # Find h2 sections and wrap them
        html = re.sub(
            r"(<h2.*?</h2>)([\s\S]*?)(?=<h2|$)",
            lambda m: f'<section class="{config.h2_section_class}">'
            f"{m.group(1)}{m.group(2)}</section>",
            html,
        )

        return html
    except Exception as e:
        print(f"Error wrapping sections: {str(e)}")
        return html


def print_build_summary(stats: Dict[str, Any], config: SiteConfig) -> None:
    """Prints a summary of the build process to the console.

    Args:
        stats: A dictionary containing build statistics.
        config: The site configuration object.
    """
    print("\nBuild Summary:")
    print(f"- Files processed successfully: {stats['processed']}")
    if stats["errors"] > 0:
        print(f"- Files with errors: {stats['errors']}")
    print(f"- Output directory: {os.path.abspath(config.output_dir)}")
    print(f"- Build time: {stats['build_time']:.2f} seconds")
    print(f"- HTML minification: {'Enabled' if config.minify else 'Disabled'}")

    print("\nBuild complete!")
