# IUTA Slides

Reveal.js presentations using the IUTA visual template.

The repository contains:

- `template/` — the reusable IUTA Reveal.js template.
- `presentations/` — individual presentation decks (each in its own folder with `index.html`).
- `presentations/assets/` — shared assets (template CSS, vendor libraries, images).
- `docs/` — the MkDocs landing page and documentation-site assets.
- `scripts/prepare_site.py` — stages only public template files for the MkDocs site.
- `.github/workflows/pages.yml` — builds and deploys the MkDocs site to GitHub Pages.

## Presentations

- `20260923_workshop_short/` — StreamFind FAIR data workshop (short version).
- `template/` — reusable IUTA template for new presentations.

## GitHub Pages

The published site is:

<https://ricardo-cunha.github.io/iuta-slides/>

The site publishes the reusable template only. Presentation decks and their shared assets are excluded from the generated site.

## Local setup

Create the local Python environment and install the documentation dependencies:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\python.exe -m pip install -r requirements-docs.txt
```

Build the documentation locally:

```powershell
.\\.venv\\Scripts\\python.exe scripts\\prepare_site.py
.\\.venv\\Scripts\\python.exe -m mkdocs build --strict
```

Preview it locally:

```powershell
.\\.venv\\Scripts\\python.exe -m mkdocs serve
```

MkDocs will print a local preview URL, normally:

<http://127.0.0.1:8000/iuta-slides/>

## GitHub Pages deployment

The repository uses GitHub Actions for deployment. Configure the repository as follows:

1. Go to **Settings → Pages**.
2. Set **Source** to **GitHub Actions**.
3. Push to `main` or run the `Deploy IUTA Slides Pages` workflow manually.

The workflow stages only the reusable template, builds MkDocs with `--strict`, and deploys the generated `site/` directory. It does not copy presentation decks or their assets into the public site.
