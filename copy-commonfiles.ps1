#copy the common\epubmg_common.py to all plugins
Copy-Item -Path .\_common\epubmg_common.py -Destination .\epubmg_filetypeplugin\epubmg_common.py -Force
Copy-Item -Path .\_common\epubmg_common.py -Destination .\epubmg_outputplugin\epubmg_common.py -Force
Copy-Item -Path .\_common\epubmg_common.py -Destination .\epubmg_interfaceplugin\epubmg_common.py -Force
