
pyuic5 mainwindow.ui -x -o ../imprimeti/qt/mainwindow_ui.py

pyuic5 setupwindow.ui -x -o ../imprimeti/qt/setupwindow_ui.py

pyrcc5 -o ../imprimeti/qt/icons_rc.py icons.qrc
