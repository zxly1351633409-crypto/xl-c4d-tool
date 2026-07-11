param(
    [string]$Version = "3.4.0-public-core"
)

$ErrorActionPreference = "Stop"
$repoRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot ".."))
$addonRoot = Join-Path $repoRoot "xl_c4d_tool"
$distRoot = Join-Path $repoRoot "dist"
$zipPath = Join-Path $distRoot ("xl_c4d_tool-{0}.zip" -f $Version)

if (-not (Test-Path -LiteralPath (Join-Path $addonRoot "__init__.py"))) {
    throw "Missing xl_c4d_tool/__init__.py"
}

$forbidden = Get-ChildItem -LiteralPath $addonRoot -Recurse -Force | Where-Object {
    $_.Name -match '^(logs?|__pycache__|_backups)$' -or
    $_.Name -match '\.pyc$|\.blend[12@]$' -or
    $_.FullName -match '[\\/]material_nodes[\\/]' -or
    $_.Name -ieq 'Claymate.blend'
}
if ($forbidden) {
    throw "Public add-on contains forbidden release entries."
}

if (-not (Test-Path -LiteralPath $distRoot)) {
    New-Item -ItemType Directory -Path $distRoot | Out-Null
}
Compress-Archive -LiteralPath $addonRoot -DestinationPath $zipPath -CompressionLevel Optimal -Force

Add-Type -AssemblyName System.IO.Compression.FileSystem
$zip = [System.IO.Compression.ZipFile]::OpenRead($zipPath)
try {
    $names = @($zip.Entries | ForEach-Object { $_.FullName.Replace('\', '/') })
    $badRoot = @($names | Where-Object { $_ -and -not $_.StartsWith('xl_c4d_tool/') })
    $badEntries = @($names | Where-Object {
        $_ -match '(^|/)(logs?|__pycache__|_backups)(/|$)' -or
        $_ -match '\.pyc$|\.blend[12@]$' -or
        $_ -match '(^|/)material_nodes/' -or
        $_ -match 'Claymate\.blend$'
    })
    if ($badRoot.Count -or $badEntries.Count) {
        throw "Release ZIP audit failed."
    }
}
finally {
    $zip.Dispose()
}

$item = Get-Item -LiteralPath $zipPath
if ($item.Length -ge 100MB) {
    throw "Release ZIP is too large for a normal GitHub repository workflow; use a Release asset and re-audit contents."
}

$hash = Get-FileHash -LiteralPath $zipPath -Algorithm SHA256
[pscustomobject]@{
    Path = $zipPath
    Bytes = $item.Length
    SHA256 = $hash.Hash
}
