"""
Configuration handling for Simple-SSG.
"""

import os
import sys
import json
import yaml

class SiteConfig:
    """
    Configuration for site generation.
    Handles loading from file or dictionary and setting defaults.
    """
    
    def __init__(self, config_file=None, config_dict=None):
        """
        Initialize configuration from file or dictionary.
        
        Parameters:
        - config_file: Path to a YAML/JSON configuration file
        - config_dict: Dictionary containing configuration values
        """
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
    
    def set_defaults(self):
        """Set default configuration values."""
        # Basic paths
        self.content_dir = 'content'
        self.template_path = 'template.html'
        self.output_dir = 'build'
        self.static_dirs = ['css', 'images', 'js']
        self.index_path = 'index.html'
        
        # Build options
        self.clean_output = True
        self.minify = True
        self.wrap_sections = True
        
        # Section wrapping
        self.h1_section_class = 'hero'
        self.h2_section_class = 'section'
        
        # Template settings
        self.content_placeholder = '<div id="content-container">'
        self.title_placeholder = '<title>'
        self.description_placeholder = '<meta name="description" content="'
        
        # Image paths
        self.image_path_replacements = {
            '../images/': 'images/'
        }
        
        # SEO settings
        self.base_url = 'https://example.com'
        self.generate_sitemap = True
        self.generate_robots = True
        self.generate_htaccess = True
        
        # Markdown extensions
        self.markdown_extensions = ['extra', 'tables', 'smarty']
    
    def load_from_file(self, config_file):
        """Load configuration from a file."""
        try:
            if not os.path.exists(config_file):
                print(f"Error: Configuration file {config_file} not found.")
                sys.exit(1)
            
            with open(config_file, 'r', encoding='utf-8') as f:
                if config_file.endswith(('.yaml', '.yml')):
                    config = yaml.safe_load(f)
                elif config_file.endswith('.json'):
                    config = json.load(f)
                else:
                    print(f"Error: Unsupported configuration file format: {config_file}")
                    sys.exit(1)
            
            self.update_from_dict(config)
            
        except Exception as e:
            print(f"Error loading configuration file: {str(e)}")
            sys.exit(1)
    
    def update_from_dict(self, config_dict):
        """Update configuration from a dictionary."""
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                print(f"Warning: Unknown configuration option: {key}")
    
    def validate(self):
        """Validate the configuration."""
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
                print(f"Warning: Static directory {static_dir} does not exist. It will be skipped.")
        
        # Validate base URL for SEO features
        if self.generate_sitemap or self.generate_robots:
            if not self.base_url or self.base_url == 'https://example.com':
                print("Warning: Using default base URL (https://example.com) for sitemap and robots.txt.")
