@echo off
setlocal

REM Запуск завдань через явний шлях до встановленого Python (без залежності від PATH/Microsoft Store alias).
set "PY=%LocalAppData%\Programs\Python\Python314\python.exe"

if not exist "%PY%" (
  echo Python не знайдено за шляхом:
  echo   %PY%
  echo Встанови Python або виправ шлях у цьому файлі.
  pause
  exit /b 1
)

REM Увімкнути UTF-8 для коректного виводу українських символів у консолі
chcp 65001 >nul

echo === Завдання 1 ===
"%PY%" "%~dp0task1.py"
echo.
echo === Завдання 2 ===
"%PY%" "%~dp0task2.py"

echo.
pause

