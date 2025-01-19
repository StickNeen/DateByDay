@echo off
setlocal

rem Loop through all arguments
set "args="
:loop
if "%~1"=="" goto done
set "args=%args% %~1"
shift
goto loop

:done
rem Replace "streamlit" with "python -m streamlit"
set "args=%args:streamlit=python -m streamlit%"
echo %args%

rem Execute the command
%args%

endlocal