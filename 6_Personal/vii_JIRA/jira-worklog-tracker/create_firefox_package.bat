@echo off
echo 🦊 Creating Firefox Extension Package...
echo.

REM Create temporary directory for Firefox
if exist "firefox_package" rmdir /s /q "firefox_package"
mkdir "firefox_package"

REM Copy required files
echo Copying extension files for Firefox...
copy "content.js" "firefox_package\"
copy "popup.html" "firefox_package\"
copy "popup.js" "firefox_package\"
copy "styles.css" "firefox_package\"
copy "README.md" "firefox_package\"

REM Use Firefox manifest
copy "manifest_firefox.json" "firefox_package\manifest.json"
echo ✅ Firefox manifest copied

REM Copy icons (if they exist)
if exist "icon16.png" (
    copy "icon16.png" "firefox_package\"
    copy "icon32.png" "firefox_package\"
    copy "icon48.png" "firefox_package\"
    copy "icon128.png" "firefox_package\"
    echo ✅ Icons copied
) else (
    echo ⚠️  Icons missing - create icons first!
)

echo.
echo 📦 Firefox package ready in firefox_package folder
echo.

REM Create ZIP for Firefox
where powershell >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Creating Firefox ZIP file...
    powershell Compress-Archive -Path "firefox_package\*" -DestinationPath "jira-worklog-tracker-firefox.zip" -Force
    echo ✅ Firefox ZIP created: jira-worklog-tracker-firefox.zip
) else (
    echo Please manually create ZIP file from firefox_package folder contents
)

echo.
echo 🦊 Firefox package creation complete!
echo Upload to https://addons.mozilla.org/developers/
pause
