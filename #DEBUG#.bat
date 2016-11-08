@echo off
setlocal enabledelayedexpansion
start .\DevEnvSys\pydoc
set /p DebugFileName=<_DES_DEBUG.cfg
cls
call python !DebugFileName!
pause
