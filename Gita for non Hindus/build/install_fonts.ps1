$src  = 'D:\Kapil\Books\Gita for non Hindus\build\fonts'
$dest = "$env:LOCALAPPDATA\Microsoft\Windows\Fonts"
$reg  = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Fonts'
New-Item -ItemType Directory -Force -Path $dest | Out-Null
if (-not (Test-Path $reg)) { New-Item -Path $reg -Force | Out-Null }
$count = 0
Get-ChildItem $src -Filter *.ttf | ForEach-Object {
    $destFile = Join-Path $dest $_.Name
    Copy-Item $_.FullName $destFile -Force
    $base = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
    New-ItemProperty -Path $reg -Name "$base (TrueType)" -Value $destFile -PropertyType String -Force | Out-Null
    $count++
}
"Installed $count TTF fonts per-user."
