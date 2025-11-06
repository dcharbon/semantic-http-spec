# semantic-http-spec
Specification of a semantic resource protocol building on HTTP. Specifies additional headers and content on HTTP requests and responses to support rich discovery of schema and semantic web data for resources made available via HTTP.

## Documentation

The full documentation is available on [GitHub Pages](https://dcharbon.github.io/semantic-http-spec/).

## Building the Documentation

This project uses [Jupyter Book](https://jupyterbook.org/) (v1.x, Sphinx-based) to generate documentation from the RST files in the `source/` directory.

### Prerequisites

This project uses [uv](https://docs.astral.sh/uv/) for dependency management. To install uv:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

### Local Build

To build the documentation locally:

```bash
# Install dependencies (creates virtual environment and installs packages)
uv sync

# Build HTML documentation
uv run jupyter-book build .
```

The built documentation will be in the `_build/html/` directory.

### Automated Builds

Documentation is automatically built and deployed via GitHub Actions when changes are pushed to the main branch. The workflow builds the book and copies the output to the `docs/` directory for GitHub Pages deployment.

## GitHub Pages Setup

To enable GitHub Pages for this repository:

1. Go to repository Settings → Pages
2. Under "Build and deployment":
   - Source: Deploy from a branch
   - Branch: Select `main` (or `master`) and `/docs` folder
   - Click Save

The site will be published at: `https://dcharbon.github.io/semantic-http-spec/`

## Semantic HTTP Mapping

This project includes a groundbreaking **Semantic HTTP Mapping** system that allows you to add semantic layers to existing REST APIs without modifying them. Think of it as "TypeScript declaration files for REST APIs."

### Quick Start

```bash
# Generate a semantic mapping for any API
python tools/semantic_mapper.py

# Run the generated proxy
cd example-proxy
pip install -r requirements.txt
python app.py

# Test it
curl -X OPTIONS http://localhost:8080/users/123
```

### Key Features

- **AI-powered semantic inference** - Automatically infers schema.org mappings from field names
- **Proxy generation** - Creates production-ready proxy services
- **Community mappings** - Share and reuse mappings for popular APIs
- **Zero modification** - Works with any existing REST API

### Documentation

- [Mapping Overview](MAPPING_OVERVIEW.md) - Executive overview of the mapping system
- [Mapping Guide](SEMANTIC_MAPPING_GUIDE.md) - Complete user guide
- [Tool Architecture](MAPPING_TOOL_ARCHITECTURE.md) - Technical architecture
- [Analysis & Solution](ANALYSIS_AND_SOLUTION_SUMMARY.md) - Detailed analysis

### Examples

- [Stripe Customer API](examples/stripe-customers-mapping.yaml) - Real-world example
- [Generated Example](example-mapping.yaml) - Auto-generated mapping

## License

This project uses multiple licenses for different components:

- **Specification** (files in `source/*.rst`): [Creative Commons Attribution 4.0 International](LICENSE-SPEC)
  - The Semantic HTTP specification is a standard and should be freely implementable by anyone
- **Code, Tools & Examples**: [Apache License 2.0](LICENSE)
  - All implementation code, tools, mappings, and examples use the business-friendly Apache 2.0 license
  - Includes patent protection and allows commercial use

See the [LICENSE](LICENSE) and [LICENSE-SPEC](LICENSE-SPEC) files for full details.

## Welcome to GitHub Pages

You can use the [editor on GitHub](https://github.com/openteamsinc/semantic-http-spec/edit/master/README.md) to maintain and preview the content for your website in Markdown files.

Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/openteamsinc/semantic-http-spec/settings). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://help.github.com/categories/github-pages-basics/) or [contact support](https://github.com/contact) and we’ll help you sort it out.
