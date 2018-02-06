@echo off

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/src/main/resources/scripts/win 1D_ranging.py

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/src/main/resources/scripts/win 3D_positioning.py

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/src/main/resources/scripts/win motion_data.py

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/src/main/resources/scripts/win graphing_realtime_2D.py

wscript "send_yes.vbs"
pyinstaller --distpath PozyxGUI/pozyxgui/src/main/resources/scripts/win configure_uwb_settings.py
wscript "send_yes.vbs"

pause