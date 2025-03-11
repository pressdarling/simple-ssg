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
        
    def test_existing_class_attribute(self):
        """Test processing class annotations when a class attribute already exists."""
        html = '<h1 class="existing">Test Heading</h1>{.new-class}'
        processed = process_class_annotations(html)
        
        # Check that both classes are preserved
        self.assertIn('class="existing new-class"', processed)
        
    def test_config_attribute_error(self):
        """Test handling of AttributeError in configuration."""
        # Create an object with no markdown_extensions attribute
        class BadConfig:
            pass
            
        html = convert_markdown_to_html("# Test", BadConfig())
        self.assertIn('<p>Error in configuration:', html)

class TestHtmlConverter(unittest.TestCase):
    def test_html_passthrough(self):
        """Test HTML passthrough."""
        html = '<h1>Test Heading</h1><p>This is a test paragraph.</p>'
        result = convert_html_to_html(html)
        
        self.assertEqual(result, html)

if __name__ == '__main__':
    unittest.main()
