@echo off
echo 🌐 Creating packages for ALL browsers (FREE distribution)...
echo.

REM Create Chrome package
echo 📦 Creating Chrome package...
call create_package.bat

REM Create Firefox package  
echo.
echo 🦊 Creating Firefox package...
call create_firefox_package.bat

REM Create Edge package (same as Chrome)
echo.
echo 🔷 Creating Edge package...
if exist "edge_package" rmdir /s /q "edge_package"
mkdir "edge_package"

copy "manifest.json" "edge_package\"
copy "content.js" "edge_package\"
copy "popup.html" "edge_package\"
copy "popup.js" "edge_package\"
copy "styles.css" "edge_package\"
copy "README.md" "edge_package\"

if exist "icon16.png" (
    copy "icon*.png" "edge_package\"
    echo ✅ Edge package ready
)

where powershell >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    powershell Compress-Archive -Path "edge_package\*" -DestinationPath "jira-worklog-tracker-edge.zip" -Force
    echo ✅ Edge ZIP created
)

echo.
echo 🎉 ALL PACKAGES CREATED!
echo.
echo 📁 Files created:
echo   ✅ jira-worklog-tracker.zip (Chrome/Brave/Opera)
echo   ✅ jira-worklog-tracker-firefox.zip (Firefox)  
echo   ✅ jira-worklog-tracker-edge.zip (Microsoft Edge)
echo.
echo 🚀 FREE DISTRIBUTION OPTIONS:
echo   1. GitHub Releases (upload ZIP files)
echo   2. Firefox Add-ons Store (FREE, official)
echo   3. Microsoft Edge Add-ons (FREE, official)
echo   4. Direct sharing (send ZIP to colleagues)
echo.
echo 💰 COSTS: $0.00 - Completely FREE!
echo.
pause
