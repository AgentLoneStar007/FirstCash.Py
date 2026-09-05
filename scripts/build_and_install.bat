@echo off
setlocal

echo --- Removing existing builds of library...
if exist "dist" rmdir /s /q "dist"

echo --- Activating virtual environment...
call ".venv\Scripts\activate.bat" || exit /b 1

echo --- Uninstalling existing build of library...
python -m pip uninstall -y firstcash

echo --- Building latest version of library...
python -m build || exit /b 1

echo --- Installing latest version...
for %%F in ("dist\*.whl") do (
    python -m pip install "%%F" --force-reinstall || exit /b 1
)

echo --- Done!

endlocal
