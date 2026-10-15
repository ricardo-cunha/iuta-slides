from __future__ import annotations

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
TEMPLATE_ASSETS_OUT = DOCS / "assets" / "template"


def remove_readonly(func, path, _exc_info):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def prepare() -> None:
    for output in (SLIDES_OUT, LEGACY_SLIDES_OUT, TEMPLATE_OUT, TEMPLATE_ASSETS_OUT):
        output.mkdir(parents=True, exist_ok=True)
        for child in output.iterdir():
            if child.is_dir():
                shutil.rmtree(child, onerror=remove_readonly)
            else:
                child.unlink()

    template_source = PRESENTATIONS / "template"
    shutil.copytree(template_source, TEMPLATE_OUT, dirs_exist_ok=True)

    # Publish only reusable template assets. Never copy presentation decks or
    # the shared deck-asset directory into the public documentation tree.
    shared_template_assets = PRESENTATIONS / "assets" / "template"
    if shared_template_assets.is_dir():
        shutil.copytree(shared_template_assets, TEMPLATE_ASSETS_OUT, dirs_exist_ok=True)


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
    ]
    (DOCS / "index.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    prepare()
    write_home()
    print("Prepared the public template. Presentation decks and assets are excluded.")
