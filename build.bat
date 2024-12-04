@echo off
:: set variables for paths
set APP_NAME=Video-Download
set BUILD_DIR=%cd%\dist
set FINAL_DIR=%cd%\Video-Downloader
set VENV_DIR=%cd%\env\Scripts

:: clean previous builds
IF EXIST %FINAL_DIR% RMDIR /S /Q %FINAL_DIR%
IF EXIST %BUILD_DIR% RMDIR /S /Q %BUILD_DIR%
IF EXIST %cd%\build RMDIR /S /Q %cd%\build
IF EXIST %cd%\main.spec DEL %cd%\main.spec

call %VENV_DIR%\activate

:: build w/ PyInstaller (adds metadata, ensure fresh builds)
pyinstaller --noconsole --clean --name "%APP_NAME%" ^
src/main.py

call %VENV_DIR%\deactivate

:: organize output into final folder
MD %FINAL_DIR%
MOVE %BUILD_DIR%\%APP_NAME% %FINAL_DIR%

:: clean residual files
IF EXIST %cd%\main.spec DEL %cd%\main.spec
IF EXIST %cd%\%APP_NAME%.spec DEL %cd%\%APP_NAME%.spec
RMDIR /S /Q %BUILD_DIR%
RMDIR /S /Q %cd%\build

echo build complete @ "%FINAL_DIR%"
pause
