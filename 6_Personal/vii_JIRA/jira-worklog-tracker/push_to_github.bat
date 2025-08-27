@echo off
echo 🚀 GitHub Repository Setup
echo.
echo ✅ Current Status:
echo   - Git repository initialized
echo   - All files committed
echo   - Ready to push to GitHub
echo.
echo 📋 Next Steps:
echo.
echo 1. CREATE GITHUB REPOSITORY:
echo    - Go to: https://github.com/new
echo    - Name: jira-worklog-tracker
echo    - Make it PUBLIC
echo    - Don't initialize with README (we have files)
echo.
echo 2. CONNECT AND PUSH:
set /p username="Enter your GitHub username: "
echo.
echo Running git commands...
echo.

git remote add origin https://github.com/%username%/jira-worklog-tracker.git
git branch -M main
git push -u origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS! Repository pushed to GitHub
    echo.
    echo 🔗 Your repository: https://github.com/%username%/jira-worklog-tracker
    echo.
    echo 📋 NEXT: Create Release
    echo   1. Go to: https://github.com/%username%/jira-worklog-tracker/releases
    echo   2. Click "Create a new release"
    echo   3. Tag: v1.0.0
    echo   4. Upload the ZIP files from this folder
    echo   5. Use description from GITHUB_SETUP_GUIDE.md
    echo.
    echo 🎉 Your extension will be publicly available!
) else (
    echo ❌ Error occurred. Make sure you:
    echo   1. Created the GitHub repository first
    echo   2. Have internet connection
    echo   3. Are logged into Git
    echo.
    echo Try running: git remote -v
    echo To check if remote was added correctly
)
echo.
pause
