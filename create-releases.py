#!/usr/bin/env python3

import sys
import re
import shutil
import argparse
from pathlib import Path


def validate_version(version: str) -> bool:
    """Validate that the version is in the format x.x.x"""
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        print("Error: Version must be in the format x.x.x", file=sys.stderr)
        print("Example: 1.0.0", file=sys.stderr)
        print("Usage: create-releases.py --version 1.0.0", file=sys.stderr)
        return False
    return True


def create_releases(version: str):
    """Create zip files for each plugin directory"""
    print(f"Creating release {version} in _releases")

    # Get the root directory (current directory)
    root = Path.cwd()

    # Create the releases directory
    releases_dir = root / "_releases" / version
    releases_dir.mkdir(parents=True, exist_ok=True)

    # Get all directories excluding _releases and .common
    folders = [d for d in root.iterdir() if d.is_dir() and not d.name.startswith("_") and not d.name.startswith(".")]

    # Create zip file for each folder
    for folder in folders:
        zip_path = releases_dir / f"{folder.name}.zip"
        if zip_path.exists():
            zip_path.unlink()

        shutil.make_archive(
            str(zip_path.with_suffix("")),  # Remove .zip as make_archive adds it
            "zip",
            root_dir=root,
            base_dir=folder.name,
        )

    print("\nCreated releases:")
    for file in releases_dir.iterdir():
        print(f"  {file.name}")


def main():
    parser = argparse.ArgumentParser(description="Create release zip files for plugins")
    parser.add_argument("--version", type=str, default="1.0.0", help="Version number in format x.x.x")

    args = parser.parse_args()

    if not validate_version(args.version):
        sys.exit(1)

    create_releases(args.version)


if __name__ == "__main__":
    main()
