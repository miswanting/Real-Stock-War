@echo off
setlocal enabledelayedexpansion
set /p MainFileName=<_DES_MAIN.cfg
echo 1.Generate Spec File
echo 2.Pack
set /p c=Choose:

if /i "%c%"=="1" goto Generate_Spec_File
if /i "%c%"=="2" goto Pack
echo No
ping -n 2 localhost>nul

:Generate_Spec_File
cls
pyi-makespec -F --log-level DEBUG !MainFileName!
goto End

:Pack
cls
rmdir /s /q build
rmdir /s /q dist
pyinstaller --specpath !MainFileName!.spec
goto End

:End
pause
