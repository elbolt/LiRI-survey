#!/usr/bin/env python3
"""Generate manifest.json for Posit Connect deployment."""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ENTRYPOINT = "survey_app.py"
APPMODE = "python-streamlit"


def md5(path: Path) -> str:
    h = hashlib.md5()
    h.update(path.read_bytes())
    return h.hexdigest()


def pip_version() -> str:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "--version"],
        capture_output=True, text=True
    )
    # output looks like: "pip 26.0.1 from ..."
    return result.stdout.split()[1]


def tracked_files() -> list[str]:
    """Return files tracked by git (respects .gitignore)."""
    result = subprocess.run(
        ["git", "ls-files"],
        capture_output=True, text=True
    )
    return [f.strip() for f in result.stdout.splitlines() if f.strip()]


def main():
    root = Path(__file__).parent

    python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    pip_ver = pip_version()

    files_to_include = set(tracked_files())
    # Always include manifest.json and this script itself
    files_to_include.add("manifest.json")
    files_to_include.add("write_manifest.py")

    files_section = {}
    for rel_path in sorted(files_to_include):
        p = root / rel_path
        if p.exists():
            files_section[rel_path] = {"checksum": md5(p)}
        else:
            print(f"  Warning: {rel_path} not found on disk, skipping.")

    manifest = {
        "version": 1,
        "locale": "en_US.UTF-8",
        "metadata": {
            "appmode": APPMODE,
            "entrypoint": ENTRYPOINT,
        },
        "python": {
            "version": python_ver,
            "package_manager": {
                "name": "pip",
                "version": pip_ver,
                "package_file": "requirements.txt",
            },
        },
        "files": files_section,
    }

    out = root / "manifest.json"
    out.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Written manifest.json (Python {python_ver}, pip {pip_ver})")
    print(f"Included {len(files_section)} files.")


if __name__ == "__main__":
    main()
