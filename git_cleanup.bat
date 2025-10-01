@echo off
REM Git cleanup script - removes old files from git tracking

echo.
echo ====================================================================
echo    GIT CLEANUP - Removing old files from Git tracking
echo ====================================================================
echo.

cd /d "%~dp0"

echo Removing old root files...
git rm --cached models.py 2>nul && echo   [OK] Removed models.py || echo   [--] models.py not in git
git rm --cached config.py 2>nul && echo   [OK] Removed config.py || echo   [--] config.py not in git  
git rm --cached test_emails.txt 2>nul && echo   [OK] Removed test_emails.txt || echo   [--] test_emails.txt not in git

echo.
echo Removing old agent files...
git rm --cached agents\categorizer.py 2>nul && echo   [OK] Removed categorizer.py || echo   [--] categorizer.py not in git
git rm --cached agents\classifier.py 2>nul && echo   [OK] Removed classifier.py || echo   [--] classifier.py not in git
git rm --cached agents\sentiment.py 2>nul && echo   [OK] Removed sentiment.py || echo   [--] sentiment.py not in git
git rm --cached agents\urgency.py 2>nul && echo   [OK] Removed urgency.py || echo   [--] urgency.py not in git
git rm --cached agents\router.py 2>nul && echo   [OK] Removed router.py || echo   [--] router.py not in git
git rm --cached agents\responder.py 2>nul && echo   [OK] Removed responder.py || echo   [--] responder.py not in git

echo.
echo ====================================================================
echo    CLEANUP COMPLETE!
echo ====================================================================
echo.

echo Current git status:
git status --short

echo.
echo ====================================================================
echo    NEXT STEPS:
echo ====================================================================
echo    1. Review the changes above
echo    2. git add .
echo    3. git commit -m "Complete insurance claims multi-agent system"
echo    4. git push origin main
echo ====================================================================
echo.

pause
