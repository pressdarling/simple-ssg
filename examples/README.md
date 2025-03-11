# Simple-SSG Examples

This directory contains example projects built with Simple-SSG to demonstrate its capabilities and usage patterns.

## Example Projects

- [**basic-website**](basic-website/) - A minimal website demonstrating core Simple-SSG features

## Basic Website Example

The [basic-website](basic-website/) example demonstrates a minimal Simple-SSG project with:

- Content files (Markdown)
- HTML template
- CSS styling
- Configuration
- Build output

### Directory Structure

```
basic-website/
├── config.yaml       # Configuration file
├── content/          # Markdown content
│   ├── index.md      # Home page
│   ├── about.md      # About page
│   ├── contact.md    # Contact page
│   └── 404.md        # Error page
├── css/              # Stylesheets
│   └── styles.css    # Main stylesheet
├── images/           # Image directory (empty)
├── template.html     # HTML template
└── index.html        # Entry point
```

### Running the Example

To build and run the example:

```bash
# Navigate to the example directory
cd basic-website

# Build the site using Simple-SSG CLI
simple-ssg build

# Serve the site locally
simple-ssg serve
```

### Key Features Demonstrated

The basic website example demonstrates several key Simple-SSG features:

1. **Content Management**

   - Markdown content with frontmatter
   - Automatic conversion to HTML
   - Section wrapping based on headings

2. **Template System**

   - Single template for consistent design
   - Variable substitution from frontmatter
   - Content injection

3. **Configuration**

   - Configuration file with build settings
   - Static directory specification
   - Build options

4. **CSS Integration**
   - Static asset copying
   - Basic styling
   - Class annotations

## Creating Your Own Examples

You can use these examples as starting points for your own projects:

1. **Copy an Example**: Copy one of the example directories
2. **Customize Content**: Edit the Markdown files in the `content` directory
3. **Update Template**: Modify the `template.html` file to change the design
4. **Configure**: Adjust the `config.yaml` file as needed
5. **Build**: Run `simple-ssg build` to generate the site

## Example Usage in Documentation

These examples are referenced in the Simple-SSG documentation:

- [Getting Started Guide](../docs/getting-started.md) uses the basic-website example
- [Integration Guide](../docs/integration-guide.md) shows how to adapt these examples

## Contributing Examples

If you create a useful example, consider contributing it back to the Simple-SSG project:

1. Create a new directory in `examples/`
2. Add a README.md explaining the example
3. Include all necessary files (content, template, config)
4. Ensure the example is self-contained and easily runnable
5. Submit a pull request

For more information about Simple-SSG, see the [Simple-SSG Documentation](../docs/README.md).
