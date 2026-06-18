Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$dir = "D:\Kapil\Books\Endangered Animals\temp_audit"
$scr = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
function S([string]$f) {
    $b = New-Object System.Drawing.Bitmap($scr.Width, $scr.Height)
    $g = [System.Drawing.Graphics]::FromImage($b)
    $g.CopyFromScreen($scr.Location, [System.Drawing.Point]::Empty, $scr.Size)
    $b.Save("$dir\$f", [System.Drawing.Imaging.ImageFormat]::Png); $g.Dispose(); $b.Dispose()
}
$n = $args[0]; [System.Windows.Forms.SendKeys]::SendWait("{RIGHT}"); Start-Sleep 800; S "_live_p$n.png"; Write-Output "P$n"
