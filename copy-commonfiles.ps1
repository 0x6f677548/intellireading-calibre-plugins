#copy the common\common.py to all plugins
Copy-Item -Path .\_common\common.py -Destination .\epubmg_filetypeplugin\common.py -Force
Copy-Item -Path .\_common\common.py -Destination .\epubmg_outputplugin\common.py -Force
Copy-Item -Path .\_common\common.py -Destination .\epubmg_interfaceplugin\common.py -Force
