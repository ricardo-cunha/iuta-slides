from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PRESENTATIONS = ROOT / "presentations"
SLIDES_OUT = DOCS / "presentations"
LEGACY_SLIDES_OUT = DOCS / "slides"
TEMPLATE_OUT = DOCS / "template"
ACCESS_JS = DOCS / "javascripts" / "access-gate.js"

# This is only a link token, not encryption. Set a private value for deployment.
SECRET = os.environ.get("SLIDES_ACCESS_SECRET", "local-preview-secret")


def remove_readonly(func, path, _exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def token_for(name: str) -> str:
    return hashlib.sha256(f"{SECRET}:{name}".encode("utf-8")).hexdigest()


def inject_gate(html: str, token: str) -> str:
    gate = (
        f'<script>window.IUTA_SLIDE_ACCESS_TOKEN="{token}";</script>\n'
        '<script src="../../javascripts/access-gate.js"></script>\n'
    )
    if "access-gate.js" in html:
        return html
    return html.replace("</head>", f"{gate}</head>", 1)


def prepare() -> list[tuple[str, str]]:
    for output in (SLIDES_OUT, LEGACY_SLIDES_OUT, TEMPLATE_OUT):
        output.mkdir(parents=True, exist_ok=True)
        for child in output.iterdir():
            if child.is_dir():
                shutil.rmtree(child, onerror=remove_readonly)
            else:
                child.unlink()

    template_source = ROOT / "template"
    shutil.copytree(template_source, TEMPLATE_OUT, dirs_exist_ok=True)

    entries: list[tuple[str, str]] = []
    for source in sorted(PRESENTATIONS.iterdir()):
        if not source.is_dir() or not (source / "index.html").is_file():
            continue
        name = source.name
        destination = SLIDES_OUT / name
        shutil.copytree(source, destination)
        html_path = destination / "index.html"
        html_path.write_text(
            inject_gate(html_path.read_text(encoding="utf-8"), token_for(name)),
            encoding="utf-8",
        )
        entries.append((name, token_for(name)))
    return entries


def write_home(entries: list[tuple[str, str]]) -> None:
    lines = [
        "# IUTA Slides",
        "",
        "Presentations for the IUTA seminar and related StreamFind work.",
        "",
        "## Template",
        "",
        "[Open the Reveal.js IUTA template](template/index.html)",
        "",
        "## Available presentations",
        "",
        "Presentations are intentionally unlisted. Use a tokenized link supplied by the owner to open a deck.",
        "",
        "## Repository",
        "",
        "[View the source repository](https://github.com/ricardo-cunha/iuta-slides)",
        "",
        "## Access model",
        "",
        "Presentation links use light, link-based access control. Anyone with a valid link can open that presentation, so these links are not a substitute for server-side authentication.",
        "",
    ]
    (DOCS / "index.md").write_text("\n".join(lines), encoding="utf-8")


def print_links(entries: list[tuple[str, str]]) -> None:
    print("Tokenized presentation links:")
    for name, token in entries:
        print(f"- https://ricardo-cunha.github.io/iuta-slides/presentations/{name}/index.html?access={token}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-links", action="store_true")
    args = parser.parse_args()

    entries = prepare()
    write_home(entries)
    print(f"Prepared {len(entries)} presentation(s) and the public template")
    if args.show_links:
        print_links(entries)
