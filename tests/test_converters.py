"""
Tests for the converters module.
"""

import unittest
from simple_ssg.converters.markdown import convert_markdown_to_html, process_class_annotations
from simple_ssg.converters.html import convert_html_to_html

class TestMarkdownConverter(unittest.TestCase):
    def test_basic_conversion(self):
        """Test basic Markdown to HTML conversion."""
        markdown = "# Test Heading\n\nThis is a test paragraph."
        html = convert_markdown_to_html(markdown)
        
        self.assertIn('<h1>Test Heading</h1>', html)
        self.assertIn('<p>This is a test paragraph.</p>', html)
    
    def test_class_annotations(self):
        """Test class annotations processing."""
        html = '<h1>Test Heading</h1>{.test-class}'
        processed = process_class_annotations(html)
        
        self.assertEqual(processed, '<h1 class="test-class">Test Heading</h1>')
    
    def test_multiple_classes(self):
        """Test processing of multiple classes."""
        html = '<h1>Test Heading</h1>{.class1.class2}'
        processed = process_class_annotations(html)
        
        self.assertIn('class="class1 class2"', processed)
    
    def test_error_handling(self):
        """Test error handling in conversion."""
        # This should not raise an exception
        html = convert_markdown_to_html(None)
        self.assertIn('<p>Error', html)

class TestHtmlConverter(unittest.TestCase):
    def test_html_passthrough(self):
        """Test HTML passthrough."""
        html = '<h1>Test Heading</h1><p>This is a test paragraph.</p>'
        result = convert_html_to_html(html)
        
        self.assertEqual(result, html)

if __name__ == '__main__':
    unittest.main()
