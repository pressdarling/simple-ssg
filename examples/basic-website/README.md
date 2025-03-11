# Simple-SSG Basic Website Example

This example demonstrates a minimal website built with Simple-SSG, showing the essential features and configuration options.

## Project Structure

```
./
├── config.yaml       # Simple-SSG configuration
├── content/          # Markdown content files
│   ├── 404.md        # Error page
│   ├── about.md      # About page
│   ├── contact.md    # Contact page
│   └── index.md      # Home page
├── css/              # Stylesheets
│   └── styles.css    # Main stylesheet
├── images/           # Image directory (empty)
├── template.html     # HTML template
└── index.html        # Entry point (for testing)
```

## Features Demonstrated

This example demonstrates several key Simple-SSG features:

1. **Markdown Content** - Using Markdown for content with front matter
2. **HTML Template** - Single template for consistent design
3. **CSS Integration** - Styling with a separate CSS file
4. **Configuration** - Basic Simple-SSG configuration
5. **Static Assets** - Managing static assets like CSS and images

## Getting Started

### Building the Example

To build this example:

```bash
# Navigate to the example directory
cd basic-website

# Build the site using the Simple-SSG CLI
simple-ssg build

# The built site will be in the 'build' directory
```

### Serving the Example

To serve the example locally:

```bash
# Serve the site on localhost:8000
simple-ssg serve
```

### Modifying the Example

1. **Edit Content** - Modify the Markdown files in the `content` directory
2. **Update Template** - Edit `template.html` to change the design
3. **Customize Styles** - Modify `css/styles.css` for styling
4. **Configure** - Adjust `config.yaml` for different build options

## Configuration Details

The `config.yaml` file contains basic Simple-SSG configuration:

```yaml
# Basic paths
content_dir: content
template_path: template.html
output_dir: build
static_dirs:
  - css
  - images
index_path: index.html

# Build options
clean_output: true
minify: true
wrap_sections: true

# SEO settings
site_name: "Simple-SSG Example"
site_description: "A basic website example using Simple-SSG"
generate_sitemap: true
generate_robots: true
```

## Template System

The template (`template.html`) demonstrates:

1. **Variable Substitution** - Using `{{title}}`, `{{content}}`, etc.
2. **Metadata Handling** - SEO tags from front matter
3. **Content Injection** - Where content is placed in the template

## Content Format

Content files use Markdown with YAML front matter:

```markdown
---
title: "Page Title"
description: "Page description for SEO"
---

# Page Heading

Page content in Markdown format.

## Section Heading

More content with **formatting** and [links](another-page.html).
```

## Learning Path

After exploring this example, consider:

1. **Advanced Features** - Try adding more advanced Simple-SSG features
2. **Custom Styling** - Experiment with more complex CSS
3. **Multiple Templates** - Create different templates for different page types
4. **Content Organization** - Organize content into subdirectories
5. **Deployment** - Deploy the built site to a web host

## Related Resources

- [Simple-SSG Documentation](../../docs/README.md) - Complete package documentation
- [Examples Directory](../) - More Simple-SSG examples
- [Getting Started Guide](../../docs/getting-started.md) - Detailed guide for beginners
