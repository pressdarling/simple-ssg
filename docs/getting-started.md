# Getting Started with Simple-SSG

This guide will help you get started with Simple-SSG, a minimalist static site generator.

## Installation

Install Simple-SSG using pip:

```bash
pip install simple-ssg
```

## Creating a New Project

Simple-SSG includes a project initialization command that sets up a basic site structure:

```bash
simple-ssg init my-website
cd my-website
```

This creates a new directory with the following structure:

```
my-website/
├── config.yaml           # Configuration file
├── content/              # Markdown content files
│   ├── index.md          # Homepage content
│   ├── about.md          # About page content
│   └── 404.md            # 404 page content
├── css/                  # CSS stylesheets
│   └── styles.css        # Main stylesheet
├── images/               # Image files
├── js/                   # JavaScript files (optional)
└── template.html         # HTML template
```

## Building the Site

To build the site, run:

```bash
simple-ssg build
```

This will process all Markdown files in the `content` directory and output HTML files to the `build` directory.

You can specify a different configuration file with:

```bash
simple-ssg build --config my-config.yaml
```

## Previewing the Site

To preview the site locally, run:

```bash
simple-ssg serve
```

This starts a local development server on port 8000. You can specify a different port with:

```bash
simple-ssg serve --port 8080
```

## Configuration

Simple-SSG can be configured through a YAML or JSON file. Here's an example configuration:

```yaml
# Basic paths
content_dir: content
template_path: template.html
output_dir: build
static_dirs:
  - css
  - images
  - js
index_path: index.html

# Build options
clean_output: true
minify: true
wrap_sections: true

# Section wrapping
h1_section_class: hero
h2_section_class: section

# SEO settings
base_url: https://example.com
generate_sitemap: true
generate_robots: true
generate_htaccess: true

# Markdown extensions
markdown_extensions:
  - extra
  - tables
  - smarty
```

## Writing Content

Simple-SSG uses Markdown for content with some enhancements:

### Basic Markdown

```markdown
# Page Title

This is a paragraph with **bold** and *italic* text.

## Section Title

- List item 1
- List item 2

1. Numbered item 1
2. Numbered item 2

[Link text](url)

![Image alt text](image.jpg)
```

### Class Annotations

You can add CSS classes to elements using the `{.classname}` syntax:

```markdown
# Page Title {.custom-title}

This is a paragraph with a [special link](page.html){.special-link}.

## Section Title {.custom-section}

> This is a blockquote {.quote}
```

This will generate HTML with class attributes:

```html
<h1 class="custom-title">Page Title</h1>

<p>
  This is a paragraph with a
  <a href="page.html" class="special-link">special link</a>.
</p>

<h2 class="custom-section">Section Title</h2>

<blockquote class="quote">This is a blockquote</blockquote>
```

### Automatic Section Wrapping

Simple-SSG automatically wraps content in section tags based on heading structure:

- H1 headings and their content are wrapped in `<section class="hero">...</section>`
- H2 headings and their content are wrapped in `<section class="section">...</section>`

## Templates

Simple-SSG uses a simple template system. The template should include a placeholder for the content:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>My Site</title>
    <link rel="stylesheet" href="css/styles.css" />
  </head>
  <body>
    <header>
      <h1>My Site</h1>
      <nav>
        <a href="index.html">Home</a>
        <a href="about.html">About</a>
      </nav>
    </header>

    <main>
      <div id="content-container">
        <div class="loading">Loading content...</div>
      </div>
    </main>

    <footer>
      <p>&copy; 2025 My Site</p>
    </footer>
  </body>
</html>
```

The content will replace the `div` with the ID `content-container`.

## Deployment

The output of Simple-SSG is just static HTML, CSS, and optional JavaScript, which can be deployed to any web host:

### GitHub Pages

```bash
simple-ssg build
cd build
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/username.github.io.git
git push -u origin main
```

### Netlify

1. Run `simple-ssg build`
2. Drag and drop the `build` directory to Netlify

### Traditional Hosting

Simply upload the contents of the `build` directory to your web host.

## Next Steps

- Checkout the [examples directory](../examples/) for sample projects
- Read the [Integration Guide](integration-guide.md) to learn how to integrate Simple-SSG with other tools
- Explore the [API documentation](api.md) to learn about Simple-SSG's internals
