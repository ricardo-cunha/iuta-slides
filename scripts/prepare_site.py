from __future__ import annotations

import hashlib
import os
import shutil
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PRESENTATIONS = ROOT / "presentations"
SLIDES_OUT = DOCS / "slides"
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
    SLIDES_OUT.mkdir(parents=True, exist_ok=True)
    for child in SLIDES_OUT.iterdir():
        if child.is_dir():
            shutil.rmtree(child, onerror=remove_readonly)
        else:
            child.unlink()

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
        "> Slide links contain an access token. Treat each link as confidential: anyone who has a valid link can open that presentation.",
        "",
        "## Available presentations",
        "",
    ]
    for name, token in entries:
        label = name.replace("_", " ")
        lines.append(f"- [{label}](slides/{name}/index.html?access={token})")
    lines.extend(
        [
            "",
            "## Repository",
            "",
            "[View the source repository](https://github.com/ricardo-cunha/iuta_slides)",
            "",
            "## Access model",
            "",
            "These links provide light, link-based access control for a static site. They are not a substitute for server-side authentication and should not protect confidential material.",
            "",
        ]
    )
    (DOCS / "index.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    entries = prepare()
    write_home(entries)
    print(f"Prepared {len(entries)} presentation(s) in {SLIDES_OUT}")
    for name, _ in entries:
        print(f"- {name}")
