param(
    [int]$TotalPages = 82,
    [string]$OutputDir = "D:\Kapil\Books\Endangered Animals\temp_audit"
)

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

# Activate Acrobat first
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32Helper {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

$procs = Get-Process | Where-Object { $_.MainWindowTitle -ne "" -and ($_.ProcessName -match "acrobat|acrord|reader") }
if ($procs) {
    $p = $procs[0]
    [Win32Helper]::ShowWindow($p.MainWindowHandle, 9)
    [Win32Helper]::SetForegroundWindow($p.MainWindowHandle)
    Start-Sleep -Milliseconds 800
}

# Screenshot function
function TakeScreenshot([string]$path) {
    $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
    $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($screen.Location, [System.Drawing.Point]::Empty, $screen.Size)
    $bitmap.Save($path, [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
}

# Capture Page 1 (current)
TakeScreenshot "$OutputDir\_live_p01.png"
Write-Output "Captured page 1"

# Navigate and capture remaining pages
for ($i = 2; $i -le $TotalPages; $i++) {
    # Press Right Arrow to go to next page
    [System.Windows.Forms.SendKeys]::SendWait("{RIGHT}")
    Start-Sleep -Milliseconds 550
    
    $num = "{0:D3}" -f $i
    TakeScreenshot "$OutputDir\_live_p$num.png"
    
    if ($i % 10 -eq 0) {
        Write-Output "Captured page $i / $TotalPages..."
    }
}

Write-Output "DONE! All $TotalPages pages captured."
