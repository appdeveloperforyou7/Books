Add-Type @"
using System;
using System.Runtime.InteropServices;
public class Win32 {
    [DllImport("user32.dll")]
    public static extern bool SetForegroundWindow(IntPtr hWnd);
    [DllImport("user32.dll")]
    public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
}
"@

# Try to find Acrobat/Reader window by title
$procs = Get-Process | Where-Object { $_.MainWindowTitle -ne "" -and ($_.ProcessName -match "acrobat|acrord|reader") }
if ($procs) {
    foreach ($p in $procs) {
        Write-Output "Found: $($p.ProcessName) - $($p.MainWindowTitle)"
        [Win32]::ShowWindow($p.MainWindowHandle, 9) # SW_RESTORE
        [Win32]::SetForegroundWindow($p.MainWindowHandle)
        Start-Sleep -Milliseconds 500
    }
} else {
    Write-Output "No Acrobat/Reader window found. Trying any PDF viewer..."
    $all = Get-Process | Where-Object { $_.MainWindowTitle -ne "" } | Select-Object ProcessName, MainWindowTitle | Format-Table -AutoSize
    Write-Output $all
}
