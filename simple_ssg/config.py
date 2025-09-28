"""Configuration handling for Simple-SSG.

This module defines the `SiteConfig` class, which is responsible for managing
all configuration settings for the static site generation process. It handles
loading settings from files or dictionaries, setting default values, and
validating the final configuration.
"""

import os
import sys
import json
from typing import Optional, Dict, Any

import yaml


class SiteConfig:
    """Manages site configuration settings.

    This class centralizes all configuration for the site generator. It can be
    initialized from a configuration file (YAML or JSON) or a dictionary. It
    provides default values for all settings, which can be overridden.

    Attributes:
        content_dir (str): Path to the directory containing content files.
        template_path (str): Path to the main HTML template file.
        output_dir (str): Path to the directory where the site will be built.
        static_dirs (list[str]): List of directories containing static assets.
        index_path (str): Path to a root-level index file, if any.
        clean_output (bool): If True, the output directory is cleaned before
                             building.
        minify (bool): If True, the generated HTML is minified.
        wrap_sections (bool): If True, content is wrapped in <section> tags.
        h1_section_class (str): CSS class for sections created from <h1> tags.
        h2_section_class (str): CSS class for sections created from <h2> tags.
        base_url (str): The base URL of the site, used for SEO purposes.
        generate_sitemap (bool): If True, a sitemap.xml file is generated.
        generate_robots (bool): If True, a robots.txt file is generated.
        generate_htaccess (bool): If True, a .htaccess file is generated.
        markdown_extensions (list[str]): List of extensions for the Markdown
                                         converter.
        test_mode (bool): If True, validation of file paths is skipped.
    """

    def __init__(
        self,
        config_file: Optional[str] = None,
        config_dict: Optional[Dict[str, Any]] = None,
        test_mode: bool = False,
    ):
        """Initializes the site configuration.

        The configuration is loaded in the following order:
        1. Default values are set.
        2. If `config_file` is provided, it is loaded, overriding defaults.
        3. If `config_dict` is provided, it is loaded, overriding the file
           configuration.

        Args:
            config_file: The path to a YAML or JSON configuration file.
            config_dict: A dictionary containing configuration values.
            test_mode: If True, skips validation of directories, which is
                       useful for testing purposes.
        """
        # Store test mode flag
        self.test_mode = test_mode

        # Set default values
        self.set_defaults()

        # Load from file if provided
        if config_file:
            self.load_from_file(config_file)

        # Override with dictionary if provided
        if config_dict:
            self.update_from_dict(config_dict)

        # Validate configuration
        self.validate()

    def set_defaults(self) -> None:
        """Sets the default values for all configuration options."""
        # Basic paths
        self.content_dir = "content"
        self.template_path = "template.html"
        self.output_dir = "build"
        self.static_dirs = ["css", "images", "js"]
        self.index_path = "index.html"

        # Build options
        self.clean_output = True
        self.minify = True
        self.wrap_sections = True

        # Section wrapping
        self.h1_section_class = "hero"
        self.h2_section_class = "section"

        # Template settings
        self.content_placeholder = '<div id="content-container">'
        self.title_placeholder = "<title>"
        self.description_placeholder = '<meta name="description" content="'

        # Image paths
        self.image_path_replacements = {"../images/": "images/"}

        # SEO settings
        self.base_url = "https://example.com"
        self.generate_sitemap = True
        self.generate_robots = True
        self.generate_htaccess = True

        # Markdown extensions
        self.markdown_extensions = ["extra", "tables", "smarty"]

    def load_from_file(self, config_file: str) -> None:
        """Loads configuration from a YAML or JSON file.

        Args:
            config_file: The path to the configuration file.

        Raises:
            SystemExit: If the file is not found or cannot be parsed.
        """
        try:
            if not os.path.exists(config_file):
                print(f"Error: Configuration file {config_file} not found.")
                sys.exit(1)

            with open(config_file, "r", encoding="utf-8") as f:
                if config_file.endswith((".yaml", ".yml")):
                    config = yaml.safe_load(f)
                elif config_file.endswith(".json"):
                    config = json.load(f)
                else:
                    print(f"Error: Unsupported configuration file format: {config_file}")
                    sys.exit(1)

            self.update_from_dict(config)

        except Exception as e:
            print(f"Error loading configuration file: {str(e)}")
            sys.exit(1)

    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Updates configuration from a dictionary.

        Only known configuration keys are updated. Unknown keys are ignored,
        and a warning is printed.

        Args:
            config_dict: A dictionary of configuration values.
        """
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Unknown configuration option: {key}")

    def validate(self) -> bool:
        """Validates the configuration to ensure required files and directories exist.

        This method checks for the existence of the content directory and the
        template file. It also warns if static directories are missing.
        Validation is skipped if `test_mode` is True.

        Returns:
            True if the configuration is valid.

        Raises:
            SystemExit: If a required file or directory is not found.
        """
        # Skip validation in test mode
        if self.test_mode:
            return True

        # Check required directories
        if not os.path.exists(self.content_dir):
            print(f"Error: Content directory {self.content_dir} not found.")
            sys.exit(1)

        if not os.path.exists(self.template_path):
            print(f"Error: Template file {self.template_path} not found.")
            sys.exit(1)

        # Check static directories
        for static_dir in self.static_dirs:
            if not os.path.exists(static_dir):
                print(
                    f"Warning: Static directory {static_dir} "
                    "does not exist. It will be skipped."
                )

        # Validate base URL for SEO features
        if self.generate_sitemap or self.generate_robots:
            if not self.base_url or self.base_url == "https://example.com":
                print(
                    "Warning: Using default base URL "
                    "(https://example.com) for sitemap and robots.txt."
                )

        return True
