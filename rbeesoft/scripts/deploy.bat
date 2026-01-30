@echo off

setlocal

set /p CONFIRM="Did you update the CHANGELOG? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

set /p BUMP_LEVEL="What version bump level do you want to use? [major, minor, patch (default)] "
if /I "%BUMP_LEVEL%"=="major" (
    poetry version major
) else if /I "%BUMP_LEVEL%"=="minor" (
    poetry version minor
) else (
    poetry version patch
)

set /p TOKEN=<"G:\My Drive\data\ApiKeysAndPasswordFiles\pypi-token.txt"
poetry publish --build --username __token__ --password %TOKEN%

endlocal