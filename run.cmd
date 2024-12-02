@echo off
pyuic5.exe -x .\interface.ui -o ui_interface.py
pyrcc5.exe .\resources.qrc -o .\resources_rc.py
python -B main.py