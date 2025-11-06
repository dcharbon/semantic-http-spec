# semantic-http-spec
Specification of a semantic resource protocol building on HTTP. Specifies additional headers and content on HTTP requests and responses to support rich discovery of schema and semantic web data for resources made available via HTTP.

## Documentation

The full documentation is available on [GitHub Pages](https://dcharbon.github.io/semantic-http-spec/).

## Building the Documentation

This project uses [Jupyter Book](https://jupyterbook.org/) (v1.x, Sphinx-based) to generate documentation from the RST files in the `source/` directory.

### Local Build

To build the documentation locally:

```bash
# Install dependencies
pip install "jupyter-book<2" sphinxcontrib-httpdomain sphinxcontrib-httpexample

# Build HTML documentation
jupyter-book build .
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
