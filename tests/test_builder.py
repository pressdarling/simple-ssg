"""
Tests for the builder module.
"""

import os
import shutil
import tempfile
import unittest
from simple_ssg.builder import build_site
from simple_ssg.config import SiteConfig

class TestBuilder(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.content_dir = os.path.join(self.test_dir, 'content')
        self.output_dir = os.path.join(self.test_dir, 'build')
        
        # Create content directory
        os.makedirs(self.content_dir)
        
        # Create a simple template file
        self.template_path = os.path.join(self.test_dir, 'template.html')
        with open(self.template_path, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n'
                    '<html>\n'
                    '<head><title>Test</title></head>\n'
                    '<body>\n'
                    '<div id="content-container"><div class="loading">Loading...</div></div>\n'
                    '</body>\n'
                    '</html>')
    
    def tearDown(self):
        # Clean up temp directory
        shutil.rmtree(self.test_dir)
    
    def test_empty_site_build(self):
        """Test building an empty site."""
        # Create a test config
        config_dict = {
            'content_dir': self.content_dir,
            'template_path': self.template_path,
            'output_dir': self.output_dir,
            'static_dirs': [],
            'base_url': 'http://example.com',
            'minify': False
        }
        
        # Build the site
        stats = build_site(config_dict=config_dict)
        
        # Check that the output directory was created
        self.assertTrue(os.path.exists(self.output_dir))
        
        # Check stats
        self.assertEqual(stats['processed'], 0)
        self.assertEqual(stats['errors'], 0)
    
    def test_basic_page_build(self):
        """Test building a site with a basic page."""
        # Create a test markdown file
        md_path = os.path.join(self.content_dir, 'test.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write('# Test Page\n\nThis is a test page.')
        
        # Create a test config
        config_dict = {
            'content_dir': self.content_dir,
            'template_path': self.template_path,
            'output_dir': self.output_dir,
            'static_dirs': [],
            'base_url': 'http://example.com',
            'minify': False
        }
        
        # Build the site
        stats = build_site(config_dict=config_dict)
        
        # Check that the output file was created
        output_file = os.path.join(self.output_dir, 'test.html')
        self.assertTrue(os.path.exists(output_file))
        
        # Check stats
        self.assertEqual(stats['processed'], 1)
        self.assertEqual(stats['errors'], 0)
        
        # Check file contents
        with open(output_file, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn('<h1', content)
            self.assertIn('Test Page', content)
            self.assertIn('This is a test page.', content)

if __name__ == '__main__':
    unittest.main()
