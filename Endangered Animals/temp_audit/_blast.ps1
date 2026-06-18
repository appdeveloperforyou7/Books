Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class W32 {
    [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
    [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
}
"@

$p = (Get-Process | Where-Object { $_.MainWindowTitle -match "Chronicles" })[0]
[W32]::ShowWindow($p.MainWindowHandle, 9)
[W32]::SetForegroundWindow($p.MainWindowHandle)
Start-Sleep 800

$dir = "D:\Kapil\Books\Endangered Animals\temp_audit"
$scr = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds

function Shot([string]$f) {
    $b = New-Object System.Drawing.Bitmap($scr.Width, $scr.Height)
    $g = [System.Drawing.Graphics]::FromImage($b)
    $g.CopyFromScreen($scr.Location, [System.Drawing.Point]::Empty, $scr.Size)
    $b.Save("$dir\$f", [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $b.Dispose()
}

Shot "_live_p001.png"; Write-Output "Page 1 captured"
for ($i=2; $i -le 82; $i++) {
    [System.Windows.Forms.SendKeys]::SendWait("{RIGHT}")
    Start-Sleep 1000
    $n = "{0:D3}" -f $i
    Shot "_live_p$n.png"
    if ($i % 10 -eq 0) { Write-Output "Page $i captured" }
}
Write-Output "ALL 82 PAGES CAPTURED - DONE"
