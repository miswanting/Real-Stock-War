@echo off
start pydoc.bat
del *.log
cd dist
del *.log
cls
call python app_standalone.py
cd ..
move /Y dist\*.log .\
pause
