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
    
    def test_markdown_class_annotation_complex_nested(self):
        """Test complex nested class annotations that previously caused f-string issues."""
        test_cases = [
            # Multiple classes with dots
            ('<h1>Title</h1>{.class1.class2.class3}', 'class="class1 class2 class3"'),
            
            # Class annotation with existing attributes
            ('<div class="existing" id="test">Content</div>{.new}', 'class="existing new"'),
            
            # Nested tags with class annotations
            ('<div><h1>Title</h1>{.header-class}</div>', 'class="header-class"'),
            
            # Complex tag with multiple attributes
            ('<h1 id="title" data-test="value" class="existing">Title</h1>{.new.extra}', 
             'class="existing new extra"'),
        ]
        
        for html_input, expected_class in test_cases:
            with self.subTest(html=html_input):
                processed = process_class_annotations(html_input)
                self.assertIn(expected_class, processed, 
                            f"Failed to process: {html_input}")
    
    def test_f_string_edge_cases(self):
        """Test edge cases that previously caused f-string syntax errors."""
        # Test case that had nested quotes in f-string
        html = '<h1 class="existing-class" id="test">Title</h1>{.new-class.another}'
        
        # This should not raise a SyntaxError
        try:
            result = process_class_annotations(html)
            self.assertIn('class="existing-class new-class another"', result)
        except SyntaxError as e:
            self.fail(f"F-string syntax error should be fixed: {e}")
    
    def test_class_annotation_with_special_characters(self):
        """Test class annotations with special characters and edge cases."""
        test_cases = [
            # Class names with hyphens and underscores
            ('<p>Text</p>{.test-class_name}', 'class="test-class_name"'),
            
            # Multiple classes with various separators
            ('<div>Content</div>{.class1.class-2.class_3}', 'class="class1 class-2 class_3"'),
            
            # Empty class annotation (should be handled gracefully)
            ('<span>Text</span>{.}', '<span>Text</span>{.}'),  # Should remain unchanged
        ]
        
        for html_input, expected in test_cases:
            with self.subTest(html=html_input):
                result = process_class_annotations(html_input)
                if expected.startswith('class='):
                    self.assertIn(expected, result)
                else:
                    self.assertEqual(expected, result)
    
    def test_stress_testing_markdown_processing(self):
        """Stress test markdown processing with complex scenarios."""
        complex_markdown = """
        # Main Title {.hero-title}
        
        This is a paragraph with **bold** and *italic* text.
        
        ## Section One {.section.primary}
        
        Here's a list:
        - Item 1
        - Item 2 {.special-item}
        - Item 3
        
        ### Subsection {.subsection.highlighted}
        
        A blockquote:
        > This is a quote {.quote-style}
        
        And a [link](https://example.com){.external-link} in text.
        
        ```python
        # Code block
        def hello():
            return "world"
        ```
        
        ## Section Two {.section.secondary}
        
        Another paragraph with multiple **formatting** *options* and `inline code`.
        """
        
        # Should process without errors
        try:
            result = convert_markdown_to_html(complex_markdown)
            
            # Verify key content is present
            self.assertIn('<h1', result)
            self.assertIn('<h2', result)
            self.assertIn('<h3', result)
            self.assertIn('<strong>bold</strong>', result)
            self.assertIn('<em>italic</em>', result)
            self.assertIn('<code>inline code</code>', result)
            self.assertIn('<blockquote>', result)
            
            # Verify class annotations were processed
            self.assertIn('class="hero-title"', result)
            self.assertIn('class="section primary"', result)
            self.assertIn('class="subsection highlighted"', result)
            
        except Exception as e:
            self.fail(f"Complex markdown processing should not fail: {e}")

class TestHtmlConverter(unittest.TestCase):
    def test_html_passthrough(self):
        """Test HTML passthrough."""
        html = '<h1>Test Heading</h1><p>This is a test paragraph.</p>'
        result = convert_html_to_html(html)
        
        self.assertEqual(result, html)

if __name__ == '__main__':
    unittest.main()
