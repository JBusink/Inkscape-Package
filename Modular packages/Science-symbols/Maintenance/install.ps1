$ErrorActionPreference = 'Stop'
$package = Split-Path -Parent $PSScriptRoot
$catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'catalog.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$files = @($catalog.categories | ForEach-Object { Get-Item -LiteralPath (Join-Path $package $_.library) })
if ($files.Count -eq 0) { throw 'No libraries found. Run Build.cmd first.' }
foreach ($file in $files) {
    [xml]$svg = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    if ($svg.SelectNodes('//*[local-name()="text" or local-name()="tspan" or local-name()="flowRoot" or local-name()="foreignObject"]').Count) {
        throw "Live text found in $($file.Name). Installation cancelled."
    }
}
$profile = Join-Path $env:APPDATA 'inkscape'
$destination = Join-Path $profile 'symbols'
New-Item -ItemType Directory -Path $destination -Force | Out-Null
$previous = @(Get-ChildItem -LiteralPath $destination -File | Where-Object { $_.Name -match '^(Science|Physics)-.+\.svg$' })
if ($previous.Count) {
    $backup = Join-Path $profile ('science-symbols-backup-' + (Get-Date -Format 'yyyyMMdd-HHmmssfff') + '.zip')
    Compress-Archive -LiteralPath $previous.FullName -DestinationPath $backup
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    $archive = [IO.Compression.ZipFile]::OpenRead($backup)
    try {
        foreach ($old in $previous) {
            $entry = $archive.GetEntry($old.Name)
            if ($null -eq $entry) { throw "Backup entry missing: $($old.Name)" }
            $stream = $entry.Open()
            $sha = [Security.Cryptography.SHA256]::Create()
            try {
                $hash = [BitConverter]::ToString($sha.ComputeHash($stream)).Replace('-', '')
                if ($hash -ne (Get-FileHash -LiteralPath $old.FullName).Hash) { throw "Backup verification failed: $($old.Name)" }
            } finally { $stream.Dispose(); $sha.Dispose() }
        }
    } finally { $archive.Dispose() }
}
foreach ($file in $files) {
    $target = Join-Path $destination $file.Name
    Copy-Item -LiteralPath $file.FullName -Destination $target -Force
    if ((Get-FileHash -LiteralPath $file.FullName).Hash -ne (Get-FileHash -LiteralPath $target).Hash) {
        throw "Copy verification failed: $($file.Name)"
    }
}
# Remove retired managed libraries only after every current library is verified.
foreach ($old in $previous) {
    if ($old.Name -notin $files.Name) {
        if ((Split-Path -Parent $old.FullName) -ne $destination) { throw 'Unexpected legacy path.' }
        Remove-Item -LiteralPath $old.FullName
    }
}
Write-Host "$($files.Count) libraries installed. Save your work and restart Inkscape."

