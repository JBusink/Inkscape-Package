$ErrorActionPreference = 'Stop'
$sessionId = (Get-Process -Id $PID).SessionId
if (Get-Process -Name inkscape -ErrorAction SilentlyContinue | Where-Object { $_.SessionId -eq $sessionId }) {
    throw 'Save your work and close all Inkscape windows, then run Install.cmd again.'
}
$package = Split-Path -Parent $PSScriptRoot
$catalog = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'catalog.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$files = @($catalog.categories | ForEach-Object { Get-Item -LiteralPath (Join-Path $package $_.library) })
if ($files.Count -eq 0) { throw 'No libraries found. Run Build.cmd first.' }
foreach ($file in $files) {
    # Inkscape 1.4.x on Windows scans entire lines with a recursive regex.
    # Reject minified libraries before they can make the Symbols panel crash.
    $titleFound = $false
    foreach ($line in [IO.File]::ReadLines($file.FullName)) {
        if ($line.Length -gt 4096) { throw "Unsafe SVG header in $($file.Name). Rebuild or download the current package." }
        if ($line -match '^\s*<title>[^<]+</title>\s*$') { $titleFound = $true; break }
        if ($line -match '<defs\b') { break }
    }
    if (-not $titleFound) { throw "Missing separate library title in $($file.Name). Rebuild or download the current package." }
    [xml]$svg = Get-Content -LiteralPath $file.FullName -Raw -Encoding UTF8
    if ($svg.SelectNodes('//*[local-name()="text" or local-name()="tspan" or local-name()="flowRoot" or local-name()="foreignObject"]').Count) {
        throw "Live text found in $($file.Name). Installation cancelled."
    }
}
$profile = if ($env:INKSCAPE_PROFILE_DIR) { $env:INKSCAPE_PROFILE_DIR } else { Join-Path $env:APPDATA 'inkscape' }
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
Write-Host "$($files.Count) libraries installed in $destination"
Write-Host 'Start Inkscape. Open Object > Symbols (Ctrl+Shift+Y).'
Write-Host 'In the symbol-set selector, choose Optics, Circuits, or another category.'
Write-Host 'These are symbol libraries; they do not add entries to the Extensions menu.'

