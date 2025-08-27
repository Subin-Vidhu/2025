@echo off
echo 🚀 Creating Chrome Extension Package...
echo.

REM Create temporary directory
if exist "package_temp" rmdir /s /q "package_temp"
mkdir "package_temp"

REM Copy required files
echo Copying extension files...
copy "manifest.json" "package_temp\"
copy "content.js" "package_temp\"
copy "popup.html" "package_temp\"
copy "popup.js" "package_temp\"
copy "styles.css" "package_temp\"
copy "README.md" "package_temp\"

REM Copy icons (if they exist)
if exist "icon16.png" (
    copy "icon16.png" "package_temp\"
    echo ✅ icon16.png copied
) else (
    echo ⚠️  icon16.png missing - create icons first!
)

if exist "icon32.png" (
    copy "icon32.png" "package_temp\"
    echo ✅ icon32.png copied
) else (
    echo ⚠️  icon32.png missing - create icons first!
)

if exist "icon48.png" (
    copy "icon48.png" "package_temp\"
    echo ✅ icon48.png copied
) else (
    echo ⚠️  icon48.png missing - create icons first!
)

if exist "icon128.png" (
    copy "icon128.png" "package_temp\"
    echo ✅ icon128.png copied
) else (
    echo ⚠️  icon128.png missing - create icons first!
)

echo.
echo 📦 Files ready in package_temp folder
echo.
echo Next steps:
echo 1. Check that all icon files are created
echo 2. Create ZIP file from package_temp contents
echo 3. Upload to Chrome Web Store Developer Dashboard
echo.

REM Check if PowerShell is available for ZIP creation
where powershell >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo Creating ZIP file automatically...
    powershell Compress-Archive -Path "package_temp\*" -DestinationPath "jira-worklog-tracker.zip" -Force
    echo ✅ ZIP file created: jira-worklog-tracker.zip
) else (
    echo Please manually create ZIP file from package_temp folder contents
)

echo.
echo 🎉 Package creation complete!
pause
