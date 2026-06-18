param(
    [string]$Key = "Right",
    [int]$Delay = 600
)

Add-Type -AssemblyName System.Windows.Forms

# Map key names
$keyMap = @{
    "Right" = [System.Windows.Forms.Keys]::Right
    "Left"  = [System.Windows.Forms.Keys]::Left
    "Down"  = [System.Windows.Forms.Keys]::Down
    "Up"    = [System.Windows.Forms.Keys]::Up
}

$k = $keyMap[$Key]
if (-not $k) { $k = [System.Windows.Forms.Keys]::$Key }

[System.Windows.Forms.SendKeys]::SendWait("{$Key}")
Start-Sleep -Milliseconds $Delay
Write-Output "Pressed $Key key"
