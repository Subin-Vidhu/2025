# Script to find files modified on March 8th (any year) with focus on .csv and .py files
# Run this in PowerShell as Administrator for best results

param(
    [int]$Year = (Get-Date).Year  # Default to current year, but can specify different year
)

Write-Host "Searching for files modified on March 8, $Year..." -ForegroundColor Green
Write-Host "=" * 60

# Get all local drives (excluding network drives)
$localDrives = Get-WmiObject -Class Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 } | Select-Object -ExpandProperty DeviceID

Write-Host "Local drives found: $($localDrives -join ', ')" -ForegroundColor Yellow
Write-Host ""

# Initialize collections for results
$csvFiles = @()
$pyFiles = @()
$otherFiles = @()

foreach ($drive in $localDrives) {
    Write-Host "Searching drive $drive..." -ForegroundColor Cyan
    
    try {
        # Search for all files modified on March 8th of the specified year
        $files = Get-ChildItem -Path "$drive\" -Recurse -File -ErrorAction SilentlyContinue | 
                 Where-Object { 
                     $_.LastWriteTime.Date -eq (Get-Date -Year $Year -Month 3 -Day 8).Date 
                 }
        
        foreach ($file in $files) {
            $fileInfo = [PSCustomObject]@{
                Name = $file.Name
                FullPath = $file.FullName
                Size = [math]::Round($file.Length / 1KB, 2)
                LastModified = $file.LastWriteTime
                Extension = $file.Extension.ToLower()
            }
            
            switch ($file.Extension.ToLower()) {
                '.csv' { $csvFiles += $fileInfo }
                '.py' { $pyFiles += $fileInfo }
                default { $otherFiles += $fileInfo }
            }
        }
        
        Write-Host "Drive $drive completed." -ForegroundColor Green
    }
    catch {
        Write-Host "Error accessing drive $drive : $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "RESULTS SUMMARY" -ForegroundColor Magenta
Write-Host "=" * 60

# Display CSV files
if ($csvFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "CSV FILES MODIFIED ON MARCH 8, $Year ($($csvFiles.Count) found):" -ForegroundColor Green
    Write-Host "-" * 50
    $csvFiles | Sort-Object FullPath | Format-Table -Property Name, @{Name="Size(KB)"; Expression={$_.Size}}, LastModified, FullPath -AutoSize
} else {
    Write-Host ""
    Write-Host "No CSV files found modified on March 8, $Year" -ForegroundColor Yellow
}

# Display Python files
if ($pyFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "PYTHON FILES MODIFIED ON MARCH 8, $Year ($($pyFiles.Count) found):" -ForegroundColor Green
    Write-Host "-" * 50
    $pyFiles | Sort-Object FullPath | Format-Table -Property Name, @{Name="Size(KB)"; Expression={$_.Size}}, LastModified, FullPath -AutoSize
} else {
    Write-Host ""
    Write-Host "No Python files found modified on March 8, $Year" -ForegroundColor Yellow
}

# Display other files (optional - uncomment if you want to see all files)
if ($otherFiles.Count -gt 0) {
    Write-Host ""
    Write-Host "OTHER FILES MODIFIED ON MARCH 8, $Year ($($otherFiles.Count) found):" -ForegroundColor Green
    Write-Host "-" * 50
    # Group by extension for better overview
    $otherFiles | Sort-Object Extension, FullPath | Format-Table -Property Name, Extension, @{Name="Size(KB)"; Expression={$_.Size}}, LastModified, FullPath -AutoSize
} else {
    Write-Host ""
    Write-Host "No other files found modified on March 8, $Year" -ForegroundColor Yellow
}

# Summary statistics
Write-Host ""
Write-Host "TOTAL SUMMARY:" -ForegroundColor Magenta
Write-Host "CSV files: $($csvFiles.Count)"
Write-Host "Python files: $($pyFiles.Count)"
Write-Host "Other files: $($otherFiles.Count)"
Write-Host "Total files: $(($csvFiles.Count + $pyFiles.Count + $otherFiles.Count))"

# Option to export results to CSV
$exportChoice = Read-Host "`nWould you like to export results to a CSV file? (y/n)"
if ($exportChoice -eq 'y' -or $exportChoice -eq 'Y') {
    $allResults = $csvFiles + $pyFiles + $otherFiles
    $exportPath = "March8_ModifiedFiles_$Year.csv"
    $allResults | Export-Csv -Path $exportPath -NoTypeInformation
    Write-Host "Results exported to: $exportPath" -ForegroundColor Green
}

Write-Host ""
Write-Host "Search completed!" -ForegroundColor Green