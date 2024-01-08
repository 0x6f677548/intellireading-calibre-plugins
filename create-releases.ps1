param (
    [string]$version = "1.0.0"
)


#create a zip file for each child folder in the current directory that does not start with a _ or a .
#the zip file will be named after the folder
#the zip file will be created in the _releases folder
#usage example: create-releases.ps1 -version 1.0.0

#validate that the version is in the correct format
if ($version -notmatch "^\d+\.\d+\.\d+$") {
    Write-Error "Version must be in the format x.x.x"
    Write-Error "Example: 1.0.0"
    Write-Error "Usage: create-releases.ps1 -version 1.0.0"
    exit
}


Write-Output "Creating release $version in _releases"




$root = Get-Location
#the releases folder will be "_releases\" plus the version
$releases = Join-Path $root "_releases\$version"
if (!(Test-Path $releases)) {
    New-Item -ItemType Directory -Path $releases
}

$folders = Get-ChildItem -Path $root -Directory -Exclude "_releases", ".common"

foreach ($folder in $folders) {
    $zip = Join-Path $releases "$($folder.Name).zip"
    if (Test-Path $zip) {
        Remove-Item $zip
    }
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::CreateFromDirectory($folder.FullName, $zip)
}


Write-Output "Created releases:"
#list the files in the releases folder
Get-ChildItem -Path $releases


