#!/bin/bash

# Copy the _common/common.py to all plugins
echo "Copying common.py..."
cp -f ./_common/common.py ./epubmg_filetypeplugin/common.py
cp -f ./_common/common.py ./epubmg_outputplugin/common.py
cp -f ./_common/common.py ./epubmg_interfaceplugin/common.py

# Check if metaguiding.py exists or if the user wants to update it
update_metaguiding="no"
if [ ! -f "./_common/metaguiding.py" ]; then
    echo "_common/metaguiding.py not found."
    update_metaguiding="yes"
else
    read -p "Do you want to update metaguiding.py? (yes/no) [no]: " update_response
    if [[ "$update_response" =~ ^[Yy](es)?$ ]]; then
        update_metaguiding="yes"
    fi
fi

if [ "$update_metaguiding" == "yes" ]; then
    # Check if the user wants to download or copy
    read -p "Download latest metaguiding.py or copy from ../intellireading-cli/src/intellireading/client/metaguiding.py? (download/copy) [download]: " source_choice
    if [[ "$source_choice" =~ ^[Cc](opy)?$ ]]; then
        # Copy from local path
        local_path="../intellireading-cli/src/intellireading/client/metaguiding.py"
        if [ -f "$local_path" ]; then
            echo "Copying metaguiding.py from $local_path..."
            cp -f "$local_path" ./_common/metaguiding.py
        else
            echo "Error: Local file $local_path not found. Cannot copy."
            # Decide if you want to exit or proceed without updating
            # exit 1 # Uncomment to exit if copy fails
        fi
    else
        # Download from URL
        url="https://go.hugobatista.com/ghraw/intellireading-cli/refs/heads/main/src/intellireading/client/metaguiding.py"
        echo "Downloading metaguiding.py from $url..."
        # Use curl, check for success
        if curl -fLo ./_common/metaguiding.py "$url"; then
            echo "Download successful."
        else
            echo "Error: Failed to download metaguiding.py from $url."
            # Decide if you want to exit or proceed without updating
            # exit 1 # Uncomment to exit if download fails
        fi
    fi
fi

# Copy the _common/metaguiding.py to all plugins if it exists
if [ -f "./_common/metaguiding.py" ]; then
    echo "Copying metaguiding.py to plugins..."
    cp -f ./_common/metaguiding.py ./epubmg_filetypeplugin/metaguiding.py
    cp -f ./_common/metaguiding.py ./epubmg_outputplugin/metaguiding.py
    cp -f ./_common/metaguiding.py ./epubmg_interfaceplugin/metaguiding.py
else
    echo "Warning: _common/metaguiding.py not found or update failed. Skipping copy to plugins."
fi

echo "Common files copy process finished."
