"""
Tests for HTML minification functionality.
"""

import unittest
from simple_ssg.enhancers.minifier import minify_html


class TestHtmlMinifier(unittest.TestCase):
    def test_basic_minification(self):
        """Test basic HTML minification."""
        html = """
        <html>
            <head>
                <title>Test</title>
            </head>
            <body>
                <h1>Hello World</h1>
                <p>This is a test.</p>
            </body>
        </html>
        """
        
        minified = minify_html(html)
        
        # Should remove extra whitespace
        self.assertNotIn('    ', minified)
        self.assertNotIn('\n        ', minified)
        
        # Should preserve content
        self.assertIn('<title>Test</title>', minified)
        self.assertIn('<h1>Hello World</h1>', minified)
        self.assertIn('<p>This is a test.</p>', minified)
    
    def test_comment_removal(self):
        """Test that HTML comments are removed."""
        html = """
        <html>
            <!-- This is a comment -->
            <body>
                <h1>Content</h1>
                <!-- Another comment -->
                <p>Text</p>
            </body>
        </html>
        """
        
        minified = minify_html(html)
        
        # Comments should be removed
        self.assertNotIn('<!-- This is a comment -->', minified)
        self.assertNotIn('<!-- Another comment -->', minified)
        
        # Content should remain
        self.assertIn('<h1>Content</h1>', minified)
        self.assertIn('<p>Text</p>', minified)
    
    def test_conditional_comments_preserved(self):
        """Test that IE conditional comments are preserved."""
        html = """
        <html>
            <!--[if IE]>
                <p>This is IE</p>
            <![endif]-->
            <!-- Regular comment -->
            <body>Content</body>
        </html>
        """
        
        minified = minify_html(html)
        
        # Conditional comments should be preserved
        self.assertIn('<!--[if IE]>', minified)
        self.assertIn('<![endif]-->', minified)
        
        # Regular comments should be removed
        self.assertNotIn('<!-- Regular comment -->', minified)
    
    def test_whitespace_between_tags(self):
        """Test whitespace removal between tags."""
        html = "<div>   <span>   Content   </span>   </div>"
        
        minified = minify_html(html)
        
        # Should remove whitespace between tags but preserve inner content
        self.assertIn('<div><span>', minified)
        self.assertIn('</span></div>', minified)
        self.assertIn('Content', minified)
    
    def test_regex_escaping_fix(self):
        """Test that regex patterns are properly escaped."""
        # This tests the specific fix made for f-string regex patterns
        html = """
        <div>
            <p>   Content   </p>
            <h1>   Title   </h1>
        </div>
        """
        
        minified = minify_html(html)
        
        # Should properly handle regex patterns without syntax warnings
        self.assertIn('<p>Content</p>', minified)
        self.assertIn('<h1>Title</h1>', minified)
        
        # No extra whitespace around these tags
        self.assertNotIn('<p>   ', minified)
        self.assertNotIn('   </p>', minified)
        self.assertNotIn('<h1>   ', minified)
        self.assertNotIn('   </h1>', minified)
    
    def test_complex_html_structure(self):
        """Test minification with complex nested HTML."""
        html = """
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="UTF-8">
                <title>Complex Page</title>
            </head>
            <body>
                <header>
                    <nav>
                        <ul>
                            <li><a href="/">Home</a></li>
                            <li><a href="/about">About</a></li>
                        </ul>
                    </nav>
                </header>
                <main>
                    <section>
                        <article>
                            <h1>Article Title</h1>
                            <p>Paragraph content with <strong>bold</strong> text.</p>
                        </article>
                    </section>
                </main>
                <footer>
                    <p>&copy; 2025 Test Site</p>
                </footer>
            </body>
        </html>
        """
        
        minified = minify_html(html)
        
        # Should preserve DOCTYPE
        self.assertIn('<!DOCTYPE html>', minified)
        
        # Should preserve nested structure logically
        self.assertIn('<nav><ul><li>', minified)
        self.assertIn('<main><section><article>', minified)
        
        # Should preserve content
        self.assertIn('Article Title', minified)
        self.assertIn('Paragraph content', minified)
        self.assertIn('&copy; 2025 Test Site', minified)
        
        # Should remove excessive whitespace
        self.assertLess(len(minified), len(html))
    
    def test_tag_specific_whitespace_removal(self):
        """Test whitespace removal around specific HTML tags."""
        test_tags = [
            ('div', '<div>   Content   </div>'),
            ('section', '<section>   Content   </section>'),
            ('header', '<header>   Content   </header>'),
            ('footer', '<footer>   Content   </footer>'),
            ('nav', '<nav>   Content   </nav>'),
            ('main', '<main>   Content   </main>'),
            ('article', '<article>   Content   </article>'),
            ('aside', '<aside>   Content   </aside>'),
            ('h1', '<h1>   Title   </h1>'),
            ('h2', '<h2>   Title   </h2>'),
            ('ul', '<ul>   <li>Item</li>   </ul>'),
            ('ol', '<ol>   <li>Item</li>   </ol>'),
            ('li', '<li>   Item   </li>'),
            ('p', '<p>   Text   </p>')
        ]
        
        for tag_name, html_input in test_tags:
            with self.subTest(tag=tag_name):
                minified = minify_html(html_input)
                
                # Should remove leading/trailing whitespace around the tag
                self.assertNotIn(f'<{tag_name}>   ', minified, 
                                f"Leading whitespace not removed for {tag_name}")
                self.assertNotIn(f'   </{tag_name}>', minified, 
                                f"Trailing whitespace not removed for {tag_name}")
    
    def test_error_handling(self):
        """Test error handling in minification."""
        # Test with malformed HTML
        malformed_html = "<div><p>Unclosed paragraph<div>Nested incorrectly</p></div>"
        
        # Should not raise an exception
        try:
            result = minify_html(malformed_html)
            self.assertIsInstance(result, str)
        except Exception as e:
            self.fail(f"Minification should handle malformed HTML gracefully: {e}")
    
    def test_empty_and_none_input(self):
        """Test handling of empty and None input."""
        # Empty string
        self.assertEqual(minify_html(""), "")
        
        # None input should be handled gracefully and return original input
        result = minify_html(None)
        self.assertEqual(result, None)  # Should return None as fallback
    
    def test_whitespace_preservation_in_content(self):
        """Test that meaningful whitespace in content is preserved."""
        html = "<p>This is a sentence with multiple words.</p>"
        
        minified = minify_html(html)
        
        # Spaces between words should be preserved
        self.assertIn("sentence with multiple", minified)
        self.assertIn("multiple words", minified)
    
    def test_special_characters_handling(self):
        """Test handling of special characters and entities."""
        html = """
        <div>
            <p>Special chars: &amp; &lt; &gt; &quot; &#39;</p>
            <p>Unicode: café résumé</p>
        </div>
        """
        
        minified = minify_html(html)
        
        # Special characters should be preserved
        self.assertIn('&amp; &lt; &gt; &quot; &#39;', minified)
        self.assertIn('café résumé', minified)


if __name__ == '__main__':
    unittest.main()