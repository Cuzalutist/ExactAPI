@echo off
cd /d "%~dp0"
call conda activate Exact
python getExactTokenUpdate1.py
call conda deactivate
@REM pause
