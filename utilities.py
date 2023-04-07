"""
This is a utility module to do common methods, conversions, etc.
@author - James Malone

rewritten and adapted: @author - Wolfgang Rafelt, 2023
"""

# Imports
import time
import configparser
from datetime import datetime, timedelta
from decimal import Decimal


def convertArcSecondsToDegrees(seconds):
    """Convert arc seconds with 0.01 percision to degrees"""
    return (seconds / 3600) * 0.01

def convertArcSecondsToDms(seconds):
    """Convert arc seconds to degrees, minutes, seconds. Returns
    a touple with the integer dms values."""
    degrees = convertArcSecondsToDegrees(seconds)
    degree = int(degrees)
    minute = int((degrees - degree) * 60)
    second = float((degrees - degree - minute/60) * 3600)
    return (degree, abs(minute), abs(second))

def convertArcSecondsToHms(seconds):
    """Converts arc seconds at 0.01 precision to arc HH:MM:SS"""
    hours = float(seconds) / (15.0 * 60.0 * 60.0 * 100.0) #Thank you INDI.
    minutes = (Decimal(hours) % 1) * 60
    seconds = (Decimal(minutes) % 1) * 60
    return (int(hours), int(minutes), float(seconds))

def convertDegreesToArcSeconds(seconds):
    """Convert degrees into arcseconds."""
    return (seconds * 3600) / 0.01 # The value is 0.01 arc seconds

def convertDmsToArcSeconds(degrees: int, minutes: int, seconds: float):
    """Convert degrees, minutes, and seconds to arcseconds. Returns an integer in
    arcseconds."""
    decimalValue = convertDmsToDegrees(degrees, minutes, seconds)
    arcseconds = convertDegreesToArcSeconds(decimalValue)
    return int(arcseconds)

def convertDmsToDegrees(degrees: int, minutes: int, seconds: float):
    """Convert a DMS value to decimal degrees. Will round to 5 decimal places
    if it is needed."""
    return round(degrees + (minutes / 60) + (seconds / 3600), 5)

def convertDegreesToDms(degrees: float):
    """Convert a Degree value to DMS degrees. Will round to 5 decimal places
    if it is needed."""
    mnt, sec = divmod(abs(degrees)*3600, 60)
    deg, mnt = divmod(mnt, 60)
    if degrees < 0:
        deg = -deg
    deg, mnt = int(deg), int(mnt)
    return (deg, mnt, sec)

def convertJ2kToUnixUtc(sec, offset = 0):
    """Convert J2000 in 0.01 seconds to formatted UNIX in ms with offset if needed."""
    converted = datetime(2000,1,1,12,0) + timedelta(milliseconds=sec) + timedelta(minutes=offset)
    return time.mktime(converted.timetuple())

def convertUnixToFormatted(unixMs):
    """Convert a unix timestamp to HH:MM:SS.ss."""
    return datetime.utcfromtimestamp(int(unixMs)).strftime("%d.%m.%Y, %H:%M:%S")

def getUtcOffsetMin():
    """Get the UTC offset of this computer in minutes."""
    offset = int(time.timezone/60)
    return offset * -1

def getUtcTimeInJ2k():
    """Get the UTC time expressed in J2000 format (seconds since 12 on 1/1/2000.)"""
    j2kTime = datetime(2000, 1, 1, 12, 00)
    utc = datetime.utcnow()
    difference = utc - j2kTime
    return(int(difference.total_seconds() * 1000))

def offsetUtcTime(unix, offset):
    """Convert utc time into a time with the supplied timezone offset."""
    offsetSec = timedelta(minutes=abs(int(offset))).seconds
    if offset < 1:
        return unix - offsetSec
    if offset > 0:
        return unix + offsetSec
    if offset == 0:
        return unix + 0 # No changes

def checkDateFormat(strDate):
    check = True
    # initializing format
    format = "%d.%m.%Y"
    try:
        check = bool(datetime.strptime(strDate, format))
    except ValueError:
        check = False
    if int(strDate[6:10]) < 2020 or int(strDate[6:10]) > 2050:
        check = False
    return check


def checkTimeFormat(strTime):
    check = True
    # initializing format
    format = "%H:%M:%S"
    try:
        check = bool(datetime.strptime(strTime, format))
    except ValueError:
        check = False
    return check

def checkValidFormat(datString,formatString):
    '''Funktion checks the valid stringformat.
        format:
        v = sign
        z = figure 0..9
        d = degree
        h = hour
        m = m or ' = minute
        s = s or " = second
        p = . or : in date or time
        n = N or S
        w = W or E
        # = hashtag
        '''

    result = True
    try:
        for i in range(0,len(formatString)-1):
            if formatString[i] == 'v':
                if datString[i] == '+' or datString[i] == '-':
                    result = True
                else:
                    result = False
            elif formatString[i] == 'z':
                if not (datString[i].isdigit):
                    result = False
            elif formatString[i] == 'd':
                if datString[i] != '°':
                    result = False
            elif formatString[i] == 'h':
                if datString[i] != 'h':
                    result = False
            elif formatString[i] == 'm':
                if not(datString[i] == 'm' or datString[i] == '\''):
                    result = False
            elif formatString[i] == 's':
                if not(datString[i] == 's' or datString[i] == '\"' or datString[i] == '\'\''):
                    result = False
            elif formatString[i] == 'p':
                if not(datString[i] == '.' or datString[i] == ':'):
                    result = False
            elif formatString[i] == 'n':
                if not(datString[i] == 'N' or datString[i] == 'S'):
                    result = False
            elif formatString[i] == 'w':
                if not(datString[i] == 'W' or datString[i] == 'E'):
                    result = False
            elif formatString[i] == '#':
                if datString[i] != '#':
                    result = False
    except IndexError:
        pass
        # Fehler protokollieren
    return result

def readConfig():
    """Function to read the config file. Retruns a data structure
       of config information."""
    config= configparser.ConfigParser()
    config.read('setup.ini')
    configData = {}
    configData['MountMod'] = config['DEFAULT']['MountModel']
    configData['ConType'] = config['DEFAULT']['TypeConnection']
    configData['SuppModels'] = config['DEFAULT']['SupportedModels']
    configData['SuppModels'] = configData['SuppModels'].replace(" ",'')
    configData['SuppModels'] = configData['SuppModels'].replace('"','')
    configData['SuppModels'] = configData['SuppModels'].split(",")
    configData['SuppModels'] = tuple(configData['SuppModels'])
    configData['SerPort'] = config['USB']['SerialPort']
    configData['SerSpeed'] = config['USB']['SerialSpeed']
    configData['WLanSSID'] = config['WLAN']['WLanSSID']
    configData['IpAddress'] = config['WLAN']['IpAddress']
    configData['WLanPort'] = config['WLAN']['WLanPort']
    configData['PollCoord'] = config['STARTUP']['PollCoordinates']
    configData['PollRefresh'] = config['STARTUP']['PollRefresh']
    configData['StartSpeed'] = config['STARTUP']['StartSpeed']
    configData['TrackAtStart'] = config['STARTUP']['TrackAtStart']
    configData['Sidereal'] = config['TRACKINGRATES']['Sidereal']
    configData['Lunar'] = config['TRACKINGRATES']['Lunar']
    configData['Solar'] = config['TRACKINGRATES']['Solar']
    configData['King'] = config['TRACKINGRATES']['King']
    configData['Custom'] = config['TRACKINGRATES']['Custom']

    configData['Encoders'] = config['CAPABILITIES']['Encoders']
    configData['Pec'] = config['CAPABILITIES']['Pec']
    configData['MechanicalZero'] = config['CAPABILITIES']['MechanicalZero']
    configData['MountType'] = config['CAPABILITIES']['Type']
    return configData

def writeConfig(configData):
    config= configparser.ConfigParser()

    config['DEFAULT']['MountModel'] = configData.get('MountMod')
    config['DEFAULT']['TypeConnection'] = configData.get('ConType')
    value = str(configData.get('SuppModels'))
    config['DEFAULT']['SupportedModels'] = value[1:len(value)-1]
    config.add_section('USB')
    config['USB']['SerialPort'] = configData.get('SerPort')
    config['USB']['SerialSpeed'] = configData.get('SerSpeed')
    config.add_section('WLAN')
    config.set('WLAN','WLanSSID',configData.get('WLanSSID'))
    config.set('WLAN','IpAddress',configData.get('IpAddress'))
    config.set('WLAN','WLanPort',configData.get('WLanPort'))
    config.add_section('STARTUP')
    config['STARTUP']['PollCoordinates'] = configData.get('PollCoord')
    config['STARTUP']['PollRefresh'] = configData.get('PollRefresh')
    config['STARTUP']['StartSpeed'] = configData.get('StartSpeed')
    config['STARTUP']['TrackAtStart'] = configData.get('TrackAtStart')
    config.add_section('TRACKINGRATES')
    config['TRACKINGRATES']['Sidereal'] = configData.get('Sidereal')
    config['TRACKINGRATES']['Lunar'] = configData.get('Lunar')
    config['TRACKINGRATES']['Solar'] = configData.get('Solar')
    config['TRACKINGRATES']['King'] = configData.get('King')
    config['TRACKINGRATES']['Custom'] = configData.get('Custom')
    config.add_section('CAPABILITIES')
    config['CAPABILITIES']['Encoders'] = configData.get('Encoders')
    config['CAPABILITIES']['Pec'] = configData.get('Pec')
    config['CAPABILITIES']['MechanicalZero'] = configData.get('MechanicalZero')
    config['CAPABILITIES']['Type'] = configData.get('MountType')

    with open('setup.ini', 'w') as configfile:
        config.write(configfile)
