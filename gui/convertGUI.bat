@echo off
for %%A in (.\*.ui) do (
	For %%B in ("%%A") do (
		pyuic5 -x %%~nB.ui -o %%~nB.py
	)
)
pause
