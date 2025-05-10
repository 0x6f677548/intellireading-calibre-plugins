#copy the common\common.py to all plugins
Copy-Item -Path .\_common\common.py -Destination .\epubmg_filetypeplugin\common.py -Force
Copy-Item -Path .\_common\common.py -Destination .\epubmg_outputplugin\common.py -Force
Copy-Item -Path .\_common\common.py -Destination .\epubmg_interfaceplugin\common.py -Force

# check if the metaguiding.py exists in the common folder or if the user wants to update it
if (-not (Test-Path .\_common\metaguiding.py) -or (Read-Host "Do you want to update metaguiding.py? (yes/no)") -eq "yes") {


    # check if the user wants to download the latest version of metaguiding.py or copy it from ../intellireading-cli/src/intellireading/client/metaguiding.py
    $download = Read-Host "Do you want to download the latest version of metaguiding.py or copy it from ../intellireading-cli/src/intellireading/client/metaguiding.py? (download/copy)"
    if ($download -eq "copy") {
        #copy the metaguiding.py from ../intellireading-cli/src/intellireading/client/metaguiding.py
        Copy-Item -Path ..\intellireading-cli\src\intellireading\client\metaguiding.py -Destination .\_common\metaguiding.py -Force
    }
    else {
        #download the latest version of metaguiding.py from https://go.hugobatista.com/ghraw/intellireading-cli/refs/heads/main/src/intellireading/client/metaguiding.py
        Invoke-WebRequest -Uri "https://go.hugobatista.com/ghraw/intellireading-cli/refs/heads/main/src/intellireading/client/metaguiding.py" -OutFile .\_common\metaguiding.py
    }
    
}
#copy the common\metaguiding.py to all plugins
Copy-Item -Path .\_common\metaguiding.py -Destination .\epubmg_filetypeplugin\metaguiding.py -Force
Copy-Item -Path .\_common\metaguiding.py -Destination .\epubmg_outputplugin\metaguiding.py -Force
Copy-Item -Path .\_common\metaguiding.py -Destination .\epubmg_interfaceplugin\metaguiding.py -Force


