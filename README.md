# IUTA Slides

Reveal.js presentations using the IUTA visual template.

The repository contains:

- `template/` — the reusable IUTA Reveal.js template.
- `presentations/` — individual presentation decks (each in its own folder with `index.html`).
- `presentations/assets/` — shared assets (template CSS, vendor libraries, images).
- `docs/` — the MkDocs landing page and documentation-site assets.
- `scripts/prepare_site.py` — stages the template and unlisted, token-gated presentations for the MkDocs site.
- `.github/workflows/pages.yml` — builds and deploys the MkDocs site to GitHub Pages.

## Presentations

Presentation decks are kept off the site homepage. Generate their tokenized links using the instructions below.

## GitHub Pages

The published site is:

<https://ricardo-cunha.github.io/iuta-slides/>

The homepage lists the reusable template only. Presentation decks are deployed but not listed; use a tokenized link to open one.

Presentation links use link-based obscurity, not real authentication. Anyone with a valid link can open that deck, and the deck's assets may be accessible by direct URL. Do not use this to protect confidential material.

## Local setup

Create the local Python environment and install the documentation dependencies:

```powershell
python -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
```

Build the documentation locally:

```powershell
.venv\Scripts\python.exe scripts\prepare_site.py
.venv\Scripts\python.exe -m mkdocs build --strict
```

Preview it locally:

```powershell
.venv\Scripts\python.exe -m mkdocs serve
```

MkDocs will print a local preview URL, normally:

<http://127.0.0.1:8000/iuta-slides/>

## Get presentation links

Set `SLIDES_ACCESS_SECRET` to the same private value configured in GitHub repository settings under **Settings → Secrets and variables → Actions**. The secret is used to derive a SHA-256 token for each presentation folder.

In PowerShell:

```powershell
$env:SLIDES_ACCESS_SECRET = 'your-exact-secret'
.\.venv\Scripts\python.exe scripts\prepare_site.py --show-links
```

In Bash or Git Bash:

```bash
SLIDES_ACCESS_SECRET='your-exact-secret' .venv/Scripts/python.exe scripts/prepare_site.py --show-links
```

The command prints links similar to:

```text
https://ricardo-cunha.github.io/iuta-slides/presentations/20260908_iuta_seminar/index.html?access=<token>
```

Use a strong secret and keep it private. The local value must match the GitHub Actions secret exactly. Changing it invalidates previously generated links.

## GitHub Pages deployment

The repository uses GitHub Actions for deployment. Configure the repository as follows:

1. Add `SLIDES_ACCESS_SECRET` under **Settings → Secrets and variables → Actions**.
2. Go to **Settings → Pages** and set **Source** to **GitHub Actions**.
3. Push to `main` or run the `Deploy IUTA Slides Pages` workflow manually.

The workflow stages the template and presentations, builds MkDocs with `--strict`, and deploys the generated `site/` directory. Presentation names and contents remain off the homepage; links are available only to people who have the corresponding URL.
