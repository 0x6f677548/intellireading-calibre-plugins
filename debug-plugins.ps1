#verify if we got a param with calibre directory path
if ($args.count -eq 0) {

    #verify if we have a environment variable with calibre directory path
    if ($env:CALIBRE_DIR) {
        $calibreDir = $env:CALIBRE_DIR
    } else {
        #ask for calibre directory path
        $calibreDir = Read-Host "Please enter the path to calibre directory (ex: C:\Program Files\calibre):"
        #set environment variable with calibre directory path
        $env:CALIBRE_DIR = $calibreDir
    }
} else {
    $calibreDir = $args[0]
}

.\copy-commonfiles.ps1


#output calibre directory path
Write-Output "Calibre directory: $calibreDir"



#array of plugins to remove and add
$plugins = @(
    @("Epub Metaguider post processor (intellireading.com)",'.\epubmg_filetypeplugin\'),
    @("Epub Metaguider output format (intellireading.com)", '.\epubmg_outputplugin\'),
    @("Epub Metaguider GUI (intellireading.com)", '.\epubmg_interfaceplugin\')
)


# remove and rebuild all plugins
foreach ($plugin in $plugins) {
    #output plugin name
    Write-Output "Removing and reinstalling '$($plugin[0])' with path '$($plugin[1])'"
    &$calibreDir\calibre-customize.exe -r $plugin[0]
    &$calibreDir\calibre-customize.exe -b $plugin[1]
}

&$calibreDir\calibre-debug.exe -g