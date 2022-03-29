@echo off
:: /Q for quiet
IF EXIST %cd%\Video-Downloader RMDIR /S %cd%\Video-Downloader
call .\env\Scripts\activate && pyinstaller --noconsole src/main.py
call deactivate
rename %cd%\dist\main\main.exe Video-Download.exe
move %cd%\dist\main %cd%\dist\src
md %cd%\Video-Downloader
move %cd%\dist\src %cd%\Video-Downloader
IF EXIST %cd%\main.spec del %cd%\main.spec
RMDIR %cd%\dist /S /Q %cd%\dist