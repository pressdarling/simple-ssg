# About Simple-SSG

Simple-SSG is a minimalist static site generator designed to be simple, understandable, and customizable.

## Why Simple-SSG?

There are many static site generators available, but Simple-SSG focuses on:

### Simplicity

The entire codebase is small and easy to understand. There are no complex dependencies or configurations required.

### Markdown-Driven

Content is written in Markdown, which is easy to read and write. Simple-SSG adds a few enhancements like class annotations.

### Customizability

The template system is straightforward and can be customized to fit your needs. The build process can be extended with custom plugins.

### Deployment Flexibility

The output is just static HTML, CSS, and optional JavaScript, which can be deployed to any web host, including GitHub Pages, Netlify, and traditional hosting.

## How It Works

Simple-SSG works by:

1. Reading Markdown files from the content directory
2. Converting them to HTML using Python-Markdown
3. Wrapping sections based on heading structure
4. Injecting the content into an HTML template
5. Generating a sitemap and other SEO enhancements
6. Outputting the result to the build directory

## Getting Started

To get started with Simple-SSG:

```bash
# with uv (preferred)
uvx simple-ssg

# otherwise:
pip install simple-ssg

# Create a new project
simple-ssg init my-site

# Build the site
cd my-site
simple-ssg build

# Serve the site locally
simple-ssg serve
```

## Learn More

Check out the [Simple-SSG GitHub repository](https://github.com/bradyclarke/simple-ssg) for more information.

[Back to Home](index.html){.button}
