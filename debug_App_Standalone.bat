@echo off
start pydoc.bat
del *.log
cd dist
del *.log
cls
call app_standalone.py
cd ..
move /Y dist\*.log .\
pause
