@echo off
goto set

:set
cls
title Run Rutap Bot 2019 - Preparing
chcp 65001
color 0b
goto main

:main
cls
title Run Rutap Bot 2019 - Main
echo.
echo 1. Module Insatll OR Update
echo 2. Run Rutap Bot 2019
echo 3. Exit
echo.
set /p b=Input a number and press Enter. : 
if %b% == 1 goto Module_Install
if %b% == 2 goto Run
if %b% == 3 goto out

:out
exit

:Module_Install
cls
title Run Rutap Bot 2019 - Please check this!
echo If you have Python 3.6 and you run this file as an administrator, press Enter.
pause
cls
title Run Rutap Bot 2019 - Module Install OR Update
echo.
echo ==============================
echo Please Wait...
echo ==============================
echo.
cd %USERPROFILE%\AppData\Local\pip
del /f /s /q cache > NUL
python -m pip install --upgrade pip
python -m pip install -U discord.py
python -m pip install datetime
python -m pip install numpy
python -m pip install pillow
python -m pip install psutil
python -m pip install pymysql
python -m pip install requests
python -m pip install beautifulsoup4
python -m pip install oauth2
python -m pip install pycryptodome
python -m pip install hurry.filesize
echo.
echo ==============================
echo Press Enter to return to Main.
echo ==============================
echo.
pause
goto main

:Run
cls
title Run Rutap Bot 2019 - run rutap.py
echo.
echo ==============================
echo Please Wait...
echo ==============================
echo.
python rutap.py
echo.
echo ==============================
echo Press Enter to return to Main.
echo ==============================
echo.
pause
goto set
