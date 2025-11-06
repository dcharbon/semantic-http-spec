# GitHub Pages Setup Guide

## Current Status

The repository has been configured for GitHub Pages deployment. All changes are on the branch `claude/review-repo-status-011CUqkQaLVYT7QspBrQJGcm`.

## What Was Done

### 1. Build Configuration
- **Updated `Makefile`** to build Sphinx documentation directly to `docs/` folder (instead of `build/`)
- **Updated `make.bat`** with the same configuration for Windows users
- **Updated `.gitignore`** to exclude Sphinx build artifacts (`.doctrees/`, `.buildinfo`)

### 2. Documentation Build
- Installed Sphinx v8.2.3 and required extensions:
  - `sphinxcontrib-httpdomain`
  - `sphinxcontrib-httpexample`
- Rebuilt all documentation with updated dependencies
- Added `.nojekyll` file to `docs/` folder to prevent Jekyll processing
- Note: `sphinx-jsonschema` extension was temporarily disabled in `source/conf.py` due to installation compatibility issues

### 3. GitHub Actions Workflow
- Created `.github/workflows/sphinx-build.yml` for automated documentation builds
- Workflow triggers on pushes to `main` or `master` branches
- Automatically rebuilds documentation when source files change
- Removed old `github-pages.yml` workflow that was pushing to a separate `gh-pages` branch

### 4. Documentation Updates
- Updated `README.md` with:
  - Link to GitHub Pages documentation site
  - Local build instructions
  - GitHub Pages configuration steps
  - Clear explanation of the build process

## How to Enable GitHub Pages

### Step 1: Merge the Feature Branch

The changes are currently on branch `claude/review-repo-status-011CUqkQaLVYT7QspBrQJGcm`. To merge into `master`:

```bash
git checkout master
git merge claude/review-repo-status-011CUqkQaLVYT7QspBrQJGcm
git push origin master
```

### Step 2: Configure GitHub Pages

1. Go to your repository on GitHub: `https://github.com/dcharbon/semantic-http-spec`
2. Click on **Settings** (in the repository menu)
3. Scroll down to **Pages** in the left sidebar
4. Under "Build and deployment":
   - **Source**: Select "Deploy from a branch"
   - **Branch**: Select `master` (or `main`) from the dropdown
   - **Folder**: Select `/docs` from the dropdown
   - Click **Save**

### Step 3: Wait for Deployment

- GitHub will automatically deploy the contents of the `docs/` folder
- The site will be available at: `https://dcharbon.github.io/semantic-http-spec/`
- Initial deployment typically takes 1-2 minutes
- You can check deployment status in the "Actions" tab of your repository

## Future Updates

Once GitHub Pages is configured, any changes pushed to the `master` branch that affect the `source/` directory will trigger the GitHub Actions workflow to automatically rebuild and update the documentation.

To manually rebuild documentation locally:

```bash
# Install dependencies (if not already installed)
pip install sphinx sphinxcontrib-httpdomain sphinxcontrib-httpexample

# Build documentation
make html
# or
sphinx-build -b html source docs

# Commit and push
git add docs/
git commit -m "Update documentation"
git push origin master
```

## Repository Structure

```
semantic-http-spec/
├── .github/
│   └── workflows/
│       └── sphinx-build.yml       # Automated build workflow
├── docs/                          # Built HTML documentation (published to GitHub Pages)
│   ├── .nojekyll                 # Prevents Jekyll processing
│   ├── index.html                # Main documentation page
│   └── ...                       # Other HTML files and assets
├── source/                        # Sphinx source files (RST format)
│   ├── conf.py                   # Sphinx configuration
│   ├── index.rst                 # Main documentation source
│   └── ...                       # Other RST files
├── Makefile                       # Build script (Unix/Linux/Mac)
├── make.bat                       # Build script (Windows)
├── environment.yml                # Conda environment specification
└── README.md                      # Project README with setup instructions
```

## Troubleshooting

### If the site doesn't appear after configuration:
1. Check the "Actions" tab for any workflow failures
2. Verify that the `docs/` folder contains `index.html` and other HTML files
3. Ensure the `.nojekyll` file exists in the `docs/` folder
4. Wait a few minutes for GitHub's CDN to update

### If the build fails:
1. Check the workflow logs in the "Actions" tab
2. Verify that all required dependencies are installed
3. Try building locally to identify any issues

### Known Issues:
- `sphinx-jsonschema` extension is currently disabled due to installation issues
- If you need JSON schema rendering, you may need to find an alternative extension or fix the installation

## Additional Notes

- The repository previously used GitLab CI for GitLab Pages (see `.gitlab-ci.yml`)
- That configuration built to a `public/` directory
- The new setup uses GitHub Actions and builds to `docs/` for GitHub Pages
- Both systems can coexist if needed, but GitHub Pages is now the primary deployment target
