#from PyQt5 import QtCore, QtGui, QtWidgets

from   PyQt5 import QtCore, QtGui, QtWidgets
from   PyQt5.QtWidgets import *
from   PyQt5 import QtCore
from   PyQt5.QtCore import Qt
from   PyQt5.QtCore import QTimer
import utilities
import sys
from   colorscheme import colorPopupDialogScheme


class PopupDialog(QDialog):
    '''This Class define a simple own dialog for information without buttons.
       parameters:
       title = window title in the titleBar : str
       message     = textmessage : str
       displayTime = time to stay at the display (second * 10): int'''
    def __init__(self, title, message, displayTime, colScheme):
        super().__init__()
        self.count = 0
        self.displayTime = displayTime 
        # this will hide the title bar
        self.setWindowFlag(Qt.FramelessWindowHint)

        # set the title
        self.setWindowTitle(title)
        self.setGeometry(400, 300, 400, 120)
  
        # creating a label widget
        # by default label will display at top left corner
        self.label1 = QLabel(title, self)
        self.label1.setGeometry(0, 0, 400, 40)
        self.label1.setAlignment(Qt.AlignCenter)
        self.label2 = QLabel(message, self)
        self.label2.setGeometry(0, 40, 400, 80)
        self.label2.setAlignment(QtCore.Qt.AlignCenter)
  
        # setting up border and background color
        head, body = colorPopupDialogScheme(colScheme)
        self.label1.setStyleSheet('QLabel{background-color:' + head + '}''QLabel{color:white}''QLabel{font: bold 20px}')
        self.label2.setStyleSheet('QLabel{background-color:' + body + '}')

        # show all the widgets
        self.show()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.display)
        self.timer.start(100)

    def display(self):
        self.count += 1
        if self.count > self.displayTime:
            self.timer.stop()
            self.close()


#************************************************************************************
class SetupDialog(QDialog):
    '''This Class define the dialog for setup window.
       parameters:
       title = window title in the titleBar : str'''
    def __init__(self, title):
        super().__init__()
        self.connChanged = False

        # read setup.ini
        self.configData = utilities.readConfig()
        self.connChanged = False

        # set the title
        self.setWindowTitle(title)
        self.setGeometry(400, 300, 510, 550)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.groupBoxMountMove = QtWidgets.QGroupBox(self)
        self.groupBoxMountMove.setGeometry(QtCore.QRect(30, 350, 451, 121))
        self.groupBoxMountMove.setObjectName("groupBoxMountMove")
        self.groupBoxMountMove.setTitle("mount move")
        self.layoutWidget = QtWidgets.QWidget(self.groupBoxMountMove)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 40, 141, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.labelStartSpeed = QtWidgets.QLabel(self.layoutWidget)
        self.labelStartSpeed.setObjectName("labelStartSpeed")
        self.labelStartSpeed.setText("Start Speed")
        self.gridLayout_3.addWidget(self.labelStartSpeed, 0, 0, 1, 1)
        self.labelTrackingAtStart = QtWidgets.QLabel(self.layoutWidget)
        self.labelTrackingAtStart.setObjectName("labelTrackingAtStart")
        self.labelTrackingAtStart.setText("Tracking at Start")
        self.gridLayout_3.addWidget(self.labelTrackingAtStart, 1, 0, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBoxMountMove)
        self.layoutWidget1.setGeometry(QtCore.QRect(260, 40, 101, 71))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.comboBoxStartSpeed = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBoxStartSpeed.setObjectName("comboBoxStartSpeed")
        self.comboBoxStartSpeed.addItem("1x")
        self.comboBoxStartSpeed.addItem("2x")
        self.comboBoxStartSpeed.addItem("8x")
        self.comboBoxStartSpeed.addItem("16x")
        self.comboBoxStartSpeed.addItem("64x")
        self.comboBoxStartSpeed.addItem("128x")
        self.comboBoxStartSpeed.addItem("256c")
        self.comboBoxStartSpeed.addItem("512x")
        self.comboBoxStartSpeed.addItem("Max")
        self.gridLayout_4.addWidget(self.comboBoxStartSpeed, 0, 0, 1, 1)
        self.comboBoxTrackingAtStart = QtWidgets.QComboBox(self.layoutWidget1)
        self.comboBoxTrackingAtStart.setObjectName("comboBoxTrackingAtStart")
        self.comboBoxTrackingAtStart.addItem("on")
        self.comboBoxTrackingAtStart.addItem("off")
        self.gridLayout_4.addWidget(self.comboBoxTrackingAtStart, 1, 0, 1, 1)
        self.groupBoxGeneral = QtWidgets.QGroupBox(self)
        self.groupBoxGeneral.setGeometry(QtCore.QRect(30, 20, 450, 300))
        self.groupBoxGeneral.setObjectName("groupBoxGeneral")
        self.groupBoxGeneral.setTitle("general")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBoxGeneral)
        self.layoutWidget2.setGeometry(QtCore.QRect(30, 41, 221, 241))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.labelMountIpAddress = QtWidgets.QLabel(self.layoutWidget2)
        self.labelMountIpAddress.setObjectName("labelMountIpAddress")
        self.labelMountIpAddress.setText("Mount Ip-Address")
        self.gridLayout.addWidget(self.labelMountIpAddress, 3, 0, 1, 1)
        self.labelPollingCoordinates = QtWidgets.QLabel(self.layoutWidget2)
        self.labelPollingCoordinates.setObjectName("labelPollingCoordinates")
        self.labelPollingCoordinates.setText("Polling Rate Coordinates")
        self.gridLayout.addWidget(self.labelPollingCoordinates, 5, 0, 1, 1)
        self.labelPollingRefresh = QtWidgets.QLabel(self.layoutWidget2)
        self.labelPollingRefresh.setObjectName("labelPollingRefresh")
        self.labelPollingRefresh.setText("Polling Rate Refresh")
        self.gridLayout.addWidget(self.labelPollingRefresh, 6, 0, 1, 1)
        self.labelWlanSsid = QtWidgets.QLabel(self.layoutWidget2)
        self.labelWlanSsid.setObjectName("labelWlanSsid")
        self.labelWlanSsid.setText("WLAN SSID")
        self.gridLayout.addWidget(self.labelWlanSsid, 2, 0, 1, 1)
        self.labelFavoredConnection = QtWidgets.QLabel(self.layoutWidget2)
        self.labelFavoredConnection.setObjectName("labelFavoredConnection")
        self.labelFavoredConnection.setText("Favored Connection")
        self.gridLayout.addWidget(self.labelFavoredConnection, 0, 0, 1, 1)
        self.labelWLANPort = QtWidgets.QLabel(self.layoutWidget2)
        self.labelWLANPort.setObjectName("labelWLANPort")
        self.labelWLANPort.setText("WLAN Port")
        self.gridLayout.addWidget(self.labelWLANPort, 4, 0, 1, 1)
        self.labelSerialPort = QtWidgets.QLabel(self.layoutWidget2)
        self.labelSerialPort.setObjectName("labelSerialPort")
        self.labelSerialPort.setText("Serial Port")
        self.gridLayout.addWidget(self.labelSerialPort, 1, 0, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(self.groupBoxGeneral)
        self.layoutWidget3.setGeometry(QtCore.QRect(260, 41, 161, 241))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEditWlanSsid = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEditWlanSsid.setObjectName("lineEditWlanSsid")
        self.lineEditWlanSsid.setText("HBX8409-XXXXXX")
        self.gridLayout_2.addWidget(self.lineEditWlanSsid, 2, 0, 1, 1)
        self.comboBoxFavoredConnection = QtWidgets.QComboBox(self.layoutWidget3)
        self.comboBoxFavoredConnection.setObjectName("comboBoxFavoredConnection")
        self.comboBoxFavoredConnection.addItem("USB")
        self.comboBoxFavoredConnection.addItem("WLAN")
        self.gridLayout_2.addWidget(self.comboBoxFavoredConnection, 0, 0, 1, 1)
        self.lineEditMountIpAddress = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEditMountIpAddress.setObjectName("lineEditMountIpAddress")
        self.lineEditMountIpAddress.setText("10.10.100.254")
        self.gridLayout_2.addWidget(self.lineEditMountIpAddress, 3, 0, 1, 1)
        self.comboBoxPollingCoordinates = QtWidgets.QComboBox(self.layoutWidget3)
        self.comboBoxPollingCoordinates.setObjectName("comboBoxPollingCoordinates")
        self.comboBoxPollingCoordinates.addItem("1 sec")
        self.comboBoxPollingCoordinates.addItem("5 sec")
        self.comboBoxPollingCoordinates.addItem("10 sec")
        self.comboBoxPollingCoordinates.addItem("30 sec")
        self.comboBoxPollingCoordinates.addItem("None")
        self.gridLayout_2.addWidget(self.comboBoxPollingCoordinates, 5, 0, 1, 1)
        self.lineEditWlanPort = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEditWlanPort.setObjectName("lineEditPort")
        self.lineEditWlanPort.setText("8899")
        self.gridLayout_2.addWidget(self.lineEditWlanPort, 4, 0, 1, 1)
        self.comboBoxPollingRefresh = QtWidgets.QComboBox(self.layoutWidget3)
        self.comboBoxPollingRefresh.setObjectName("comboBoxPollingRefresh")
        self.comboBoxPollingRefresh.addItem("1 : 1")
        self.comboBoxPollingRefresh.addItem("1 : 5")
        self.comboBoxPollingRefresh.addItem("1 : 10")
        self.comboBoxPollingRefresh.addItem("1 : 30")
        self.comboBoxPollingRefresh.addItem("None")
        self.gridLayout_2.addWidget(self.comboBoxPollingRefresh, 6, 0, 1, 1)
        self.lineEditSerialPort = QtWidgets.QLineEdit(self.layoutWidget3)
        self.lineEditSerialPort.setObjectName("lineEditSerialPort")
        self.lineEditSerialPort.setText("/dev/ttyUSB0")
        self.gridLayout_2.addWidget(self.lineEditSerialPort, 1, 0, 1, 1)
        self.pushButtonOk = QtWidgets.QPushButton(self)
        self.pushButtonOk.setGeometry(QtCore.QRect(380, 500, 100, 28))
        self.pushButtonOk.setObjectName("pushButtonOk")
        self.pushButtonOk.setText("Ok")
        self.pushButtonCancel = QtWidgets.QPushButton(self)
        self.pushButtonCancel.setGeometry(QtCore.QRect(250, 500, 100, 28))
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.pushButtonCancel.setText("Cancel")

# **************************************************************************************

        if self.configData['ConType'] == 'USB':
            self.comboBoxFavoredConnection.setCurrentIndex(0)
            self.lineEditWlanSsid.setEnabled(False)
            self.lineEditMountIpAddress.setEnabled(False)
            self.lineEditWlanPort.setEnabled(False)
            self.lineEditSerialPort.setEnabled(True)
        elif self.configData['ConType'] == 'WLAN':
            self.comboBoxFavoredConnection.setCurrentIndex(1)
            self.lineEditSerialPort.setEnabled(False)
            self.lineEditWlanSsid.setEnabled(True)
            self.lineEditMountIpAddress.setEnabled(True)
            self.lineEditWlanPort.setEnabled(True)
        self.lineEditSerialPort.selectAll()
        self.lineEditSerialPort.insert(self.configData['SerPort'])
        self.lineEditWlanSsid.selectAll()
        self.lineEditWlanSsid.insert(self.configData['WLanSSID'])
        self.lineEditMountIpAddress.selectAll()
        self.lineEditMountIpAddress.insert(self.configData['IpAddress'])
        self.lineEditWlanPort.selectAll()
        self.lineEditWlanPort.insert(self.configData['WLanPort'])

        if self.configData['PollCoord'] == '1':
            self.comboBoxPollingCoordinates.setCurrentIndex(0)
        if self.configData['PollCoord'] == '5':
            self.comboBoxPollingCoordinates.setCurrentIndex(1)
        if self.configData['PollCoord'] == '10':
            self.comboBoxPollingCoordinates.setCurrentIndex(2)
        if self.configData['PollCoord'] == '30':
            self.comboBoxPollingCoordinates.setCurrentIndex(3)
        if self.configData['PollCoord'] == 'None':
            self.comboBoxPollingCoordinates.setCurrentIndex(4)

        if self.configData['PollRefresh'] == '1:1':
            self.comboBoxPollingRefresh.setCurrentIndex(0)
        if self.configData['PollRefresh'] == '1:5':
            self.comboBoxPollingRefresh.setCurrentIndex(1)
        if self.configData['PollRefresh'] == '1:10':
            self.comboBoxPollingRefresh.setCurrentIndex(2)
        if self.configData['PollRefresh'] == '1:30':
            self.comboBoxPollingRefresh.setCurrentIndex(3)
        if self.configData['PollRefresh'] == 'None':
            self.comboBoxPollingRefresh.setCurrentIndex(4)

        if self.configData['StartSpeed'] == '1x':
            self.comboBoxStartSpeed.setCurrentIndex(0)
        elif self.configData['StartSpeed'] == '2x':
            self.comboBoxStartSpeed.setCurrentIndex(1)
        elif self.configData['StartSpeed'] == '8x':
            self.comboBoxStartSpeed.setCurrentIndex(2)
        elif self.configData['StartSpeed'] == '16x':
            self.comboBoxStartSpeed.setCurrentIndex(3)
        elif self.configData['StartSpeed'] == '64x':
            self.comboBoxStartSpeed.setCurrentIndex(4)
        elif self.configData['StartSpeed'] == '128x':
            self.comboBoxStartSpeed.setCurrentIndex(5)
        elif self.configData['StartSpeed'] == '256x':
            self.comboBoxStartSpeed.setCurrentIndex(6)
        elif self.configData['StartSpeed'] == '512x':
            self.comboBoxStartSpeed.setCurrentIndex(7)
        elif self.configData['StartSpeed'] == 'Max':
            self.comboBoxStartSpeed.setCurrentIndex(8)

        if self.configData['TrackAtStart'] == 'on':
            self.comboBoxTrackingAtStart.setCurrentIndex(0)
        if self.configData['TrackAtStart'] == 'off':
            self.comboBoxTrackingAtStart.setCurrentIndex(1)


# **************************************************************************************

        self.comboBoxFavoredConnection.currentIndexChanged.connect(self.favoredConnectionChanged)
        self.comboBoxPollingCoordinates.currentIndexChanged.connect(self.pollingRateCoordinatesChanged)
        self.comboBoxPollingRefresh.currentIndexChanged.connect(self.pollingRateRefreshChanged)
        self.comboBoxStartSpeed.currentIndexChanged.connect(self.startSpeedChanged)
        self.comboBoxTrackingAtStart.currentIndexChanged.connect(self.trackingAtStartChanged)

        self.pushButtonOk.clicked.connect(self.buttonOkClicked)
        self.pushButtonCancel.clicked.connect(self.buttonCancelClicked)

# **************************************************************************************

    def favoredConnectionChanged(self):
        self.connChanged = True
        if self.comboBoxFavoredConnection.currentIndex() == 0:
            self.comboBoxFavoredConnection.setCurrentIndex(0)
            self.lineEditWlanSsid.setEnabled(False)
            self.lineEditMountIpAddress.setEnabled(False)
            self.lineEditWlanPort.setEnabled(False)
            self.lineEditSerialPort.setEnabled(True)
            self.configData['ConType'] = 'USB'
        elif self.comboBoxFavoredConnection.currentIndex() == 1:
            self.comboBoxFavoredConnection.setCurrentIndex(1)
            self.lineEditSerialPort.setEnabled(False)
            self.lineEditWlanSsid.setEnabled(True)
            self.lineEditMountIpAddress.setEnabled(True)
            self.lineEditWlanPort.setEnabled(True)
            self.configData['ConType'] = 'WLAN'

    def pollingRateCoordinatesChanged(self):
        if self.comboBoxPollingCoordinates.currentIndex() == 0:
            self.configData['PollCoord'] = '1'
            self.comboBoxPollingRefresh.setEnabled(True)
        if self.comboBoxPollingCoordinates.currentIndex() == 1:
            self.configData['PollCoord'] = '5'
            self.comboBoxPollingRefresh.setEnabled(True)
        if self.comboBoxPollingCoordinates.currentIndex() == 2:
            self.configData['PollCoord'] = '10'
            self.comboBoxPollingRefresh.setEnabled(True)
        if self.comboBoxPollingCoordinates.currentIndex() == 3:
            self.configData['PollCoord'] = '30'
            self.comboBoxPollingRefresh.setEnabled(True)
        if self.comboBoxPollingCoordinates.currentIndex() == 4:
            self.configData['PollCoord'] = 'None'
            self.comboBoxPollingRefresh.setEnabled(False)

    def pollingRateRefreshChanged(self):
        if self.comboBoxPollingRefresh.currentIndex() == 0:
            self.configData['PollRefresh'] = '1:1'
        if self.comboBoxPollingRefresh.currentIndex() == 1:
            self.configData['PollRefresh'] = '1:5'
        if self.comboBoxPollingRefresh.currentIndex() == 2:
            self.configData['PollRefresh'] = '1:10'
        if self.comboBoxPollingRefresh.currentIndex() == 3:
            self.configData['PollRefresh'] = '1:30'
        if self.comboBoxPollingRefresh.currentIndex() == 4:
            self.configData['PollRefresh'] == 'None'

    def startSpeedChanged(self):
        if self.comboBoxStartSpeed.currentIndex() == 0:
            self.configData['StartSpeed'] = '1x'
        if self.comboBoxStartSpeed.currentIndex() == 1:
            self.configData['StartSpeed'] = '2x'
        if self.comboBoxStartSpeed.currentIndex() == 2:
            self.configData['StartSpeed'] = '8x'
        if self.comboBoxStartSpeed.currentIndex() == 3:
            self.configData['StartSpeed'] = '16x'
        if self.comboBoxStartSpeed.currentIndex() == 4:
            self.configData['StartSpeed'] = '64x'
        if self.comboBoxStartSpeed.currentIndex() == 5:
            self.configData['StartSpeed'] = '128x'
        if self.comboBoxStartSpeed.currentIndex() == 6:
            self.configData['StartSpeed'] = '256x'
        if self.comboBoxStartSpeed.currentIndex() == 7:
            self.configData['StartSpeed'] = '512x'
        if self.comboBoxStartSpeed.currentIndex() == 8:
            self.configData['StartSpeed'] = 'Max'
#        print(self.configData['StartSpeed'])

    def trackingAtStartChanged(self):
        if self.comboBoxTrackingAtStart.currentIndex() == 0:
            self.configData['TrackAtStart'] = 'on'
        if self.comboBoxTrackingAtStart.currentIndex() == 1:
            self.configData['TrackAtStart'] = 'off'
#        print(self.configData['TrackAtStart'])

    def buttonOkClicked(self):
        utilities.writeConfig(self.configData)
        self.close()

    def buttonCancelClicked(self):
        self.close()


#************************************************************************************
class LogFileRead(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'liomoco - logfile.log'
        self.left = 10
        self.top = 20
        self.width = 800
        self.height = 600
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QTextEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(760,560)
        
        logfile = open('logfile.log', 'r')
        logText = ''
        for zeile in logfile:
            print(zeile)
            logText = logText + zeile
        self.textbox.setText(logText)
        print(logText)
        logfile.close

        self.show()