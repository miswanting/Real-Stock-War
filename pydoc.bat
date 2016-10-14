@echo off
cd dist
cls
pydoc -w app_standalone
cd ..
move .\dist\*.html .\
exit
