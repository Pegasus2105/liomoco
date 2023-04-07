"""
iOptron telescope Python interface
This is intended to understand how the mount works
If I am going to trash their software (it IS crap) I need to understand it
James Malone, 2021

rewritten and adapted: @author - Wolfgang Rafelt, 2023
"""


# Imports
import time
import logging
import configparser
from   dataclasses       import dataclass
from   serial.serialutil import SerialException
from   datetime          import datetime
from   dialoges          import PopupDialog
import iOptronGUI
import utilities
import ioUtilities


# Data classes
@dataclass
class Mount:
    """Some mount current status options."""
    connectionStatus: str = 'offline'
    isInMotion: bool = False
    isInIoProzess: bool = False

@dataclass
class Altitude:
    """An altitude position. Contains the arcseconds and DMS."""
    arcseconds: float = None
    degrees: float = None
    minutes: int = None
    seconds: float = None
    limit: str = None

@dataclass
class Azimuth:
    """An azimuth position. Contains the arcseconds and DMS."""
    arcseconds: float = None
    degrees: float = None
    minutes: int = None
    seconds: float = None

@dataclass
class RA:
    """Right ascension (RA) data."""
    arcseconds: float = None
    hours: int = None
    minutes: int = None
    seconds: float = None
    degrees: float = None

@dataclass
class DEC:
    """Information about a declination value."""
    arcseconds: float = None
    degrees: int = None
    minutes: int = None
    seconds: float = None

@dataclass
class Firmwares:
    """Information on the firmware istalled on the mount and components."""
    mainboard: str = None
    handController: str = None
    rightAscention: str = None
    declination: str = None

@dataclass
class Location:
    """Holds location information along with GPS data."""
    gpsAvailable: bool = False
    gpsLocked: bool = False
    longitude: float = None
    latitude: float = None

@dataclass
class Guiding:
    """Informationa bout the RA and dec guiding rate. Can be 0.01 - 0.99.
    Represents the rate * siderial rate."""
    rightAscentionRate: float = None
    declinationRate: float = None
    raFilterEnabled: bool = None
    hasRaFilter: bool = False

@dataclass
class SystemStatus:
    """System status information."""
    code: int = None
    description: str = None

@dataclass
class Tracking:
    """Holds tracking and rate information for the mount."""
    code: int = None
    custom: float = 1.0000
    availableRates: dict = None
    isTracking: bool = False
    memoryStore: int = None

    def currentRate(self):
        """Return a string description of the current rate."""
        if self.isTracking is False:
            return "not tracking"
        if self.code is not None:
            return self.availableRates[self.code]
        # Not set, return none
        return None

@dataclass
class meridian:
    """Holds meridian-related information."""
    code: str = None
    degreeLimit: str = None

    def description(self):
        """Get the text description of the meridian treatment."""
        if self.code == 0:
            return "Stop at meridian"
        if self.code == 1:
            return "Flip at meridian with custom limit"
        else:
            return "Unknown or not set."

@dataclass
class MovingSpeed:
    """Information about the moving speed of the mount."""
    code: int = None
#    multiplier: int = None
    description: str = None
#    buttonRate: int = None
#    availableRates: dict = None

@dataclass
class Parking:
    """Contains information and location of parking."""
    isParked: bool = None
    altitude: Altitude = Altitude()
    azimuth: Azimuth = Azimuth()

@dataclass
class Pec:
    """Holds information related to the periodic error correction (PEC.)"""
    integrityComplete: bool = None
    enabled: bool = None
    recording: bool = None

@dataclass
class TimeSource:
    """Keeps track of the source of time. May be removed in the future."""
    code: int = None
    description: str = "unset"

@dataclass
class TimeInfo:
    """Time related information."""
    utcOffset: int = None
    summerTime: int = None
    dst: bool = None
    julianDate: int = None
    unixUtc: float = None
    unixOffset: float = None
    formatted: str = None

@dataclass
class Hemisphere:
    """Holds information about the hemisphere of the mount."""
    code: int = None
    location: str = None

class Ioptron:
    """A class to interact with iOptron mounts using Python."""
    def __init__(self):
        self.myMount = Mount()
        self.config = utilities.readConfig()

        if self.config['ConType'] == 'USB':
            if self.config['SerPort'] != '' and self.config['SerPort'] != 'WLAN':
                self.scope = ioUtilities.IoConnectionUSB(self.config['SerPort'],self.config['SerSpeed'])
                if self.scope.isOpen():
                    info = PopupDialog('INFO: USB', 'Mount is USB serial connected.', 10, 'gray')
                    info.exec()
                    self.myMount.connectionStatus = 'online'
                    self.mountConnectionType = self.config['ConType']
                else:
                    print('Serial Problem')
            else:
                raise SerialException
        elif self.config['ConType'] == 'WLAN':
            if self.config['WLanPort'] != '' and self.config['IpAddress'] != '':
                self.scope = ioUtilities.IoConnectionWlan(self.config['IpAddress'], self.config['WLanPort'])
                self.myMount.connectionStatus = 'online'
                self.mountConnectionType = self.config['ConType']
                info = PopupDialog('INFO: WLAN', 'Mount is WLAN connected.', 10, 'gray')
                info.exec()

        self.movingSpeed = MovingSpeed()
        self.movingSpeed.description = self.config['StartSpeed']
        if self.config['StartSpeed'] == '1x':
            self.movingSpeed.code = 1
        elif self.config['StartSpeed'] == '2x':
            self.movingSpeed.code = 2
        elif self.config['StartSpeed'] == '8x':
            self.movingSpeed.code = 3
        elif self.config['StartSpeed'] == '16x':
            self.movingSpeed.code = 4
        elif self.config['StartSpeed'] == '64x':
            self.movingSpeed.code = 5
        elif self.config['StartSpeed'] == '128x':
            self.movingSpeed.code = 6
        elif self.config['StartSpeed'] == '256x':
            self.movingSpeed.code = 7
        elif self.config['StartSpeed'] == '512x':
            self.movingSpeed.code = 8
        elif self.config['StartSpeed'] == 'Max':
            self.movingSpeed.code = 9
        self.setMovingSpeed(self.movingSpeed.code)

        # Assign default values
        self.location = Location()
        mainFwInfo = self.getMainFirmwares()
        motorFwInfo = self.getMotorFirmwares()
        self.mountVersion = self.getMountVersion()
        self.firmware = Firmwares(mainboard=mainFwInfo[0], handController=mainFwInfo[1], \
            rightAscention=motorFwInfo[0], declination=motorFwInfo[1])
        self.handControllerAttached = False if 'xx' in self.firmware.handController else True
        self.systemStatus = SystemStatus()
        self.tracking = Tracking()
        self.timeSource = TimeSource()
        self.hemisphere = Hemisphere()
        self.guiding = Guiding()
        self.isSlewing = False
        self.isHome = None
        self.pec = Pec()

        # Time information
        self.time = TimeInfo()

        # Direction information
        self.rightAscension = RA()
        self.declination = DEC()
        self.pierSide = None
        self.counterweightDirection = None
        self.altitude = Altitude()
        self.azimuth = Azimuth()
        self.meridian = meridian()

        # Parking
        self.parking = Parking()

        # Set the update time to null
        self.lastUpdate = 0

    # Destructor that gets called when the object is destroyed
    def __del__(self):
        try:
            self.scope.close()
        except:
            print("CLEANUP: not needed or was unclean")


    def enablePecPlayback(self, enabled: bool):
        """Enable or disable PEC playback, toggled by the supplied boolean.
        Setting to True enables PEC playback, setting to False disables playback.
        Only available on eq mountd without encoders. Returns True when command sent
        and response is received, otherwise returns False."""
        if self.config['MountType'] != "equatorial" or \
            self.config['Encoders'] is True:
            return False
        self.myMount.isInIoProzess = True
        if enabled is True:
            self.scope.send(":SPP1#")
        if enabled is False:
            self.scope.send(":SPP0#")
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    # To get the joke here, read the official protocol docs
    def getAllKindsOfStatus(self):
        """Get (a lot) of status from the mount. Get location, GPS state, status, movement
        and tracking information, and time data."""
        self.myMount.isInIoProzess = True
        self.scope.send(":GLS#")
        responseData = self.scope.recv()
        if not utilities.checkValidFormat(responseData, 'vzzzzzzzzzzzzzzzzzzzzzz#'):
            return

        # Parse latitude and longitude
        self.location.longitude = utilities.convertArcSecondsToDegrees(int(responseData[0:9]))
        self.location.latitude = utilities.convertArcSecondsToDegrees(\
            int(responseData[9:17])) - 90 # Val is +90

        # Parse GPS state
        gpsState = responseData[17:18]
        if gpsState == '0':
            self.location.gpsAvailable = False
        elif gpsState == '1':
            self.location.gpsAvailable = True
            self.location.gpsLocked = False
        elif gpsState == '2':
            self.location.gpsAvailable = True
            self.location.gpsLocked = True

        # Parse the system status
        statusCode = responseData[18:19]
        self.systemStatus.code = statusCode
        if statusCode == '0':
            self.systemStatus.description = "stopped at non-zero position"
            self.isSlewing = False
            self.tracking.isTracking = False
        elif statusCode == '1':
            self.systemStatus.description = "tracking with periodic error correction disabled"
            self.isSlewing = False
            self.tracking.isTracking = True
            self.pec.enabled = False
        elif statusCode == '2':
            self.systemStatus.description = "slewing"
            self.isSlewing = True
            self.tracking.isTracking = False
        elif statusCode == '3':
            self.systemStatus.description = "auto-guiding"
            self.isSlewing = False
            self.tracking.isTracking = True
        elif statusCode == '4':
            self.systemStatus.description = "meridian flipping"
            self.isSlewing = True
        elif statusCode == '5':
            self.systemStatus.description = "tracking with periodic error correction enabled"
            self.isSlewing = False
            self.tracking.isTracking = True
            self.pec.enabled = True
        elif statusCode == '6':
            self.systemStatus.description = "parked"
            self.isSlewing = False
            self.tracking.isTracking = False
            self.parking.isParked = True
        elif statusCode == '7':
            self.systemStatus.description = "stopped at zero position (home position)"
            self.isSlewing = False
            self.tracking.isTracking = False

        # Parse tracking rate
        trackingRate = responseData[19:20]
        self.tracking.code = trackingRate

        # Parse moving speed
        movingSpeed = responseData[20:21]
        self.movingSpeed.code = movingSpeed

        # Parse the time source
        timeSource = responseData[21:22]
        self.timeSource.code = timeSource
        if timeSource == '1':
            self.timeSource.description = "local - RS232 or ethernet"
        elif timeSource == '2':
            self.timeSource.description = "hand controller"
        elif timeSource == '3':
            self.timeSource.description = "GPS"

        # Parse the hemisphere
        hemisphere = responseData[22:23]
        self.hemisphere.code = hemisphere
        if hemisphere == '0':
            self.hemisphere.location = 'south'
        if hemisphere == '1':
            self.hemisphere.location = 'north'
        self.myMount.isInIoProzess = False

    def getAltAndAz(self):
        """Get the altitude and azimuth of the mount's current direction."""
        self.myMount.isInIoProzess = True
        self.scope.send(':GAC#')
        returnedData = self.scope.recv()
        if not utilities.checkValidFormat(returnedData, 'vzzzzzzzzzzzzzzzzz#'):
            return

        # Altitude
        altitude = returnedData[0:9]
        try:
            float(altitude)
        except ValueError:
            pass
        else:
            self.altitude.arcseconds = float(altitude)
            self.setDataclassDmsFromArcseconds(self.altitude)

        # Azimuth
        azimuth = returnedData[9:18]
        try:
            float(azimuth)
        except ValueError:
            pass
        else:
            self.azimuth.arcseconds = float(azimuth)
            self.setDataclassDmsFromArcseconds(self.azimuth)
            self.myMount.isInIoProzess = False

    def getAltitudeLimit(self):
        """Get the altitude limt currently set. Applies to tracking and slewing. Motion will
        stop if it exceeds this value."""
        self.myMount.isInIoProzess = True
        self.scope.send(':GAL#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        self.altitude.limit = returnedData[0:3]
        return self.altitude.limit

    def getCoordinateMemory(self):
        """Get the number of positions available to store RC and DEC positions that
        do not exceed limits (altitude, mechanical, and flip.) Will return an int
        between 0 and 2. Only returns a value on eq mounts, otherwise None."""
        self.myMount.isInIoProzess = True
        self.scope.send(':QAP#')
        self.tracking.memoryStore = self.scope.recv()[0:1]
        self.myMount.isInIoProzess = False
        return self.tracking.memoryStore

    def getCustomTrackingRate(self):
        """Get the custom tracking rate, if it is set. Otherwise will be 1.000."""
        self.myMount.isInIoProzess = True
        self.scope.send(':GTR#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        # Set the value and strip the control '#' at the end (response is d{5})
        self.tracking.custom = format((float(returnedData[:5]) * 0.0001), '.4f')

    def getGuidingRate(self):
        """Get the current RA and DEC guiding rates. They are 0.01 - 0.99 * siderial."""
        self.myMount.isInIoProzess = True
        self.scope.send(':AG#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        # Convert values to 0.01 - 0.9
        self.guiding.rightAscentionRate = float(returnedData[0:2]) * 0.01
        self.guiding.declinationRate = float(returnedData[2:4])*  0.01

    def getPecIntegrity(self):
        """Get the integrity of the PEC. Returns (and sets) if it is complete or incomplete.
        Only available with eq mounts without encoders"""
        if self.config['MountType'] != "equatorial" or \
            self.config['Encoders'] is True:
            return
        # Continue - is an EQ mount without encoders
        self.myMount.isInIoProzess = True
        self.scope.send(':GPE#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        if returnedData == "0":
            self.pec.integrityComplete = False
        if returnedData == "1":
            self.pec.integrityComplete = True

    def getPecRecordingStatus(self):
        """Get the status of the PEC recording. Returns (and sets) if it is stopped or recording.
        Only available with eq mounts without encoders"""
        if self.config['MountType'] != "equatorial" or \
            self.config['Encoders'] is True:
            return
        # Continue - is an EQ mount without encoders
        self.myMount.isInIoProzess = True
        self.scope.send(':GPR#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        if returnedData == "0":
            self.pec.recording = False
        if returnedData == "1":
            self.pec.recording = True

    def getMaxSlewingSpeed(self):
        """Get the maximum slewing speed for this mount and returns a factor of siderial (eg 8x)."""
        self.myMount.isInIoProzess = True
        self.scope.send(':GSR#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False

        # Response depends on mount model
        if returnedData == "7#":
            return 256
        if returnedData == "8#":
            return 512
        if returnedData == "9#":
            return self.config['trackingSpeeds'][9]

    def getmeridianTreatment(self):
        """Get the treatment of the meridian - stop below limit or flip at limit along
        with the position limit in degrees past meridian. Only used for equitorial mounts."""
        # This works for eq mounts only
        if self.config['MountType'] != 'equatorial':
            return
        # This is an eq mount
        self.myMount.isInIoProzess = True
        self.scope.send(':GMT#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        code = returnedData[0:1]
        degrees = returnedData[1:3]
        self.meridian.code = int(code)
        self.meridian.degreeLimit = int(degrees)

    def getMainFirmwares(self):
        """Get the firmware(s) of the mount and hand controller, if it is attached, otherwise
        a null value (xxxxxx) is used for the HC firmware."""
        self.myMount.isInIoProzess = True
        self.scope.send(':FW1#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        mainFw = returnedData[0:6]
        hcFw = returnedData[6:12]
        return (mainFw, hcFw)

    def getMotorFirmwares(self):
        """Get the firmware of the motors (ra and dec)."""
        self.myMount.isInIoProzess = True
        self.scope.send(':FW2#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        rightAsc = returnedData[0:6]
        dec = returnedData[6:12]
        return (rightAsc, dec)

    def getMountVersion(self):
        """Get the model / version of the mount. Returns the model number."""
        self.myMount.isInIoProzess = True
        self.scope.send(':MountInfo#')
        mountVer = self.scope.recv()
        self.myMount.isInIoProzess = False
        return mountVer

    def getParkingPosition(self):
        """Get the current parking position of the mount. """
        self.myMount.isInIoProzess = True
        self.scope.send(':GPC#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False

        # Altitude
        altitude = returnedData[0:8]
        self.parking.altitude.arcseconds = float(altitude)
        self.setDataclassDmsFromArcseconds(self.parking.altitude)

        # Azimuth
        azimuth = returnedData[8:17]
        self.parking.azimuth.arcseconds = float(azimuth)
        self.setDataclassDmsFromArcseconds(self.parking.azimuth)

    def getRaAndDec(self):
        """Get the RA and DEC of the telescope's current pointing position."""
        self.myMount.isInIoProzess = True
        self.scope.send(':GEP#')
        returnedData = self.scope.recv()
        if not utilities.checkValidFormat(returnedData, 'vzzzzzzzzzzzzzzzzzzz#'):
            return
        # RA
        rightAsc = returnedData[9:18]
        try:
            float(rightAsc)
        except ValueError:
            print('Value ERROR float rightASC')
        else:
            self.rightAscension.arcseconds = float(rightAsc)
            self.rightAscension.degrees = \
                utilities.convertArcSecondsToDegrees(self.rightAscension.arcseconds)
            hms = utilities.convertArcSecondsToHms(rightAsc)
            self.rightAscension.hours = hms[0]
            self.rightAscension.minutes = hms[1]
            self.rightAscension.seconds = hms[2]

        # Declination
        declination = returnedData[0:9]
        try:
            float(declination)
        except ValueError:
            print('Value ERROR float rightASC')
        else:
            self.declination.arcseconds = float(declination)
            dms = utilities.convertArcSecondsToDms(self.declination.arcseconds)
            self.declination.degrees = dms[0]
            self.declination.minutes = dms[1]
            self.declination.seconds = dms[2]

        # The following only works for eq mounts
        result = ''
        if self.config['MountType'] == "equatorial":
            # Pier side
            pierSide = returnedData[18:19]
            if pierSide == '0':
                result = 'west'
            elif pierSide == '1':
                result = 'east'
            elif pierSide == '2':
                result = 'indeterminate'
            self.pierSide = result

            # Counterweight direction
            counterweightDirection = returnedData[19:20]
            if counterweightDirection == '0':
                result = 'up'
            if counterweightDirection == '1':
                result = 'normal'
            self.counterweightDirection = result
        self.myMount.isInIoProzess = False

    def getRaGuidingFilterStatus(self):
        """Get the status of the RA guiding filter for mounts with encoders."""
        # Only available for eq mounts with encoders
        if self.config['MountType'] != "equatorial" or \
            self.config['Encoders'] is False:
            return None
        self.myMount.isInIoProzess = True
        self.guiding.hasRaFilter = True
        self.scope.send(':GGF#')
        returnedData = self.scope.recv()
        self.myMount.isInIoProzess = False
        if returnedData == "0":
            self.guiding.raFilterEnabled = False
        if returnedData == "1":
            self.guiding.raFilterEnabled = True
        return self.guiding.raFilterEnabled

    def getTimeInformation(self):
        """Get all time information from the mount, including it's time,
        timezone, and DST setting."""
        self.myMount.isInIoProzess = True
        self.scope.send(':GUT#')
        responseData = self.scope.recv()
        if not utilities.checkValidFormat(responseData, 'vzzzzzzzzzzzzzzzzz#'):
            return
        self.myMount.isInIoProzess = False
        self.time.utcOffset = int(responseData[0:4])
        self.time.summerTime = int(responseData[0:4])
        self.time.dst = False if responseData[4:5] == '0' else True
        self.time.julianDate = int(responseData[5:18].lstrip("0"))
        self.time.unixUtc = utilities.convertJ2kToUnixUtc(self.time.julianDate, self.time.utcOffset)
        self.time.unixOffset = utilities.offsetUtcTime(self.time.unixUtc, self.time.utcOffset)
        self.time.formatted = utilities.convertUnixToFormatted(self.time.unixOffset)

    def goToZeroPosition(self):
        """Go to the mount's zero position."""
        self.myMount.isInIoProzess = True
        self.scope.send(':MH#')
        self.isSlewing = True
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False

    def goToMechanicalZeroPosition(self):
        """Search and go to the *mechanical* zero position.
        Only supported by some mounts."""
        ## TODO: This is a good place to log a WARN
        # ['0040', '0041', '0043', '0044', '0070', '0071','0120', '0121', '0122']
        self.myMount.isInIoProzess = True
        if self.config['mechanicalZero'] is True:
            self.scope.send(':MSH#')
            self.isSlewing = True
            # Get the response; do nothing with it
            self.scope.recv()
        self.myMount.isInIoProzess = False
        # Maybe worth throwing an exception

    def moveDecNegative(self, seconds: int = 0):
        """Move the mount in the DEC- position at the current tracking rate for
        the given number of seconds (0-99999), with zero seconds being the
        default. Will return True once command is sent."""
        return self.moveInDirectionForNSeconds('dec-', seconds)

    def moveDecPositive(self, seconds: int = 0):
        """Move the mount in the DEC+ position at the current tracking rate for
        the given number of seconds (0-99999), with zero seconds being the
        default. Will return True once command is sent."""
        return self.moveInDirectionForNSeconds('dec+', seconds)

    def moveEast(self):
        """Commands the mount to move to the east. Mount will continue moving
        until a stop command (stopAllMovement or stopNSMovement") is issued.
        This command is similar to the up "right" button on the hand controller.
        Returns True when command is sent and response received, otherwise will
        return False."""
        return self.moveInCardinalDirection('east')

    def moveInCardinalDirection(self, direction: str):
        """PRIVATE method to move the mount in the supplied cardinal direction.
        Returns True when command is sent and response received, otherwise will
        return False."""
        self.myMount.isInIoProzess = True
        directions = {'north': "mn", 'east': 'me', 'south': 'ms', 'west': 'mw'}
        assert direction.lower() in directions
        moveCommand = ":" + directions[direction.lower()] + "#"
        self.scope.send(moveCommand)
        self.myMount.isInIoProzess = False
        return True

    def moveInDirectionForNSeconds(self, direction: str, seconds: int):
        """PRIVATE method to move in a direction (RA, DEC +/-) for a given number
        of seconds. This method is to be used by methods that implement movement in
        a specific direction. Given direction must be in [ra+, ra-, dec+, dec-].
        Returns True once command is sent."""
        # Validate the arguments
        self.myMount.isInIoProzess = True
        directions = {'ra+': "ZS", 'ra-': 'ZQ', 'dec+': 'ZE', 'dec-': 'ZC'}
        assert direction.lower() in directions
        assert 0 <= seconds <= 99999
        # Form and send the move command
        moveCommand = ":" + directions[direction.lower()] + seconds + "#"
        self.scope.send(moveCommand)
#        self.scope.recv() # No output is returned
        self.myMount.isInIoProzess = False
        return True

    def moveRaNegative(self, seconds: int = 0):
        """Move the mount in the RA- position at the current tracking rate for
        the given number of seconds (0-99999), with zero seconds being the
        default. Will return True once command is sent."""
        return self.moveInDirectionForNSeconds('ra-', seconds)

    def moveRaPositive(self, seconds: int = 0):
        """Move the mount in the RA+ position at the current tracking rate for
        the given number of seconds (0-99999), with zero seconds being the
        default. Will return True once command is sent."""
        return self.moveInDirectionForNSeconds('ra+', seconds)

    def moveSouth(self):
        """Commands the mount to move to the south. Mount will continue moving
        until a stop command (stopAllMovement or stopNSMmovement") is issued.
        This command is similar to the up "down" button on the hand controller.
        Returns True when command is sent and response received, otherwise will
        return False."""
        return self.moveInCardinalDirection('south')

    def moveToDefinedAltAndAz(self):
        """Commands the mount to move to the recently (most) defined ALT and AZ.
        The ALT and AZ must be defined previous to this command being useful.
        Returns True when command is sent and response received, otherwise will
        return False."""
        self.myMount.isInIoProzess = True
        moveCommand = ":MSS#"
        self.scope.send(moveCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        self.myMount.isInIoProzess = False
        return False

    def moveToDefinedRaAndDec(self):
        """Commands the mount to move to the recently (most) defined ALT and AZ.
        The ALT and AZ must be defined previous to this command being useful.
        Returns True when command is sent and response received, otherwise will
        return False."""
        self.myMount.isInIoProzess = True
        moveCommand = ":MS1#"
        self.scope.send(moveCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        self.myMount.isInIoProzess = False
        return False

    def moveNorth(self):
        """Commands the mount to move to the north. Mount will continue moving
        until a stop command (stopAllMovement or stopNSMovement") is issued.
        This command is similar to the up "arrow" button on the hand controller.
        Returns True when command is sent and response received, otherwise will
        return False."""
        return self.moveInCardinalDirection('north')

    def moveWest(self):
        """Commands the mount to move to the west. Mount will continue moving
        until a stop command (stopAllMovement or stopNSMmovement") is issued.
        This command is similar to the up "left" button on the hand controller.
        Returns True when command is sent and response received, otherwise will
        return False."""
        return self.moveInCardinalDirection('west')

    def park(self):
        """Park the mount at the most recently defined parking position.
        Returns a true if successful or false if parking failed."""
        self.myMount.isInIoProzess = True
        self.scope.send(':MP1#')
        response = self.scope.recv()
        self.myMount.isInIoProzess = False
        if response == "1":
            # Mount parked OK
            self.parking.isParked = True
        else:
            # Mount was mot parked OK
            self.parking.isParked = False
        return self.parking.isParked

    def parseMovingSpeed(self, rate):
        """Return the mount's current tracking speed in factors of sidarial rate."""
        return str(self.config['trackingSpeeds'][rate]) + 'x'

    def resetSettings(self, confirm: bool):
        """Reset all settings to default. Only applies if True is specified to indicate
        the reset is really wanted. Does not reset any time-based information."""
        if confirm is True:
            self.scope.send(':RAS#')
            self.getAllKindsOfStatus()
            self.getTimeInformation()
            self.getRaAndDec()
            self.getAltAndAz()

    def refreshCoordinates(self):
        """Performs a refresh of the 4 basic mount status commands. These are the 4 updates
        the iOptron driver performs very refresh cycle. Only perform if last update > 1
        second ago to avoid flooding the mount."""
        self.getAltAndAz()
        self.getRaAndDec()
        self.getTimeInformation()

    def setAltitudeLimit(self, limit: str):
        """Set the maximum altitude limt, in degrees. Applies to tracking and slewing. Motion will
        stop if it exceeds this value. Limit is +/- 89 degrees. Returns True after command sent."""
        self.altitude.limit = limit
        self.myMount.isInIoProzess = True
        setCommand = ":SAL" + self.altitude.limit + "#" # Pad with 0's when single digit
        self.scope.send(setCommand)
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False
        return True

    def setMovingSpeed(self, rate):
        """Set the movement speed when the N-S-E-W buttons are used. Rate must be
        given as a multiplier of siderial (e.g. 2 for 2x or 64 for 64x.) The value
        supplied must be supported by the mount. This value is wiped and replaced
        by the default (64x) on the next powerup. Returns True after command is sent."""
        # Set the rate
        self.movingSpeed.code = rate
        self.movingSpeed.description = self.config['StartSpeed']
        movementCommand = ":SR" + str(rate) + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(movementCommand)
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False

    def setCommandedAxisFromDms(self, degrees, minutes, seconds, axis):
        """Defines the commanded axis to the specified degrees, minutes, and seconds. Will convert
        the DMS value to arcseconds and send it to the mount. PRIVATE use to keep things DRY(er).
        Returns True when command is sent and response received, otherwise returns False."""
        arcseconds = str(utilities.convertDmsToArcSeconds(degrees, minutes, seconds)).zfill(8)
        commandDict = {'ra': 'SRA', 'dec': 'Sds', 'alt': 'Sas', 'az': 'Sz'}
        assert axis in commandDict
        axisCommand = ":" + commandDict[axis] + arcseconds + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(axisCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setCommandedAltitude(self, degrees, minutes, seconds):
        """Set the commanded right altitude (ALT). Will return True when command is sent
        and response is received, otherwise will return False. Slew or calibrate commands
        operate based on the most recently defined value."""
        return self.setCommandedAxisFromDms(degrees, minutes, seconds, 'alt')

    def setCommandedAzimuth(self, degrees, minutes, seconds):
        """Set the commanded right azimuth (AZI). Will return True when command is sent
        and response is received, otherwise will return False. Slew or calibrate commands
        operate based on the most recently defined value."""
        return self.setCommandedAxisFromDms(degrees, minutes, seconds, 'az')

    def setCommandedDeclination(self, degrees, minutes, seconds):
        """Set the commanded right declination (DEC). Will return True when command is sent
        and response is received, otherwise will return False. Slew or calibrate commands
        operate based on the most recently defined value."""
        return self.setCommandedAxisFromDms(degrees, minutes, seconds, 'dec')

    def setCommandedRightAscension(self, degrees, minutes, seconds):
        """Set the commanded right ascension (RA). Will return True when command is sent and
        response is received, otherwise will return False. Slew or calibrate commands operate
        based on the most recently defined value."""
        return self.setCommandedAxisFromDms(degrees, minutes, seconds, 'ra')

    def setCurrentPositionAsZero(self):
        """Set the current position as the zero position. Returns True when command is sent and
        a response is received. Otherwise returns False."""
        self.myMount.isInIoProzess = True
        szpCommand = ":SZP#"
        self.scope.send(szpCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setGuidingRate(self, rightAscention: float, declination: float):
        """Set the current RA and DEC guiding rates. The valid range for both is 0.01 - 0.90.
        These values will be used to set the guiding rate * siderial. For example 0.50 will be
        0.50 * siderial guiding. First argument is the RA, second argument is DEC
        Only works for equitorial mounts. Returns true once command is sent
        and a response received."""
        assert self.config['MountType'] == 'equatorial' # only works on EQ mounts
        assert rightAscention >= 0.01 and rightAscention <= 0.90 \
            and declination >= 0.01 and declination <= 0.90
        self.guiding.rightAscentionRate = round(rightAscention, 2)
        self.guiding.declinationRate = round(declination, 2)
        guidingRateCommand = ":RG" + f'{self.guiding.rightAscentionRate:<04n}' \
            + f'{self.guiding.declinationRate:<04n}' + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(guidingRateCommand)
        returnedData = self.scope.recv()
        assert returnedData == '1'
        self.myMount.isInIoProzess = False
        return True

    def setRaGuidingFilterStatus(self, enabled: bool):
        """Set the status of the RA guiding filter for eq mounts with encoders.
        This command may or may not be saved on mount restart - the docs are unclear.
        Returns True after the command is sent."""
        # Only available for eq mounts with encoders
        if self.config['MountType'] != "equatorial" or \
            self.config['Encoders'] is False:
            return None
        self.myMount.isInIoProzess = True
        if enabled is True:
            self.guiding.raFilterEnabled = True
            self.scope.send(":SGF1#")
        if enabled is False:
            self.guiding.raFilterEnabled = False
            self.scope.send(":SGF0#")
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False
        return True

    def setCustomTrackingRate(self, rate):
        """Set a custom tracking rate to n.nnnn of the siderial rate. Only used
        when 'custom' tracking rate is being used. Returns True after command
        is sent."""
        formattedRate = (f"{float(rate):.6f}")
        sendCommand = ":RR" + formattedRate + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(sendCommand)
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False
        return True

    def setDataclassDmsFromArcseconds(self, dataClass):
        """PRIVATE: Set DMS for a given dataclass like Altitude and Azimuth given
        their pre-set arcseconds value. Intended to keep code DRY."""
        dms = utilities.convertArcSecondsToDms(dataClass.arcseconds)
        dataClass.degrees = dms[0]
        dataClass.minutes = dms[1]
        dataClass.seconds = dms[2]

    def setDaylightSavings(self, dst: bool):
        """Enables daylight savings time when true, disables it when false."""
        self.myMount.isInIoProzess = True
        if dst is True:
            self.scope.send(':SDS1#')
        else:
            self.scope.send(':SDS0#')
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False

        # Update time information after setting
        self.getTimeInformation()

    def setHemisphere(self, direction: str):
        """Set the mount's hemisphere. Supplied argument must be 'north', 'south', or
        'n' or 's'. Returns True after command is sent."""
        assert direction.lower() in ['north', 'south', 'n', 's']
        hemisphere = 0 if direction[0:1] == 's' else 1
        command = ":SHE" + str(hemisphere) + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(command)
        self.scope.recv()
        self.myMount.isInIoProzess = False
        return True

    def setLatitude(self, latitude: float):
        """Set the latitude of the mount in degrees. Values range from +/- 90.
        North is positive, south is negative. Returns True when command is sent and
        response reveived, otherwise False is returned."""
        assert -90.0 <= latitude <= 90.0
        self.location.latitude = latitude
        arcseconds = f'{utilities.convertDegreesToArcSeconds(self.location.latitude):08d}'
        latCommand = ":SLO" + arcseconds + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(latCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setLongitude(self, longitude: float):
        """Set the longitude of the mount in degrees. Values range from +/- 180.
        East is positive, west is negative. Returns True when command is sent and
        response reveived, otherwise False is returned."""
        assert -180.0 <= longitude <= 180.0
        self.location.longitude = longitude
        arcseconds = f'{utilities.convertDegreesToArcSeconds(self.location.longitude):08d}'
        longCommand = ":SLO" + arcseconds + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(longCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setMaxSlewingSpeed(self, speed: str):
        """Set the maximum slewing speed. Input is the maximum siderial
        rate desired. Must be '256x', '512x', or 'max'. The max rate
        will depend on the mount. Returns True once command is sent."""
        assert speed in ['256x', '512x', 'max']
        # Set to max by default
        speedBit = '9'
        if speed == '256x':
            speedBit = '7'
        if speed == '512x':
            speedBit = '8'
        speedCommand = ":MSR" + speedBit + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(speedCommand)
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False
        return True

    def setMeridianTreatment(self, treatment: str, limit: str):
        """Set the treatment of the meridian. First argument is whether to
        'stop' or 'flip'. Second argument is the limit, in degrees (nn) to apply
        the behavior to. Will return True once command is sent and response received.
        Only works for equitorial mounts; will return False otherwise."""
        self.meridian.code = treatment
        self.meridian.degreeLimit = limit
        # This works for eq mounts only
        if self.config['MountType'] != 'equatorial':
            return False # only works on EQ mounts
        # This is an eq mount
        treatmentCmd = ":SMT" + self.meridian.code + self.meridian.degreeLimit + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(treatmentCmd)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setParkingAltitude(self, degrees: int, minutes: int, seconds: float):
        """Set the parking altitude. Takes a position in integer degrees, minutes, and seconds.
        Returns True when command is sent and response received. Returns False otherwise."""
        arcseconds = str(utilities.convertDmsToArcSeconds(degrees, minutes, seconds)).zfill(8)
        parkAltCommand = ":SPH" + arcseconds + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(parkAltCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setParkingAzimuth(self, degrees: int, minutes: int, seconds: int):
        """Set the parking azimuth . Takes a position in integer degrees, minutes, and seconds.
        Returns True when command is sent and response received. Returns False otherwise."""
        arcseconds = str(utilities.convertDmsToArcSeconds(degrees, minutes, seconds)).zfill(8)
        parkAltCommand = ":SPA" + arcseconds + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(parkAltCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def setTime(self, dtString):
        """Set the current time on the mount to the current computer's time. Sets to UTC."""
        j2kTime = datetime(2000, 1, 1, 12, 00)
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
        # z z p z z p z z z z|z  z  p  z  z  p  z  z
        dtutc = datetime(int(dtString[6:10]),int(dtString[3:5]),int(dtString[0:2]),int(dtString[10:12]),int(dtString[13:15]),int(dtString[16:18]))
        difference = dtutc - j2kTime
        j2kTime = str(int(difference.total_seconds() * 1000))
        timeCommand = ":SUT" + j2kTime + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(timeCommand)
        self.myMount.isInIoProzess = False

    def setPCTime(self):
        """Set the current time on the mount to the current computer's time. Sets to UTC."""
        j2kTime = str(utilities.getUtcTimeInJ2k()).zfill(13)
        timeCommand = ":SUT" + j2kTime + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(timeCommand)
        self.myMount.isInIoProzess = False

    def setTimezoneOffset(self, offset = utilities.getUtcOffsetMin()):
        """Sets the time zone offset on the mount to the computer's TZ offset."""
        tzOffset = str(offset).zfill(3)
        tzCommand = ":SG" + tzOffset + "#" if offset < 0 else ":SG+" + tzOffset + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(tzCommand)
        # Get the response; do nothing with it
        self.scope.recv()
        self.myMount.isInIoProzess = False

    def setTrackingRate(self, rate):
        """Set the tracking rate of the mount.
        Rate must be one supported by the mount (tracking.availableRates)
        Returns True once command is sent and response reveived, otherwise
        False is returned."""
        rateCommand = ":RT" + str(self.config[rate]) + "#"
        self.myMount.isInIoProzess = True
        self.scope.send(rateCommand)
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def togglePecRecording(self, turnOn: bool):
        """PRIVATE method for toggling PEC recording on and off."""
        self.myMount.isInIoProzess = True
        if self.config['MountType'] == 'equatorial' and \
            self.config['Pec'] is True and \
            self.config['Encoders'] is False:
            # Default is off
            pecCommand = ":SPR1#" if turnOn is True else ":SPR0#"
            self.scope.send(pecCommand)
        else:
            print("PEC recording not usable with this mount")
        self.myMount.isInIoProzess = False

    def startRecordingPec(self):
        """Start recording the periodic error. Only used in eq mounts without encoders.
        Returns True if command was sent and response received, otherwise will return False."""
        self.togglePecRecording(True)
        self.myMount.isInIoProzess = True
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def stopRecordingPec(self):
        """Stop recording the periodic error. Only used in eq mounts without encoders.
        Returns True if command was sent and response received, otherwise will return False."""
        self.togglePecRecording(False)
        self.myMount.isInIoProzess = True
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def startTracking(self):
        """Commands the mount to start tracking. Returns True when command is sent and
        received, otherwise returns False."""
        self.myMount.isInIoProzess = True
        trackingCommand = ":ST1#"
        self.scope.send(trackingCommand)
        if self.scope.recv() == '1':
            self.tracking.isTracking = True
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def stopAllMovement(self):
        """Stop all slewing no matter the source of slewing or the direction(s)."""
        self.myMount.isInIoProzess = True
        self.scope.send(':Q#')
        self.isSlewing = False
        self.myMount.isInIoProzess = False

    def stopEOrWMovement(self):
        """Stop movement in the east or west directions. Useful when using the
        commands to slew in the specfic directions. Mimics the arrow buttons on
        the hand controller."""
        self.myMount.isInIoProzess = True
        self.scope.send(':qR#')
        self.isSlewing = False
        self.myMount.isInIoProzess = False

    def stopNOrSMovement(self):
        """Stop movement in the north or south directions. Useful when using the
        commands to slew in the specfic directions. Mimics the arrow buttons on
        the hand controller."""
        self.myMount.isInIoProzess = True
        self.scope.send(':qD#')
        self.isSlewing = False
        self.myMount.isInIoProzess = False

    def stopTracking(self):
        """Commands the mount to stop tracking. Returns True when command is sent and
        received, otherwise returns False."""
        trackingCommand = ":ST0#"
        self.myMount.isInIoProzess = True
        self.scope.send(trackingCommand)
        if self.scope.recv() == '1':
            self.tracking.isTracking = False
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def synchronizeMount(self):
        """Synchrolizes the mount. The most recently defined RA and DEC, or ALT and AZ
        become the commanded values. Ignored is slewing is in progress. Only useful for
        initial calibration; not to be used when tracking. Returns True once command
        is sent and response received. Otherwise False is returned."""
        self.myMount.isInIoProzess = True
        self.scope.send(":CM#")
        if self.scope.recv() == '1':
            self.myMount.isInIoProzess = False
            return True
        else:
            self.myMount.isInIoProzess = False
            return False

    def unpark(self):
        """Unpark the moint. If the mount is unparked already, this does nothing. """
        self.myMount.isInIoProzess = True
        self.scope.send(':MP0#')
        # Always returns a 1
        self.parking.isParked = False
        self.myMount.isInIoProzess = False
        return self.parking.isParked

    def updateStatus(self):
        """Call all of the (4) update commands to get the latest status of the mount."""
        currentTime = time.time()
        if currentTime - self.lastUpdate > 1:
            self.getAllKindsOfStatus()
            self.getTimeInformation()
            self.getRaAndDec()
        # Apply the latest update time
        self.lastUpdate = time.time()
