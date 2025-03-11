# Simple-SSG - A Minimalist Static Site Generator

```
simple-ssg/
├── simple_ssg/                  # Python package
│   ├── __init__.py             # Package initialization
│   ├── builder.py              # Core build functionality
│   ├── config.py               # Configuration handling
│   ├── converters/             # Content converters
│   │   ├── __init__.py
│   │   ├── markdown.py         # Markdown converter
│   │   └── html.py             # HTML passthrough
│   ├── enhancers/              # Optional enhancements
│   │   ├── __init__.py
│   │   ├── minifier.py         # HTML minification
│   │   ├── seo.py              # SEO enhancements (sitemap, robots.txt)
│   │   └── server.py           # Local development server
│   └── utils/                  # Utility functions
│       ├── __init__.py
│       ├── fs.py               # File system operations
│       └── templates.py        # Template handling
├── tests/                      # Test suite
│   ├── test_builder.py
│   ├── test_converters.py
│   ├── test_enhancers.py
│   └── fixtures/               # Test data
├── examples/                   # Example projects
│   ├── basic-website/          # Minimal example
│   ├── blog/                   # Blog example
│   └── portfolio/              # Portfolio example
├── docs/                       # Documentation
│   ├── getting-started.md
│   ├── configuration.md
│   └── extensions.md
├── .github/                    # GitHub configuration
│   └── workflows/
│       ├── tests.yml           # Run tests
│       └── release.yml         # Publish package
├── setup.py                    # Package installation
├── pyproject.toml              # Project metadata
├── README.md                   # Project documentation
├── LICENSE                     # License file
└── CHANGELOG.md                # Version history
```
