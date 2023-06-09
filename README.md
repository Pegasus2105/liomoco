# liomoco - my private linux iOptron mount commander
## GUI and model for iOptron astronomical mounts.

This is only a	advance notice. The publication will be in the next time.

Programmming language: Python and PyQt5

Operating system: linux (it may be run under windows, but it's not tested.)

Suitable for CEM120 series, CEM70 series, GEM45 series with firmware 210101 and later, CEM40 series with
firmware 210101 and later, GEM28 series and CEM26 series.

Status: Alpha (experimental)
## Requirements
1. python 3.10 or higher
2. PyQt5 (QtCore, QtGui, QtWidgets, QTimer)
3. modul: pyserial
4. iOptron mount (CEM120 series, CEM70 series, GEM45 series with firmware 210101 and later, CEM40 series with
firmware 210101 and later, GEM28 series and CEM26 series, tested with: CEM26 with GPS and without encoders under ubuntu)
5. serial or WLAN connection to the mount
## Istallation
1. make a new folder like: 'liomoco'
2. copy all files into the folder
3. open a terminal
4. go to the created folder
5. type for start: python3 iOptronGUI.py
## Preview
![GUI preview](https://github.com/Pegasus2105/liomoco/blob/main/picture/liomoco01.png)
![GUI preview](https://github.com/Pegasus2105/liomoco/blob/main/picture/liomoco02.png)
![GUI preview](https://github.com/Pegasus2105/liomoco/blob/main/picture/liomoco03.png)
![GUI preview](https://github.com/Pegasus2105/liomoco/blob/main/picture/liomoco04.png)
![GUI preview](https://github.com/Pegasus2105/liomoco/blob/main/picture/setup.png)
## Citations and sources
This project uses parts of other projects, or has implemented ideas shown in them, including:

https://github.com/chimerasaurus/ioptron-python

This project uses the following open specifications:

iOptron® Mount RS-232 Command Language
