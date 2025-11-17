#!/usr/bin/env python3
"""
Utility script to download and prepare SadTalker for LarAndre+.

Usage:
    python tools/setup_talking_head.py
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from typing import Dict
from urllib.request import urlopen

REPO_URL = "https://github.com/OpenTalker/SadTalker.git"
RELEASE_TAG = "v0.0.2"
ASSETS: Dict[str, str] = {
    "checkpoints": f"https://github.com/OpenTalker/SadTalker/releases/download/{RELEASE_TAG}/checkpoints.zip",
    "gfpgan": f"https://github.com/OpenTalker/SadTalker/releases/download/{RELEASE_TAG}/gfpgan.zip",
}


def download_zip(url: str, extract_to: Path) -> None:
    extract_to.mkdir(parents=True, exist_ok=True)
    print(f"⬇️  Downloading {url}")
    with urlopen(url) as response:
        data = response.read()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp_file:
        tmp_file.write(data)
        tmp_path = Path(tmp_file.name)

    try:
        with zipfile.ZipFile(tmp_path) as zf:
            zf.extractall(extract_to)
    finally:
        tmp_path.unlink(missing_ok=True)


def clone_repo(repo_dir: Path, force: bool = False) -> None:
    if repo_dir.exists():
        if force:
            print("♻️  Removing existing SadTalker directory (force enabled)")
            shutil.rmtree(repo_dir)
        else:
            print("✅ SadTalker repository already present")
            return

    repo_dir.parent.mkdir(parents=True, exist_ok=True)
    print(f"📦 Cloning SadTalker into {repo_dir}")
    subprocess.run(
        ["git", "clone", "--depth", "1", REPO_URL, str(repo_dir)],
        check=True,
    )


def ensure_assets(repo_dir: Path, force: bool = False) -> None:
    for folder, url in ASSETS.items():
        target_dir = repo_dir / folder
        if target_dir.exists() and any(target_dir.iterdir()) and not force:
            print(f"✅ {folder} already downloaded")
            continue

        if target_dir.exists() and force:
            shutil.rmtree(target_dir)

        download_zip(url, repo_dir)
        print(f"✅ {folder} ready")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare SadTalker locally.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-clone the repository and re-download checkpoints",
    )
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    repo_dir = project_root / "vendors" / "SadTalker"

    clone_repo(repo_dir, force=args.force)
    ensure_assets(repo_dir, force=args.force)

    print("\n🎉 SadTalker assets are ready!")
    print(f"   Repository: {repo_dir}")
    print(f"   Checkpoints: {repo_dir / 'checkpoints'}")
    print("   You can now run `python tools/generate_talking_head.py --help`")


if __name__ == "__main__":
    main()

