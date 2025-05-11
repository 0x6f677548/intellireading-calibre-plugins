#!/bin/bash

# Check if we got a param with calibre directory path
if [ -z "$1" ]; then
    # Check if we have an environment variable with calibre directory path
    if [ -z "$CALIBRE_DIR" ]; then
        # Ask for calibre directory path, suggesting a default
        default_calibre_dir="/opt/calibre/"
        read -e -p "Please enter the path to the calibre directory [${default_calibre_dir}]: " -i "${default_calibre_dir}" calibre_dir
        # Set environment variable with calibre directory path for this session and sub-processes
        export CALIBRE_DIR="$calibre_dir"
    else
        calibre_dir="$CALIBRE_DIR"
    fi
else
    calibre_dir="$1"
    # Optionally update the environment variable if argument is provided
    export CALIBRE_DIR="$calibre_dir"
fi

# Check if the copy-commonfiles script exists and is executable
if [ -f "./copy-commonfiles.sh" ]; then
    if [ ! -x "./copy-commonfiles.sh" ]; then
        echo "Making copy-commonfiles.sh executable..."
        chmod +x ./copy-commonfiles.sh
    fi
    # Run the common files script
    ./copy-commonfiles.sh
else
    echo "Warning: ./copy-commonfiles.sh not found. Skipping."
fi


# Output calibre directory path
echo "Calibre directory: $calibre_dir"

# Check if calibre executables exist
if [ ! -f "$calibre_dir/calibre-customize" ] || [ ! -f "$calibre_dir/calibre-debug" ]; then
    echo "Error: calibre-customize or calibre-debug not found in $calibre_dir"
    echo "Please ensure the Calibre directory path is correct and contains the executables."
    exit 1
fi


# Arrays of plugins to remove and add
plugin_names=(
    "Epub Metaguider post processor (intellireading.com)"
    "Epub Metaguider output format (intellireading.com)"
    "Epub Metaguider GUI (intellireading.com)"
)

plugin_paths=(
    "./epubmg_filetypeplugin/"
    "./epubmg_outputplugin/"
    "./epubmg_interfaceplugin/"
)

# Get the number of elements
num_plugins=${#plugin_names[@]}

# Remove and rebuild all plugins
echo "Removing and reinstalling plugins..."
for (( i=0; i<${num_plugins}; i++ )); do
    name="${plugin_names[$i]}"
    path="${plugin_paths[$i]}"

    # Check if plugin path exists
    if [ ! -d "$path" ]; then
        echo "Warning: Plugin path '$path' not found. Skipping plugin '$name'."
        continue
    fi

    echo "Processing '$name' with path '$path'"

    # Remove plugin (ignore errors if plugin doesn't exist)
    "$calibre_dir/calibre-customize" -r "$name" || true

    # Build and add plugin
    "$calibre_dir/calibre-customize" -b "$path"
    if [ $? -ne 0 ]; then
        echo "Error: Failed to build plugin '$name' from path '$path'."
        # Decide if you want to exit or continue with other plugins
        # exit 1 # Uncomment to exit on first failure
    fi
done

echo "Starting Calibre debug..."
# Start Calibre in debug mode
"$calibre_dir/calibre-debug" -g
