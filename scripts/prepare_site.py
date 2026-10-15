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

# This token is link-based access, not encryption or server-side authentication.
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

    template_source = PRESENTATIONS / "template"
    shutil.copytree(template_source, TEMPLATE_OUT, dirs_exist_ok=True)

    # Shared presentation assets are staged separately so decks can reference them.
    shared_assets = PRESENTATIONS / "assets"
    if shared_assets.is_dir():
        shutil.copytree(shared_assets, SLIDES_OUT / "assets", dirs_exist_ok=True)

    entries: list[tuple[str, str]] = []
    for source in sorted(PRESENTATIONS.iterdir()):
        if source.name == "template" or not source.is_dir() or not (source / "index.html").is_file():
            continue
        name = source.name
        destination = SLIDES_OUT / name
        shutil.copytree(source, destination)
        html_path = destination / "index.html"
        token = token_for(name)
        html_path.write_text(
            inject_gate(html_path.read_text(encoding="utf-8"), token),
            encoding="utf-8",
        )
        entries.append((name, token))
    return entries


def write_home() -> None:
    lines = [
        "# IUTA Slides",
        "",
        "Reusable Reveal.js template resources.",
        "",
        "## Template",
        "",
        "[Open the Reveal.js IUTA template](template/index.html)",
        "",
        "Presentation decks are unlisted. Open them with a tokenized link from the owner.",
        "",
        "These links provide link-based obscurity, not authentication. Anyone with a valid link can open the deck.",
        "",
    ]
    (DOCS / "index.md").write_text("\n".join(lines), encoding="utf-8")


def print_links(entries: list[tuple[str, str]]) -> None:
    print("Tokenized presentation links:")
    for name, token in entries:
        print(
            f"- https://ricardo-cunha.github.io/iuta-slides/"
            f"presentations/{name}/index.html?access={token}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--show-links", action="store_true")
    args = parser.parse_args()

    if args.show_links and not os.environ.get("SLIDES_ACCESS_SECRET"):
        parser.error("set SLIDES_ACCESS_SECRET to the deployment secret before generating links")

    entries = prepare()
    write_home()
    print(f"Prepared {len(entries)} unlisted presentation(s) and the public template")
    if args.show_links:
        print_links(entries)
