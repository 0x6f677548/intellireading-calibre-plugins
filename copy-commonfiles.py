#!/usr/bin/env python3

import sys
import shutil
import subprocess
from pathlib import Path
from typing import List

# Base paths
COMMON_DIR = Path("_common")
CLI_CLIENT_DIR = Path("../intellireading-cli/src/intellireading/client")
REPO_BASE_URL = "https://go.hugobatista.com/ghraw/intellireading-cli/refs/heads/main/src/intellireading/client"

# File configurations
COMMON_PY = COMMON_DIR / "common.py"  # Special case, no remote source

# List of files to copy from CLI project - just add new filenames here
CLI_FILES = [
    "metaguiding.py",
    "__about_cli__.py",
    # Add new files here
]


def get_file_paths(filename: str) -> dict:
    """Generate all paths for a given filename."""
    return {
        "filename": filename,
        "common_path": COMMON_DIR / filename,
        "local_path": CLI_CLIENT_DIR / filename,
        "url": f"{REPO_BASE_URL}/{filename}",
    }


# Plugin directories
PLUGIN_DIRS = [
    "metaguide_filetypeplugin",
    "metaguide_outputplugin",
    "metaguide_interfaceplugin",
    "metaguide_kobotouchplugin",
]


def validate_subprocess_result(result: subprocess.CompletedProcess, operation: str) -> bool:
    """Validate subprocess result and print appropriate messages."""
    if result.returncode != 0:
        print(f"Error during {operation}:")
        if result.stdout:
            print(f"Output: {result.stdout.decode()}")
        if result.stderr:
            print(f"Error: {result.stderr.decode()}")
        return False
    return True


def get_plugin_paths(filename: str) -> List[Path]:
    """Generate plugin paths for a given filename."""
    return [Path(plugin_dir) / filename for plugin_dir in PLUGIN_DIRS]


def copy_file_with_check(src: Path, dest: Path, description: str) -> bool:
    """Copy a file and handle errors."""
    try:
        shutil.copy2(src, dest)
        return True
    except IOError as e:
        print(f"Error copying {description} to {dest}: {e}")
        return False


def download_file(url: str, dest: Path, description: str) -> bool:
    """Download a file using curl and handle errors."""
    print(f"Downloading {description} from {url}...")
    result = subprocess.run(["curl", "-fLo", str(dest), url], capture_output=True, text=True)
    if not validate_subprocess_result(result, f"downloading {description}"):
        return False
    print("Download successful.")
    return True


def handle_cli_file(filename: str, local_path: Path, url: str, common_path: Path, description: str) -> bool:
    """Handle downloading or copying a CLI file."""
    source_choice = input(f"Download latest {filename} or copy from {local_path}? (download/copy) [download]: ").lower()

    if source_choice.startswith("c"):
        if local_path.is_file():
            print(f"Copying {filename} from {local_path}...")
            if not copy_file_with_check(local_path, common_path, description):
                sys.exit(1)
        else:
            print(f"Error: Local file {local_path} not found. Cannot copy.")
            sys.exit(1)
    else:
        if not download_file(url, common_path, description):
            sys.exit(1)
    return True


def copy_common_files():
    # Copy common.py to all plugins (special case - no remote source)
    print("Copying common.py...")
    common_plugin_paths = get_plugin_paths("common.py")
    for plugin_path in common_plugin_paths:
        if not copy_file_with_check(COMMON_PY, plugin_path, "common.py"):
            sys.exit(1)

    # Function to handle CLI file updates
    def update_cli_file(filename: str):
        """Handle updating a single CLI file."""
        paths = get_file_paths(filename)
        common_path = paths["common_path"]

        update_file = False
        if not common_path.is_file():
            print(f"{filename} not found.")
            update_file = True
        else:
            update_response = input(f"Do you want to update {filename}? (yes/no) [no]: ").lower()
            update_file = update_response.startswith("y")

        if update_file:
            handle_cli_file(
                filename=filename,
                local_path=paths["local_path"],
                url=paths["url"],
                common_path=common_path,
                description=filename,
            )

    # Update all CLI files
    for filename in CLI_FILES:
        update_cli_file(filename)

    # Copy all CLI files to plugins if they exist
    for filename in CLI_FILES:
        common_path = get_file_paths(filename)["common_path"]

        if common_path.is_file():
            print(f"Copying {filename} to plugins...")
            plugin_paths = get_plugin_paths(filename)
            for plugin_path in plugin_paths:
                if not copy_file_with_check(common_path, plugin_path, filename):
                    sys.exit(1)
        else:
            print(f"Warning: {filename} not found or update failed. Skipping copy to plugins.")

    print("Common files copy process finished.")
    return True


def main():
    try:
        success = copy_common_files()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
