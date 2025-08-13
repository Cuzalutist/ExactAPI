@echo off
cd /d "%~dp0"
call conda activate Exact
python getExactTokenUpdate1.py >> output.log 2>&1
call conda deactivate
@REM pause
