@echo off
echo Specify the file name (without extention):
set /p filename=

python main.py "%filename%"