@echo off
start pydoc.bat
del *.log
cd dist
del *.log
cls
call python test.py
cd ..
move /Y dist\*.log .\
pause
