# IUTA Slides

Reveal.js presentations using the IUTA visual template.

The repository contains:

- `template/` — the reusable IUTA Reveal.js template.
- `presentations/` — individual presentation decks.
- `docs/` — the MkDocs landing page and documentation-site assets.
- `scripts/prepare_site.py` — prepares the MkDocs site and generates tokenized presentation links.
- `.github/workflows/pages.yml` — builds and deploys the MkDocs site to GitHub Pages.

## GitHub Pages

The published site is:

<https://ricardo-cunha.github.io/iuta-slides/>

The template is publicly linked from the homepage. Presentations are published but intentionally omitted from the homepage listing. Their direct links contain an access token.

This is link-based obscurity, not real authentication. Anyone with a valid presentation link can open that deck, and it should not be used to protect confidential material.

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

## Get presentation links

The link tokens are derived from `SLIDES_ACCESS_SECRET`. Use the same value locally that is configured in GitHub repository settings as the Actions secret with the exact name:

```text
SLIDES_ACCESS_SECRET
```

In PowerShell:

```powershell
$env:SLIDES_ACCESS_SECRET = 'your-exact-secret'
.\\.venv\\Scripts\\python.exe scripts\\prepare_site.py --show-links
```

In Bash or Git Bash:

```bash
SLIDES_ACCESS_SECRET='your-exact-secret' .venv/Scripts/python.exe scripts/prepare_site.py --show-links
```

The command rebuilds the local staging tree and prints links similar to:

```text
https://ricardo-cunha.github.io/iuta-slides/presentations/20260908_iuta_seminar/index.html?access=<token>
```

The secret must match the GitHub Actions secret exactly. Changing it invalidates previously generated links.

## GitHub Pages deployment

The repository uses GitHub Actions for deployment. Configure the repository as follows:

1. Add the repository secret `SLIDES_ACCESS_SECRET` under **Settings → Secrets and variables → Actions**.
2. Go to **Settings → Pages**.
3. Set **Source** to **GitHub Actions**.
4. Push to `main` or run the `Deploy IUTA Slides Pages` workflow manually.

The workflow prepares the current presentation folders, builds MkDocs with `--strict`, and deploys the generated `site/` directory.
