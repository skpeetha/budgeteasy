@echo off
cd /d "G:\Srikanth\budgeteasy"
$env:PYTHONPATH="g:\Srikanth\budgeteasy"
python web\app.py
call venv\Scripts\activate.bat
code .
