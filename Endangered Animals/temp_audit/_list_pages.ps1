$pages = @(4,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81)
$dir = "D:\Kapil\Books\Endangered Animals\temp_audit"

foreach ($p in $pages) {
    $num = "{0:D2}" -f $p
    $file = "$dir\page_$num.jpg"
    if (Test-Path $file) {
        $size = (Get-Item $file).Length / 1KB
        Write-Output "P${num}: ${size:N0}KB"
    }
}
