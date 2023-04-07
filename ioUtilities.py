"""
Module for interfacing and communicating with stuff over serial and wlan.
original modul from: @author - James Malone

rewritten and adapted: @author - Wolfgang Rafelt, 2023
"""


# Imports
import sys
import time
import serial
import socket
import logging
import iOptronGUI


class IoConnectionUSB:
    """Class for communicating with devices over serial."""
    def __init__(self, port = '/dev/ttyUSB0', baud = 115200):
        self.sendWait = 0.10         # Arbritrary waiting period to save flooding comms
        self.mountIsConnected = False
        try:
            self.ser = serial.Serial(port, baud)
            self.mountIsConnected = True
            logging.debug('USB serial port ' + port + 'connected')
        except serial.SerialException:
            logging.error('serial connection failed')
            self.mountIsConnected = False
            sys.exit(1)

    def isOpen(self):
        """Open the serial connection."""
        if self.ser.isOpen():
            return True
        else:
            logging.info('USB serial port ' + port + ' is not open')
            return False

    def send(self, data):
        """Send data over the serial connection."""
        bytesToSend = data.encode('utf-8')
        try:
            self.ser.write(bytesToSend)
            time.sleep(self.sendWait)
        except:
            logging.error('USB sending serial --> %s' + data)


    def recv(self):
        """Receive the output."""
        output = ''
        try:
            while self.ser.inWaiting() > 0:
                output += self.ser.read(1).decode('utf-8')
        except:
            logging.error('USB received serial <-- %s' + str(output))
        return output

    def close(self):
        """Close the connection."""
        self.ser.close()
        self.mountIsConnected = False
        logging.info('Closed serial port successfully')


class IoConnectionWlan:
    """Class for communicating with devices over serial."""
    def __init__(self, ipAddress = '10.10.100.254', port = '8899'):
        self.sendWait = 0.10
        self.mountIsConnected = False
        self.wlan = socket.socket()
        self.wlan.settimeout(5)
        self.address = (ipAddress, int(port))
        self.mountIsConnected = True
        try:
            self.wlan.connect(self.address)
            self.mountIsConnected = True
        except OSError as errorText:
            logging.error('WLAN connection failed')
            # MessageBox output
            self.mountIsConnected = False
            sys.exit(1)
        except:
            e = sys.exc_info()[0]
            logging.error('WLAN connection failed')
            # MessageBox output
            self.mountIsConnected = False
            sys.exit(1)
        else:
            logging.debug('WLAN is connected %s' + str(ipAddress) + ':' + str(port))

    def isConnected(self):
        """Open the serial connection."""
        if self.wlan.connect_ex(self.address) == 0:
            return True
        else:
            logging.error('WLAN ' + (ipAddress, port) + ' is not open')
            return False

    def send(self, data):
        """Send data over the WLAN connection."""
        bytesToSend = data.encode('utf-8')
        try:
            self.wlan.send(bytesToSend)
        except Exception as e:
            logging.error('WLAN sending serial -> %s ' + str(data) + (ipAddress, port) + ' failed')
            return False
        time.sleep(self.sendWait)
        return True

    def recv(self):
        """Receive the output from WLAN."""
        output = ''
        try:
            output = self.wlan.recv(30).decode('utf-8')
        except:
            logging.info('WLAN Received <- %s' + str(output) + (ipAddress, port) + ' failed')
        return output

    def close(self):
        """Close the WLAN connection."""
        self.wlan.close()
        self.mountIsConnected = False
        logging.debug('Closed WLAN connection successfully')
