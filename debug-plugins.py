#!/usr/bin/env python3

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Dict

# Type definitions
PluginConfig = Dict[str, str | Path]

# File system paths
DEFAULT_CALIBRE_DIR = Path("/opt/calibre")
COPY_COMMONFILES = Path("./copy-commonfiles.py")

# Calibre executables
CALIBRE_CUSTOMIZE = "calibre-customize"
CALIBRE_DEBUG = "calibre-debug"

# Plugin configurations
PLUGIN_INFO: List[PluginConfig] = [
    {
        "name": "Epub Metaguider post processor (intellireading.com)",
        "path": Path("epubmg_filetypeplugin"),
    },
    {
        "name": "Epub Metaguider output format (intellireading.com)",
        "path": Path("epubmg_outputplugin"),
    },
    {
        "name": "Epub Metaguider GUI (intellireading.com)",
        "path": Path("epubmg_interfaceplugin"),
    },
    {
        "name": "KoboTouch Metaguider (intellireading.com)",
        "path": Path("kobotouch_metaguiderplugin"),
    }
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

def run_command(cmd: List[str], operation: str, check: bool = True) -> bool:
    """Run a command and validate its result.
    
    Args:
        cmd: Command to run as list of strings
        operation: Description of the operation for error messages
        check: Whether to check the return code
    """
    try:
        # For normal commands, capture output and show it
        result = subprocess.run(cmd, text=True)
        if check and result.returncode != 0:
            print(f"Error during {operation}: command exited with status {result.returncode}")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing {operation}: {e}")
        return False

def get_calibre_dir() -> Path:
    """Get the Calibre directory from args, env, or user input."""
    # Check if we got a param with calibre directory path
    if len(sys.argv) > 1:
        calibre_dir = sys.argv[1]
    else:
        # Check if we have an environment variable with calibre directory path
        calibre_dir = os.environ.get('CALIBRE_DIR', '')
        if not calibre_dir:
            # Ask for calibre directory path, suggesting a default
            calibre_dir = input(f"Please enter the path to the calibre directory [{DEFAULT_CALIBRE_DIR}]: ")
            calibre_dir = calibre_dir.strip() or str(DEFAULT_CALIBRE_DIR)
    
    # Set environment variable for this session and sub-processes
    os.environ['CALIBRE_DIR'] = calibre_dir
    return Path(calibre_dir)

def run_copy_commonfiles() -> bool:
    """Run the copy-commonfiles script functions directly."""
    if not COPY_COMMONFILES.exists():
        print(f"Warning: {COPY_COMMONFILES} not found. Skipping.")
        return True

    try:
        # Import the module from the current directory
        import importlib.util
        spec = importlib.util.spec_from_file_location("copy_commonfiles", COPY_COMMONFILES)
        if spec is None or spec.loader is None:
            print(f"Error: Could not load {COPY_COMMONFILES}")
            return False
            
        copy_commonfiles = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(copy_commonfiles)
        
        # Call the main function
        return copy_commonfiles.copy_common_files()
    except Exception as e:
        print(f"Error running copy-commonfiles: {e}")
        return False

def validate_calibre_executables(calibre_dir: Path) -> bool:
    """Check if required Calibre executables exist."""
    executables = {
        CALIBRE_CUSTOMIZE: calibre_dir / CALIBRE_CUSTOMIZE,
        CALIBRE_DEBUG: calibre_dir / CALIBRE_DEBUG
    }
    
    missing = [name for name, path in executables.items() if not path.exists()]
    if missing:
        print(f"Error: {', '.join(missing)} not found in {calibre_dir}")
        print("Please ensure the Calibre directory path is correct and contains the executables.")
        return False
    return True

def process_plugin(plugin: PluginConfig, calibre_dir: Path) -> bool:
    """Process a single plugin (remove and rebuild)."""
    name = str(plugin["name"])  # Ensure string type for subprocess
    path = plugin["path"]
    assert isinstance(path, Path)  # Type check for mypy

    # Check if plugin path exists
    if not path.is_dir():
        print(f"Warning: Plugin path '{path}' not found. Skipping plugin '{name}'.")
        return True

    print(f"Processing '{name}' with path '{path}'")
    calibre_customize = calibre_dir / CALIBRE_CUSTOMIZE

    # Remove plugin (ignore errors if plugin doesn't exist)
    run_command(
        [str(calibre_customize), "-r", name],
        f"removing plugin {name}",
        check=False
    )

    # Build and add plugin
    if not run_command(
        [str(calibre_customize), "-b", str(path)],
        f"building plugin {name}"
    ):
        print(f"Error: Failed to build plugin '{name}' from path '{path}'.")
        return False

    return True

def main() -> None:
    """Main function to manage Calibre plugins."""
    try:
        calibre_dir = get_calibre_dir()
        print(f"Calibre directory: {calibre_dir}")

        if not run_copy_commonfiles():
            sys.exit(1)

        if not validate_calibre_executables(calibre_dir):
            sys.exit(1)

        # Remove and rebuild all plugins
        print("Removing and reinstalling plugins...")
        for plugin in PLUGIN_INFO:
            if not process_plugin(plugin, calibre_dir):
                # Uncomment to exit on first failure
                # sys.exit(1)
                continue

        print("Starting Calibre in debug mode...")
        # Start Calibre in debug mode and wait for it to finish
        run_command(
            [str(calibre_dir / CALIBRE_DEBUG), "-g"],
            "running Calibre in debug mode"
        )
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
