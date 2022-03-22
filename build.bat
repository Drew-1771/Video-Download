@echo off
:: /Q for quiet
IF EXIST %cd%\Video-Downloader RMDIR /S %cd%\Video-Downloader
pyinstaller --noconsole src/main.py
rename %cd%\dist\main\main.exe Video-Download.exe
move %cd%\dist\main %cd%\dist\src
md %cd%\Video-Downloader
move %cd%\dist\src %cd%\Video-Downloader
del %cd%\main.spec
RMDIR %cd%\dist /S /Q %cd%\dist