"""
Tests for the configuration module.
"""

import os
import tempfile
import unittest
from simple_ssg.config import SiteConfig

class TestSiteConfig(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for test files
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        # Clean up temp directory
        os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """Test default configuration values."""
        config = SiteConfig(test_mode=True)
        
        # Check some default values
        self.assertEqual(config.content_dir, 'content')
        self.assertEqual(config.output_dir, 'build')
        self.assertTrue(config.minify)

    def test_config_from_dict(self):
        """Test configuration from dictionary."""
        config_dict = {
            'content_dir': 'pages',
            'output_dir': 'public',
            'minify': False,
            'base_url': 'https://test.com'
        }
        
        config = SiteConfig(config_dict=config_dict, test_mode=True)
        
        # Check values from dictionary
        self.assertEqual(config.content_dir, 'pages')
        self.assertEqual(config.output_dir, 'public')
        self.assertFalse(config.minify)
        self.assertEqual(config.base_url, 'https://test.com')

    def test_update_from_dict(self):
        """Test updating configuration from dictionary."""
        config = SiteConfig(test_mode=True)
        
        # Update with a dictionary
        config.update_from_dict({
            'content_dir': 'custom_content',
            'base_url': 'https://example.org'
        })
        
        # Check updated values
        self.assertEqual(config.content_dir, 'custom_content')
        self.assertEqual(config.base_url, 'https://example.org')
        
        # Check that other values remain unchanged
        self.assertEqual(config.output_dir, 'build')

if __name__ == '__main__':
    unittest.main()
