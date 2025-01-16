"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from enum import Enum

class StatusCode(Enum):
    """
    Status codes reported by APIs, including OK,
    warnings, and errors.
    """

    OK = 0
    """
    No Error
    """
    TASK_IS_BUSY = -100
    """
    Diagnostic Server is busy with another command.
    """
    INVALID_DEVICE_SPEC = -101
    """
    InvalidDeviceSpec
    """
    ECU_IS_NOT_PRESENT = -102
    """
    Device is not present. Verify the device is connected and powered, and that the
    CAN bus is terminated.
    """
    COULD_NOT_ENTER_BL = -103
    """
    Could not put the device into bootloader mode.
    """
    COULD_NOT_CONFIRM_BL = -104
    """
    Could not confirm the device has entered the bootloader.
    """
    COULD_NOT_ERASE = -105
    """
    Could not erase flash.
    """
    COULD_NOT_SEND_FLASH = -106
    """
    Could not field upgrade the device.
    """
    COULD_NOT_VALIDATE = -107
    """
    Bootloader could not verify integrity of the flashed application.
    """
    COULD_NOT_RUN_APP = -108
    """
    Could not run the device firmware application.
    """
    COULD_NOT_REQ_SET_ID = -109
    """
    Unable to set ID to this device.
    """
    COULD_NOT_CONFIRM_ID = -110
    """
    Could not verify that the changed ID took effect.
    """
    FLASH_WAS_GOOD = -111
    """
    Device field upgrade was successful.
    """
    APP_TOO_OLD = -112
    """
    Device firmware application is too old.
    """
    COULD_NOT_REQ_SET_DESC = -113
    """
    Unable to set name to this device.
    """
    COMPILE_SZ_IS_WRONG = -114
    """
    CompileSzIsWrong
    """
    GADGETEER_DEVICE_NO_SET_ID = -115
    """
    Cannot set the ID of a gadgeteer device.
    """
    INVALID_TASK = -116
    """
    This diagnostic action is not supported.
    """
    NOT_IMPLEMENTED = -117
    """
    Not Implemented, check latest installer.
    """
    NO_DEVICES_ON_BUS = -118
    """
    NoDevicesOnBus
    """
    MORE_THAN_ONE_FILE = -119
    """
    MoreThanOneFile
    """
    NODE_IS_INVALID = -120
    """
    Specified device was not found. Verify the device is connected and powered, and
    that the CAN bus is terminated.
    """
    INVALID_DEVICE_DESCRIPTOR = -121
    """
    InvalidDeviceDescriptor
    """
    COULD_NOT_SEND_CAN_FRAME = -123
    """
    CouldNotSendCanFrame
    """
    NORMAL_MODE_MSG_NOT_PRESENT = -124
    """
    NormalModeMsgNotPresent
    """
    FEATURE_NOT_SUPPORTED = -125
    """
    This feature is not supported.
    """
    NOT_UPDATING = -126
    """
    The diagnostic server is not field upgrading any devices.
    """
    CORRUPTED_POST = -127
    """
    CorruptedPOST
    """
    NO_CONFIGS = -128
    """
    This device did not report any available configs. Verify firmware and
    diagnostics are up-to-date.
    """
    CONFIG_FAILED = -129
    """
    ConfigFailed
    """
    COULD_NOT_REQ_FACTORY_DEFAULT = -130
    """
    Unable to factory default this device.
    """
    CUSTOM_NAME_NOT_SUPPORTED = -131
    """
    CustomNameNotSupported
    """
    CONFIG_READ_WRITE_MISMATCH = -132
    """
    The configs read from the device do not match the configs that were written.
    """
    COULD_NOT_REQ_SET_CONFIGS = -133
    """
    Could not apply the device configs.
    """
    INSUFFICIENT_SZ = -134
    """
    InsufficientSz
    """
    INVALID_MODEL = -135
    """
    This feature is not supported for this device model.
    """
    COULD_NOT_REQ_DEV_INFO = -140
    """
    CouldNotReqDevInfo
    """
    NO_CONTROLS = -141
    """
    This device does not support new controls.
    """
    DEVICE_IS_NULL = -142
    """
    DeviceIsNull
    """
    DEVICE_DID_NOT_RESPOND_TO_DIAG_REQ = -143
    """
    DeviceDidNotRespondToDiagReq
    """
    ONLY_SUPPORTED_IN_TUNERX = -144
    """
    This feature requires Tuner X.
    """
    CANIV_CLI_ERROR = -145
    """
    Command-line issue with caniv.
    """
    INVALID_CRF_BAD_HEADER = -200
    """
    InvalidCrfBadHeader
    """
    INVALID_CRF_FILE_SZ_INVALD = -201
    """
    InvalidCrfFileSzInvald
    """
    INVALID_CRF_WRONG_PRODUCT = -202
    """
    Specified CRF is for the wrong product.
    """
    INVALID_CRF_NO_SECTS = -203
    """
    InvalidCrfNoSects
    """
    INVALID_CRF_BAD_SECT_HEADER = -204
    """
    InvalidCrfBadSectHeader
    """
    INVALID_CRF_BAD_SECT_SIZE = -205
    """
    InvalidCrfBadSectSize
    """
    NO_CRF_FILE = -206
    """
    Specified CRF file could not be found.
    """
    COULD_NOT_FIND_DYNAMIC_ID = -300
    """
    CouldNotFindDynamicId
    """
    DID_NOT_GET_DHCP = -301
    """
    DidNotGetDhcp
    """
    DID_NOT_GET_FULL_DHCP = -302
    """
    DidNotGetFullDhcp
    """
    INVALID_LICENSE_RESP = -350
    """
    InvalidLicenseResp
    """
    INVALID_CANIV_CACHE = -351
    """
    InvalidCanivCache
    """
    CANNOT_OPEN_SERIAL_PORT = -500
    """
    CannotOpenSerialPort
    """
    CANNOT_WRITE_SERIAL_PORT = -501
    """
    CannotWriteSerialPort
    """
    CANNOT_READ_SERIAL_PORT = -502
    """
    CannotReadSerialPort
    """
    CANNOT_SERIAL_TO_DEVICE = -503
    """
    CannotSerialToDevice
    """
    NO_SERIAL_CONTROL_FRAME_RESP = -504
    """
    NoSerialControlFrameResp
    """
    CANNOT_OPEN_UDP_PORT = -600
    """
    CannotOpenUdpPort
    """
    CANNOT_WRITE_UDP_PORT = -601
    """
    CannotWriteUdpPort
    """
    CANNOT_READ_UDP_PORT = -602
    """
    CannotReadUdpPort
    """
    CANNOT_UDP_TO_DEVICE = -603
    """
    CannotUdpToDevice
    """
    NO_UDP_CONTROL_FRAME_RESP = -604
    """
    NoUdpControlFrameResp
    """
    TIMEOUT_ISO15_RESPONSE = -605
    """
    TimeoutIso15Response
    """
    INVALID_JSON = -700
    """
    InvalidJson
    """
    APP_IS_TERMINATING = -800
    """
    The user application is shutting down.
    """
    CAN_MESSAGE_STALE = 1000
    """
    CAN message is stale, data is valid but old. Check the CAN bus wiring, CAN bus
    utilization, and power to the device.
    """
    BUFFER_FULL = 1006
    """
    Buffer is full, cannot insert more data.
    """
    PULSE_WIDTH_SENSOR_NOT_PRESENT = 1010
    """
    PulseWidthSensorNotPresent
    """
    GENERAL_WARNING = 1100
    """
    General Warning Occurred.
    """
    FIRM_VERSION_COULD_NOT_BE_RETRIEVED = 1103
    """
    Firm Vers could not be retrieved. Use Phoenix Tuner X to check ID and
    firmware(CRF) version.
    """
    FEATURES_NOT_AVAILABLE_YET = 1104
    """
    This feature will be supported in a future update.
    """
    CONTROL_MODE_NOT_VALID = 1105
    """
    The control mode is not valid for this function.
    """
    CONTROL_MODE_NOT_SUPPORTED_YET = 1106
    """
    This control mode is not supported yet.  A future release will supported this
    soon.
    """
    MOT_PROF_FIRM_THRESHOLD = 1109
    """
    Motor Controller must have >= 3.2 firmware for motion profile control mode.
    """
    MOT_PROF_FIRM_THRESHOLD2 = 1110
    """
    Motor Controller must have >= 3.4 firmware for advanced PID0/PID1 features.
    """
    SIM_DEVICE_NOT_FOUND = 1200
    """
    SimDeviceNotFound
    """
    SIM_PHYSICS_TYPE_NOT_SUPPORTED = 1201
    """
    SimPhysicsTypeNotSupported
    """
    SIM_DEVICE_ALREADY_EXISTS = 1202
    """
    SimDeviceAlreadyExists
    """
    TX_FAILED = -1001
    """
    Could not transmit CAN Frame.
    """
    INVALID_PARAM_VALUE = -1002
    """
    An invalid argument was passed into the function/VI, such as a null pointer.
    """
    RX_TIMEOUT = -1003
    """
    CAN frame not received/too-stale. Check the CAN bus wiring, CAN bus utilization,
    and power to the device.
    """
    TX_TIMEOUT = -1004
    """
    CAN Transmit timed out.
    """
    UNEXPECTED_ARB_ID = -1005
    """
    ArbID is incorrect.
    """
    CAN_OVERFLOWED = -1006
    """
    CanOverflowed
    """
    SENSOR_NOT_PRESENT = -1007
    """
    Sensor Not Present.
    """
    FIRMWARE_TOO_OLD = -1008
    """
    Firmware Too Old.  Use Phoenix Tuner X to field upgrade your CTRE CAN device
    firmware(CRF).  Then restart your robot application to clear this error.
    """
    COULD_NOT_CHANGE_PERIOD = -1009
    """
    Control Frame Period could not be changed.  Most likely it is not being
    transmitted.
    """
    BUFFER_FAILURE = -1010
    """
    BufferFailure
    """
    FIRMWARE_NON_FRC = -1011
    """
    Firmware is legacy non-FRC version.  Use Phoenix Tuner X to field upgrade your
    CTRE CAN device firmware(CRF).  Firmware greater than 20.0 required.
    """
    GENERAL_ERROR = -1100
    """
    General Error Occurred.
    """
    SIG_NOT_UPDATED = -1200
    """
    No new response to update signal.
    """
    NOT_ALL_PIDVALUES_UPDATED = -1201
    """
    NotAllPIDValuesUpdated
    """
    GEN_PORT_ERROR = -1300
    """
    GEN_PORT_ERROR
    """
    PORT_MODULE_TYPE_MISMATCH = -1301
    """
    PORT_MODULE_TYPE_MISMATCH
    """
    GEN_MODULE_ERROR = -1400
    """
    GEN_MODULE_ERROR
    """
    MODULE_NOT_INIT_SET_ERROR = -1401
    """
    MODULE_NOT_INIT_SET_ERROR
    """
    MODULE_NOT_INIT_GET_ERROR = -1402
    """
    MODULE_NOT_INIT_GET_ERROR
    """
    WHEEL_RADIUS_TOO_SMALL = -1500
    """
    Wheel Radius is too small, cannot get distance traveled.
    """
    TICKS_PER_REV_ZERO = -1501
    """
    Ticks per revolution is 0, cannot get heading.
    """
    DISTANCE_BETWEEN_WHEELS_TOO_SMALL = -1502
    """
    Distance between wheels is too small, cannot get heading.
    """
    GAINS_ARE_NOT_SET = -1503
    """
    GainsAreNotSet
    """
    WRONG_REMOTE_LIMIT_SWITCH_SOURCE = -1504
    """
    Use RemoteLimitSwitchSource instead of LimitSwitchSource.
    """
    DOUBLE_VOLTAGE_COMPENSATING_WPI = -1505
    """
    Motor Controller Voltage Compensation should not be used with setVoltage(). 
    This causes compensation to happen twice.  Disable Voltage Compensation by
    calling enableVoltageCompensation(false) in order to use setVoltage().
    """
    CANDLE_ANIM_SLOT_OUT_OF_BOUNDS = -1506
    """
    CANdleAnimSlotOutOfBounds
    """
    INCOMPATIBLE_MODE = -1600
    """
    IncompatibleMode
    """
    INVALID_HANDLE = -1601
    """
    Handle passed into function is incorrect.
    """
    FEATURE_REQUIRES_HIGHER_FIRM = -1700
    """
    Features requires newer firmware version.
    """
    CONFIG_FACTORY_DEFAULT_REQUIRES_HIGHER_FIRM = -1702
    """
    Config factory default features require firmware >=3.10.
    """
    CONFIG_MOTION_SCURVE_REQUIRES_HIGHER_FIRM = -1703
    """
    Config Motion S Curve Strength features require firmware >=4.16.
    """
    TALON_FXFIRMWARE_PRE_VBAT_DETECT = -1704
    """
    Talon FX(Falcon 500) Firmware Too Old.  Use Phoenix Tuner to field upgrade your
    CTRE CAN device firmware(CRF) to >=20.3. Then restart your robot application to
    clear this error.
    """
    CANDLE_ANIMATIONS_REQUIRE_HIGHER_FIRM = -1705
    """
    CANdleAnimationsRequireHigherFirm
    """
    LIBRARY_COULD_NOT_BE_LOADED = -1800
    """
    LibraryCouldNotBeLoaded
    """
    MISSING_ROUTINE_IN_LIBRARY = -1801
    """
    MissingRoutineInLibrary
    """
    RESOURCE_NOT_AVAILABLE = -1802
    """
    ResourceNotAvailable
    """
    MUSIC_FILE_NOT_FOUND = -1900
    """
    Could not find music file specified, try specifying an absolute path.
    """
    MUSIC_FILE_WRONG_SIZE = -1901
    """
    Music file size is incorrect, could not parse correctly. Ensure you're using
    Tuner to generate file.
    """
    MUSIC_FILE_TOO_NEW = -1902
    """
    Music file version is too new, update Phoenix to utilize this file.
    """
    MUSIC_FILE_INVALID = -1903
    """
    Music file is invalid. Ensure you're using Tuner to generate file.
    """
    INVALID_ORCHESTRA_ACTION = -1904
    """
    An invalid orchestra action occurred. Ensure a music file is loaded.
    """
    MUSIC_FILE_TOO_OLD = -1905
    """
    This music file version is too old. Regenerate file using Tuner.
    """
    MUSIC_INTERRUPTED = -1906
    """
    Music interrupted due to one of the instruments being commanded a different
    control mode. Press Play to resume music.
    """
    MUSIC_NOT_SUPPORTED = -1907
    """
    This device doesn't support MusicTone control mode.
    """
    INVALID_INTERFACE = -2000
    """
    kInvalidInterface
    """
    INVALID_GUID = -2001
    """
    kInvalidGuid
    """
    INVALID_CLASS = -2002
    """
    kInvalidClass
    """
    INVALID_PROTOCOL = -2003
    """
    kInvalidProtocol
    """
    INVALID_PATH = -2004
    """
    kInvalidPath
    """
    GENERAL_WIN_USB_ERROR = -2005
    """
    kGeneralWinUsbError
    """
    FAILED_SETUP = -2006
    """
    kFailedSetup
    """
    LISTEN_FAILED = -2007
    """
    kListenFailed
    """
    SEND_FAILED = -2008
    """
    kSendFailed
    """
    RECEIVE_FAILED = -2009
    """
    kReceiveFailed
    """
    INVALID_RESP_FORMAT = -2010
    """
    kInvalidRespFormat
    """
    WIN_USB_INIT_FAILED = -2011
    """
    kWinUsbInitFailed
    """
    WIN_USB_QUERY_FAILED = -2012
    """
    kWinUsbQueryFailed
    """
    WIN_USB_GENERAL_ERROR = -2013
    """
    kWinUsbGeneralError
    """
    ACCESS_DENIED = -2014
    """
    kAccessDenied
    """
    FIRMWARE_INVALID_RESPONSE = -2015
    """
    kFirmwareInvalidResponse
    """
    STATUS_CODE_NOT_INITIALIZED = -10000
    """
    This StatusCode has not been initialized. Make sure the StatusCode is getting
    assigned to the return of a method.
    """
    WARNING_NOT_INITIALIZED = 10000
    """
    WarningNotInitialized
    """
    HW_TIMESTAMP_OUT_OF_SYNC = 10001
    """
    The timestamp reported by CANivore is at least 10ms older than the timestamp
    reported by the system, indicating it's fallen out of sync. This does not impact
    the data of this message, only the timing.
    """
    FREQUENT_CONFIG_CALLS = 10002
    """
    Do not apply or refresh configs periodically, as configs are blocking.
    """
    INVALID_NETWORK = -10001
    """
    InvalidNetwork
    """
    MULTI_SIGNAL_NOT_SUPPORTED = -10002
    """
    The CAN bus does not support multi-signal synchronization.
    """
    COULD_NOT_CAST = -10003
    """
    Could not cast from base value to this particular signal's type
    """
    NOT_FOUND = -10004
    """
    Could not find this value when searching for it
    """
    NOT_SUPPORTED = -10005
    """
    This is not supported
    """
    MISSING_CONTEXT = -10006
    """
    Could not determine context from this device hash
    """
    MODEL_MISMATCH = -10007
    """
    Model name in license file does not match model name of selected device.
    """
    SERIAL_MISMATCH = -10008
    """
    Serial Number in license file does not match model name of selected device.
    """
    NO_FILE = -10009
    """
    Could not find specified file.
    """
    LICENSE_DOWNLOAD_FAILED = -10010
    """
    License did not successfully download to Device.
    """
    SELF_TEST_IS_EMPTY = -10011
    """
    Self Test report does not have any values, is the firmware up to date?
    """
    SIGNAL_LOOKUP_FAILED = -10012
    """
    Failed to lookup signal properties.  This can happen if the fimware is too new
    and supports signals that older APIs do not support.
    """
    INVALID_MODE_TO_GET_SIGNAL = -10013
    """
    The current mode of the device is invalid for getting this signal.
    """
    UNLICENSED_DEVICE = -10014
    """
    Device is not licensed. Cannot get any data from it.
    """
    INVALID_SIZE = -10015
    """
    Size is invalid.
    """
    INVALID_LICENSE_RESPONSE = -10016
    """
    InvalidLicenseResponse
    """
    INVALID_CONTEXT = -10017
    """
    InvalidContext
    """
    INTERNAL_ERROR = -10018
    """
    InternalError
    """
    DEVICE_RESPONSE_INCORRECT = -10019
    """
    kDeviceResponseIncorrect
    """
    ERROR_POLLING_FOR_DEVICES = -10020
    """
    kErrorPollingForDevices
    """
    COULD_NOT_RETRIEVEV6_FIRMWARE = -10021
    """
    Device firmware could not be retrieved. Check that the device is running v6
    firmware, the device ID is correct, the specified CAN bus is correct, and the
    device is powered.
    """
    COULD_NOT_DECODE_DEVICE_FIRMWARE = -10022
    """
    Device firmware could not be decoded. Check that the device is running v6
    firmware, the device ID is correct, the specified CAN bus is correct, and the
    device is powered.
    """
    INVALID_IDTO_FOLLOW = -10023
    """
    The values specified for master are in valid.  Make sure the Device ID of master
    are correct.
    """
    USING_PRO_FEATURE_ON_UNLICENSED_DEVICE = -10024
    """
    Using a Pro only feature on an unlicensed device. The device may not behave as
    expected if it continues to operate while unlicensed.
    """
    FIRMWARE_TOO_NEW = -10025
    """
    Firmware Too New.  Use Phoenix Tuner X to field upgrade your CTRE CAN device
    firmware(CRF) to a compatible version.  Then restart your robot application to
    clear this error.
    """
    COULD_NOT_SERIALIZE = -10026
    """
    The data frame could not be serialized for transmit.
    """
    MECHANISM_FAULTED = -10027
    """
    The mechanism is disabled due to a fault in one of the devices.
    """
    FIRMWARE_VERS_NOT_COMPATIBLE = -10028
    """
    Firmware version is not compatible with this version of Phoenix. Make sure your
    firmware and API major versions match.
    """
    DIRECTORY_MISSING = -10029
    """
    Could not find specified directory.
    """
    API_TOO_OLD = -10030
    """
    This API version is too old for the firmware on the device. Either upgrade the
    API to a newer version or downgrade the device firmware to an older version for
    correct behavior.
    """
    LOGGER_NOT_RUNNING = -10031
    """
    The signal logger is not running. Start the signal logger before writing any
    signals.
    """
    TIMEOUT_CANNOT_BE_ZERO = -10032
    """
    Blocking operations, such as configs, cannot have a timeout of 0. Pass in a
    non-zero timeout (typically 0.050+ seconds) for normal operation.
    """
    CANNOT_LICENSE_WHILE_ENABLED = -10033
    """
    Device cannot be licensed while it is control enabled. Disable and neutral the
    device to apply the licenses.
    """
    INVALID_FILE = -10034
    """
    Could not open or read the given file.
    """
    HOOT_LOG_TOO_OLD = -10035
    """
    The given hoot log requires an older version of Phoenix API.
    """
    HOOT_LOG_TOO_NEW = -10036
    """
    The given hoot log requires a newer version of Phoenix API.
    """
    UNLICENSED_HOOT_LOG = -10037
    """
    Hoot log is not licensed. Cannot get any data from it.
    """
    CANNOT_STEP_WHILE_UNPAUSED = -10038
    """
    The simulation timing cannot be advanced by a time step while unpaused. Pause
    the simulator before advancing time.
    """
    MULTIPLE_REPLAY_NOT_SUPPORTED = -10039
    """
    Hoot replay does not support replaying multiple files. Ensure that only one file
    is loaded at a time.
    """
    USER_SIGNAL_LIMIT_EXCEEDED = -10040
    """
    The maximum number of loggable user signals has been exceeded. Additional user
    signals will not be logged.
    """
    INVALID_DEVICE_MODEL = -10041
    """
    The provided model was not a valid device type.
    """

    def is_error(self) -> bool:
        """
        Gets whether this code is an error.

        :returns: True if this code is an error
        :rtype: bool
        """
        return self.value < 0

    def is_warning(self) -> bool:
        """
        Gets whether this code is a warning.

        :returns: True if this code is a warning
        :rtype: bool
        """
        return self.value > 0

    def is_ok(self) -> bool:
        """
        Gets whether this code is OK.

        :returns: True if this code is OK
        :rtype: bool
        """
        return self.value == 0

    @property
    def name(self) -> str:
        """
        Gets the name of this StatusCode.

        :returns: Name of this StatusCode
        :rtype: str
        """
        if False:
            pass
        elif self.value == 0:
            return "OK"
        elif self.value == -100:
            return "TASK_IS_BUSY"
        elif self.value == -101:
            return "INVALID_DEVICE_SPEC"
        elif self.value == -102:
            return "ECU_IS_NOT_PRESENT"
        elif self.value == -103:
            return "COULD_NOT_ENTER_BL"
        elif self.value == -104:
            return "COULD_NOT_CONFIRM_BL"
        elif self.value == -105:
            return "COULD_NOT_ERASE"
        elif self.value == -106:
            return "COULD_NOT_SEND_FLASH"
        elif self.value == -107:
            return "COULD_NOT_VALIDATE"
        elif self.value == -108:
            return "COULD_NOT_RUN_APP"
        elif self.value == -109:
            return "COULD_NOT_REQ_SET_ID"
        elif self.value == -110:
            return "COULD_NOT_CONFIRM_ID"
        elif self.value == -111:
            return "FLASH_WAS_GOOD"
        elif self.value == -112:
            return "APP_TOO_OLD"
        elif self.value == -113:
            return "COULD_NOT_REQ_SET_DESC"
        elif self.value == -114:
            return "COMPILE_SZ_IS_WRONG"
        elif self.value == -115:
            return "GADGETEER_DEVICE_NO_SET_ID"
        elif self.value == -116:
            return "INVALID_TASK"
        elif self.value == -117:
            return "NOT_IMPLEMENTED"
        elif self.value == -118:
            return "NO_DEVICES_ON_BUS"
        elif self.value == -119:
            return "MORE_THAN_ONE_FILE"
        elif self.value == -120:
            return "NODE_IS_INVALID"
        elif self.value == -121:
            return "INVALID_DEVICE_DESCRIPTOR"
        elif self.value == -123:
            return "COULD_NOT_SEND_CAN_FRAME"
        elif self.value == -124:
            return "NORMAL_MODE_MSG_NOT_PRESENT"
        elif self.value == -125:
            return "FEATURE_NOT_SUPPORTED"
        elif self.value == -126:
            return "NOT_UPDATING"
        elif self.value == -127:
            return "CORRUPTED_POST"
        elif self.value == -128:
            return "NO_CONFIGS"
        elif self.value == -129:
            return "CONFIG_FAILED"
        elif self.value == -130:
            return "COULD_NOT_REQ_FACTORY_DEFAULT"
        elif self.value == -131:
            return "CUSTOM_NAME_NOT_SUPPORTED"
        elif self.value == -132:
            return "CONFIG_READ_WRITE_MISMATCH"
        elif self.value == -133:
            return "COULD_NOT_REQ_SET_CONFIGS"
        elif self.value == -134:
            return "INSUFFICIENT_SZ"
        elif self.value == -135:
            return "INVALID_MODEL"
        elif self.value == -140:
            return "COULD_NOT_REQ_DEV_INFO"
        elif self.value == -141:
            return "NO_CONTROLS"
        elif self.value == -142:
            return "DEVICE_IS_NULL"
        elif self.value == -143:
            return "DEVICE_DID_NOT_RESPOND_TO_DIAG_REQ"
        elif self.value == -144:
            return "ONLY_SUPPORTED_IN_TUNERX"
        elif self.value == -145:
            return "CANIV_CLI_ERROR"
        elif self.value == -200:
            return "INVALID_CRF_BAD_HEADER"
        elif self.value == -201:
            return "INVALID_CRF_FILE_SZ_INVALD"
        elif self.value == -202:
            return "INVALID_CRF_WRONG_PRODUCT"
        elif self.value == -203:
            return "INVALID_CRF_NO_SECTS"
        elif self.value == -204:
            return "INVALID_CRF_BAD_SECT_HEADER"
        elif self.value == -205:
            return "INVALID_CRF_BAD_SECT_SIZE"
        elif self.value == -206:
            return "NO_CRF_FILE"
        elif self.value == -300:
            return "COULD_NOT_FIND_DYNAMIC_ID"
        elif self.value == -301:
            return "DID_NOT_GET_DHCP"
        elif self.value == -302:
            return "DID_NOT_GET_FULL_DHCP"
        elif self.value == -350:
            return "INVALID_LICENSE_RESP"
        elif self.value == -351:
            return "INVALID_CANIV_CACHE"
        elif self.value == -500:
            return "CANNOT_OPEN_SERIAL_PORT"
        elif self.value == -501:
            return "CANNOT_WRITE_SERIAL_PORT"
        elif self.value == -502:
            return "CANNOT_READ_SERIAL_PORT"
        elif self.value == -503:
            return "CANNOT_SERIAL_TO_DEVICE"
        elif self.value == -504:
            return "NO_SERIAL_CONTROL_FRAME_RESP"
        elif self.value == -600:
            return "CANNOT_OPEN_UDP_PORT"
        elif self.value == -601:
            return "CANNOT_WRITE_UDP_PORT"
        elif self.value == -602:
            return "CANNOT_READ_UDP_PORT"
        elif self.value == -603:
            return "CANNOT_UDP_TO_DEVICE"
        elif self.value == -604:
            return "NO_UDP_CONTROL_FRAME_RESP"
        elif self.value == -605:
            return "TIMEOUT_ISO15_RESPONSE"
        elif self.value == -700:
            return "INVALID_JSON"
        elif self.value == -800:
            return "APP_IS_TERMINATING"
        elif self.value == 1000:
            return "CAN_MESSAGE_STALE"
        elif self.value == 1006:
            return "BUFFER_FULL"
        elif self.value == 1010:
            return "PULSE_WIDTH_SENSOR_NOT_PRESENT"
        elif self.value == 1100:
            return "GENERAL_WARNING"
        elif self.value == 1103:
            return "FIRM_VERSION_COULD_NOT_BE_RETRIEVED"
        elif self.value == 1104:
            return "FEATURES_NOT_AVAILABLE_YET"
        elif self.value == 1105:
            return "CONTROL_MODE_NOT_VALID"
        elif self.value == 1106:
            return "CONTROL_MODE_NOT_SUPPORTED_YET"
        elif self.value == 1109:
            return "MOT_PROF_FIRM_THRESHOLD"
        elif self.value == 1110:
            return "MOT_PROF_FIRM_THRESHOLD2"
        elif self.value == 1200:
            return "SIM_DEVICE_NOT_FOUND"
        elif self.value == 1201:
            return "SIM_PHYSICS_TYPE_NOT_SUPPORTED"
        elif self.value == 1202:
            return "SIM_DEVICE_ALREADY_EXISTS"
        elif self.value == -1001:
            return "TX_FAILED"
        elif self.value == -1002:
            return "INVALID_PARAM_VALUE"
        elif self.value == -1003:
            return "RX_TIMEOUT"
        elif self.value == -1004:
            return "TX_TIMEOUT"
        elif self.value == -1005:
            return "UNEXPECTED_ARB_ID"
        elif self.value == -1006:
            return "CAN_OVERFLOWED"
        elif self.value == -1007:
            return "SENSOR_NOT_PRESENT"
        elif self.value == -1008:
            return "FIRMWARE_TOO_OLD"
        elif self.value == -1009:
            return "COULD_NOT_CHANGE_PERIOD"
        elif self.value == -1010:
            return "BUFFER_FAILURE"
        elif self.value == -1011:
            return "FIRMWARE_NON_FRC"
        elif self.value == -1100:
            return "GENERAL_ERROR"
        elif self.value == -1200:
            return "SIG_NOT_UPDATED"
        elif self.value == -1201:
            return "NOT_ALL_PIDVALUES_UPDATED"
        elif self.value == -1300:
            return "GEN_PORT_ERROR"
        elif self.value == -1301:
            return "PORT_MODULE_TYPE_MISMATCH"
        elif self.value == -1400:
            return "GEN_MODULE_ERROR"
        elif self.value == -1401:
            return "MODULE_NOT_INIT_SET_ERROR"
        elif self.value == -1402:
            return "MODULE_NOT_INIT_GET_ERROR"
        elif self.value == -1500:
            return "WHEEL_RADIUS_TOO_SMALL"
        elif self.value == -1501:
            return "TICKS_PER_REV_ZERO"
        elif self.value == -1502:
            return "DISTANCE_BETWEEN_WHEELS_TOO_SMALL"
        elif self.value == -1503:
            return "GAINS_ARE_NOT_SET"
        elif self.value == -1504:
            return "WRONG_REMOTE_LIMIT_SWITCH_SOURCE"
        elif self.value == -1505:
            return "DOUBLE_VOLTAGE_COMPENSATING_WPI"
        elif self.value == -1506:
            return "CANDLE_ANIM_SLOT_OUT_OF_BOUNDS"
        elif self.value == -1600:
            return "INCOMPATIBLE_MODE"
        elif self.value == -1601:
            return "INVALID_HANDLE"
        elif self.value == -1700:
            return "FEATURE_REQUIRES_HIGHER_FIRM"
        elif self.value == -1702:
            return "CONFIG_FACTORY_DEFAULT_REQUIRES_HIGHER_FIRM"
        elif self.value == -1703:
            return "CONFIG_MOTION_SCURVE_REQUIRES_HIGHER_FIRM"
        elif self.value == -1704:
            return "TALON_FXFIRMWARE_PRE_VBAT_DETECT"
        elif self.value == -1705:
            return "CANDLE_ANIMATIONS_REQUIRE_HIGHER_FIRM"
        elif self.value == -1800:
            return "LIBRARY_COULD_NOT_BE_LOADED"
        elif self.value == -1801:
            return "MISSING_ROUTINE_IN_LIBRARY"
        elif self.value == -1802:
            return "RESOURCE_NOT_AVAILABLE"
        elif self.value == -1900:
            return "MUSIC_FILE_NOT_FOUND"
        elif self.value == -1901:
            return "MUSIC_FILE_WRONG_SIZE"
        elif self.value == -1902:
            return "MUSIC_FILE_TOO_NEW"
        elif self.value == -1903:
            return "MUSIC_FILE_INVALID"
        elif self.value == -1904:
            return "INVALID_ORCHESTRA_ACTION"
        elif self.value == -1905:
            return "MUSIC_FILE_TOO_OLD"
        elif self.value == -1906:
            return "MUSIC_INTERRUPTED"
        elif self.value == -1907:
            return "MUSIC_NOT_SUPPORTED"
        elif self.value == -2000:
            return "INVALID_INTERFACE"
        elif self.value == -2001:
            return "INVALID_GUID"
        elif self.value == -2002:
            return "INVALID_CLASS"
        elif self.value == -2003:
            return "INVALID_PROTOCOL"
        elif self.value == -2004:
            return "INVALID_PATH"
        elif self.value == -2005:
            return "GENERAL_WIN_USB_ERROR"
        elif self.value == -2006:
            return "FAILED_SETUP"
        elif self.value == -2007:
            return "LISTEN_FAILED"
        elif self.value == -2008:
            return "SEND_FAILED"
        elif self.value == -2009:
            return "RECEIVE_FAILED"
        elif self.value == -2010:
            return "INVALID_RESP_FORMAT"
        elif self.value == -2011:
            return "WIN_USB_INIT_FAILED"
        elif self.value == -2012:
            return "WIN_USB_QUERY_FAILED"
        elif self.value == -2013:
            return "WIN_USB_GENERAL_ERROR"
        elif self.value == -2014:
            return "ACCESS_DENIED"
        elif self.value == -2015:
            return "FIRMWARE_INVALID_RESPONSE"
        elif self.value == -10000:
            return "STATUS_CODE_NOT_INITIALIZED"
        elif self.value == 10000:
            return "WARNING_NOT_INITIALIZED"
        elif self.value == 10001:
            return "HW_TIMESTAMP_OUT_OF_SYNC"
        elif self.value == 10002:
            return "FREQUENT_CONFIG_CALLS"
        elif self.value == -10001:
            return "INVALID_NETWORK"
        elif self.value == -10002:
            return "MULTI_SIGNAL_NOT_SUPPORTED"
        elif self.value == -10003:
            return "COULD_NOT_CAST"
        elif self.value == -10004:
            return "NOT_FOUND"
        elif self.value == -10005:
            return "NOT_SUPPORTED"
        elif self.value == -10006:
            return "MISSING_CONTEXT"
        elif self.value == -10007:
            return "MODEL_MISMATCH"
        elif self.value == -10008:
            return "SERIAL_MISMATCH"
        elif self.value == -10009:
            return "NO_FILE"
        elif self.value == -10010:
            return "LICENSE_DOWNLOAD_FAILED"
        elif self.value == -10011:
            return "SELF_TEST_IS_EMPTY"
        elif self.value == -10012:
            return "SIGNAL_LOOKUP_FAILED"
        elif self.value == -10013:
            return "INVALID_MODE_TO_GET_SIGNAL"
        elif self.value == -10014:
            return "UNLICENSED_DEVICE"
        elif self.value == -10015:
            return "INVALID_SIZE"
        elif self.value == -10016:
            return "INVALID_LICENSE_RESPONSE"
        elif self.value == -10017:
            return "INVALID_CONTEXT"
        elif self.value == -10018:
            return "INTERNAL_ERROR"
        elif self.value == -10019:
            return "DEVICE_RESPONSE_INCORRECT"
        elif self.value == -10020:
            return "ERROR_POLLING_FOR_DEVICES"
        elif self.value == -10021:
            return "COULD_NOT_RETRIEVEV6_FIRMWARE"
        elif self.value == -10022:
            return "COULD_NOT_DECODE_DEVICE_FIRMWARE"
        elif self.value == -10023:
            return "INVALID_IDTO_FOLLOW"
        elif self.value == -10024:
            return "USING_PRO_FEATURE_ON_UNLICENSED_DEVICE"
        elif self.value == -10025:
            return "FIRMWARE_TOO_NEW"
        elif self.value == -10026:
            return "COULD_NOT_SERIALIZE"
        elif self.value == -10027:
            return "MECHANISM_FAULTED"
        elif self.value == -10028:
            return "FIRMWARE_VERS_NOT_COMPATIBLE"
        elif self.value == -10029:
            return "DIRECTORY_MISSING"
        elif self.value == -10030:
            return "API_TOO_OLD"
        elif self.value == -10031:
            return "LOGGER_NOT_RUNNING"
        elif self.value == -10032:
            return "TIMEOUT_CANNOT_BE_ZERO"
        elif self.value == -10033:
            return "CANNOT_LICENSE_WHILE_ENABLED"
        elif self.value == -10034:
            return "INVALID_FILE"
        elif self.value == -10035:
            return "HOOT_LOG_TOO_OLD"
        elif self.value == -10036:
            return "HOOT_LOG_TOO_NEW"
        elif self.value == -10037:
            return "UNLICENSED_HOOT_LOG"
        elif self.value == -10038:
            return "CANNOT_STEP_WHILE_UNPAUSED"
        elif self.value == -10039:
            return "MULTIPLE_REPLAY_NOT_SUPPORTED"
        elif self.value == -10040:
            return "USER_SIGNAL_LIMIT_EXCEEDED"
        elif self.value == -10041:
            return "INVALID_DEVICE_MODEL"
        else:
            return f"Status Code {self.value}"

    @property
    def description(self) -> str:
        """
        Gets the description of this StatusCode.

        :returns: Description of this StatusCode
        :rtype: str
        """
        if False:
            pass
        elif self.value == 0:
            return "No Error"
        elif self.value == -100:
            return "Diagnostic Server is busy with another command."
        elif self.value == -101:
            return "InvalidDeviceSpec"
        elif self.value == -102:
            return "Device is not present. Verify the device is connected and powered, and that the CAN bus is terminated."
        elif self.value == -103:
            return "Could not put the device into bootloader mode."
        elif self.value == -104:
            return "Could not confirm the device has entered the bootloader."
        elif self.value == -105:
            return "Could not erase flash."
        elif self.value == -106:
            return "Could not field upgrade the device."
        elif self.value == -107:
            return "Bootloader could not verify integrity of the flashed application."
        elif self.value == -108:
            return "Could not run the device firmware application."
        elif self.value == -109:
            return "Unable to set ID to this device."
        elif self.value == -110:
            return "Could not verify that the changed ID took effect."
        elif self.value == -111:
            return "Device field upgrade was successful."
        elif self.value == -112:
            return "Device firmware application is too old."
        elif self.value == -113:
            return "Unable to set name to this device."
        elif self.value == -114:
            return "CompileSzIsWrong"
        elif self.value == -115:
            return "Cannot set the ID of a gadgeteer device."
        elif self.value == -116:
            return "This diagnostic action is not supported."
        elif self.value == -117:
            return "Not Implemented, check latest installer."
        elif self.value == -118:
            return "NoDevicesOnBus"
        elif self.value == -119:
            return "MoreThanOneFile"
        elif self.value == -120:
            return "Specified device was not found. Verify the device is connected and powered, and that the CAN bus is terminated."
        elif self.value == -121:
            return "InvalidDeviceDescriptor"
        elif self.value == -123:
            return "CouldNotSendCanFrame"
        elif self.value == -124:
            return "NormalModeMsgNotPresent"
        elif self.value == -125:
            return "This feature is not supported."
        elif self.value == -126:
            return "The diagnostic server is not field upgrading any devices."
        elif self.value == -127:
            return "CorruptedPOST"
        elif self.value == -128:
            return "This device did not report any available configs. Verify firmware and diagnostics are up-to-date."
        elif self.value == -129:
            return "ConfigFailed"
        elif self.value == -130:
            return "Unable to factory default this device."
        elif self.value == -131:
            return "CustomNameNotSupported"
        elif self.value == -132:
            return "The configs read from the device do not match the configs that were written."
        elif self.value == -133:
            return "Could not apply the device configs."
        elif self.value == -134:
            return "InsufficientSz"
        elif self.value == -135:
            return "This feature is not supported for this device model."
        elif self.value == -140:
            return "CouldNotReqDevInfo"
        elif self.value == -141:
            return "This device does not support new controls."
        elif self.value == -142:
            return "DeviceIsNull"
        elif self.value == -143:
            return "DeviceDidNotRespondToDiagReq"
        elif self.value == -144:
            return "This feature requires Tuner X."
        elif self.value == -145:
            return "Command-line issue with caniv."
        elif self.value == -200:
            return "InvalidCrfBadHeader"
        elif self.value == -201:
            return "InvalidCrfFileSzInvald"
        elif self.value == -202:
            return "Specified CRF is for the wrong product."
        elif self.value == -203:
            return "InvalidCrfNoSects"
        elif self.value == -204:
            return "InvalidCrfBadSectHeader"
        elif self.value == -205:
            return "InvalidCrfBadSectSize"
        elif self.value == -206:
            return "Specified CRF file could not be found."
        elif self.value == -300:
            return "CouldNotFindDynamicId"
        elif self.value == -301:
            return "DidNotGetDhcp"
        elif self.value == -302:
            return "DidNotGetFullDhcp"
        elif self.value == -350:
            return "InvalidLicenseResp"
        elif self.value == -351:
            return "InvalidCanivCache"
        elif self.value == -500:
            return "CannotOpenSerialPort"
        elif self.value == -501:
            return "CannotWriteSerialPort"
        elif self.value == -502:
            return "CannotReadSerialPort"
        elif self.value == -503:
            return "CannotSerialToDevice"
        elif self.value == -504:
            return "NoSerialControlFrameResp"
        elif self.value == -600:
            return "CannotOpenUdpPort"
        elif self.value == -601:
            return "CannotWriteUdpPort"
        elif self.value == -602:
            return "CannotReadUdpPort"
        elif self.value == -603:
            return "CannotUdpToDevice"
        elif self.value == -604:
            return "NoUdpControlFrameResp"
        elif self.value == -605:
            return "TimeoutIso15Response"
        elif self.value == -700:
            return "InvalidJson"
        elif self.value == -800:
            return "The user application is shutting down."
        elif self.value == 1000:
            return "CAN message is stale, data is valid but old. Check the CAN bus wiring, CAN bus utilization, and power to the device."
        elif self.value == 1006:
            return "Buffer is full, cannot insert more data."
        elif self.value == 1010:
            return "PulseWidthSensorNotPresent"
        elif self.value == 1100:
            return "General Warning Occurred."
        elif self.value == 1103:
            return "Firm Vers could not be retrieved. Use Phoenix Tuner X to check ID and firmware(CRF) version."
        elif self.value == 1104:
            return "This feature will be supported in a future update."
        elif self.value == 1105:
            return "The control mode is not valid for this function."
        elif self.value == 1106:
            return "This control mode is not supported yet.  A future release will supported this soon."
        elif self.value == 1109:
            return "Motor Controller must have >= 3.2 firmware for motion profile control mode."
        elif self.value == 1110:
            return "Motor Controller must have >= 3.4 firmware for advanced PID0/PID1 features."
        elif self.value == 1200:
            return "SimDeviceNotFound"
        elif self.value == 1201:
            return "SimPhysicsTypeNotSupported"
        elif self.value == 1202:
            return "SimDeviceAlreadyExists"
        elif self.value == -1001:
            return "Could not transmit CAN Frame."
        elif self.value == -1002:
            return "An invalid argument was passed into the function/VI, such as a null pointer."
        elif self.value == -1003:
            return "CAN frame not received/too-stale. Check the CAN bus wiring, CAN bus utilization, and power to the device."
        elif self.value == -1004:
            return "CAN Transmit timed out."
        elif self.value == -1005:
            return "ArbID is incorrect."
        elif self.value == -1006:
            return "CanOverflowed"
        elif self.value == -1007:
            return "Sensor Not Present."
        elif self.value == -1008:
            return "Firmware Too Old.  Use Phoenix Tuner X to field upgrade your CTRE CAN device firmware(CRF).  Then restart your robot application to clear this error."
        elif self.value == -1009:
            return "Control Frame Period could not be changed.  Most likely it is not being transmitted."
        elif self.value == -1010:
            return "BufferFailure"
        elif self.value == -1011:
            return "Firmware is legacy non-FRC version.  Use Phoenix Tuner X to field upgrade your CTRE CAN device firmware(CRF).  Firmware greater than 20.0 required."
        elif self.value == -1100:
            return "General Error Occurred."
        elif self.value == -1200:
            return "No new response to update signal."
        elif self.value == -1201:
            return "NotAllPIDValuesUpdated"
        elif self.value == -1300:
            return "GEN_PORT_ERROR"
        elif self.value == -1301:
            return "PORT_MODULE_TYPE_MISMATCH"
        elif self.value == -1400:
            return "GEN_MODULE_ERROR"
        elif self.value == -1401:
            return "MODULE_NOT_INIT_SET_ERROR"
        elif self.value == -1402:
            return "MODULE_NOT_INIT_GET_ERROR"
        elif self.value == -1500:
            return "Wheel Radius is too small, cannot get distance traveled."
        elif self.value == -1501:
            return "Ticks per revolution is 0, cannot get heading."
        elif self.value == -1502:
            return "Distance between wheels is too small, cannot get heading."
        elif self.value == -1503:
            return "GainsAreNotSet"
        elif self.value == -1504:
            return "Use RemoteLimitSwitchSource instead of LimitSwitchSource."
        elif self.value == -1505:
            return "Motor Controller Voltage Compensation should not be used with setVoltage().  This causes compensation to happen twice.  Disable Voltage Compensation by calling enableVoltageCompensation(false) in order to use setVoltage()."
        elif self.value == -1506:
            return "CANdleAnimSlotOutOfBounds"
        elif self.value == -1600:
            return "IncompatibleMode"
        elif self.value == -1601:
            return "Handle passed into function is incorrect."
        elif self.value == -1700:
            return "Features requires newer firmware version."
        elif self.value == -1702:
            return "Config factory default features require firmware >=3.10."
        elif self.value == -1703:
            return "Config Motion S Curve Strength features require firmware >=4.16."
        elif self.value == -1704:
            return "Talon FX(Falcon 500) Firmware Too Old.  Use Phoenix Tuner to field upgrade your CTRE CAN device firmware(CRF) to >=20.3. Then restart your robot application to clear this error."
        elif self.value == -1705:
            return "CANdleAnimationsRequireHigherFirm"
        elif self.value == -1800:
            return "LibraryCouldNotBeLoaded"
        elif self.value == -1801:
            return "MissingRoutineInLibrary"
        elif self.value == -1802:
            return "ResourceNotAvailable"
        elif self.value == -1900:
            return "Could not find music file specified, try specifying an absolute path."
        elif self.value == -1901:
            return "Music file size is incorrect, could not parse correctly. Ensure you're using Tuner to generate file."
        elif self.value == -1902:
            return "Music file version is too new, update Phoenix to utilize this file."
        elif self.value == -1903:
            return "Music file is invalid. Ensure you're using Tuner to generate file."
        elif self.value == -1904:
            return "An invalid orchestra action occurred. Ensure a music file is loaded."
        elif self.value == -1905:
            return "This music file version is too old. Regenerate file using Tuner."
        elif self.value == -1906:
            return "Music interrupted due to one of the instruments being commanded a different control mode. Press Play to resume music."
        elif self.value == -1907:
            return "This device doesn't support MusicTone control mode."
        elif self.value == -2000:
            return "kInvalidInterface"
        elif self.value == -2001:
            return "kInvalidGuid"
        elif self.value == -2002:
            return "kInvalidClass"
        elif self.value == -2003:
            return "kInvalidProtocol"
        elif self.value == -2004:
            return "kInvalidPath"
        elif self.value == -2005:
            return "kGeneralWinUsbError"
        elif self.value == -2006:
            return "kFailedSetup"
        elif self.value == -2007:
            return "kListenFailed"
        elif self.value == -2008:
            return "kSendFailed"
        elif self.value == -2009:
            return "kReceiveFailed"
        elif self.value == -2010:
            return "kInvalidRespFormat"
        elif self.value == -2011:
            return "kWinUsbInitFailed"
        elif self.value == -2012:
            return "kWinUsbQueryFailed"
        elif self.value == -2013:
            return "kWinUsbGeneralError"
        elif self.value == -2014:
            return "kAccessDenied"
        elif self.value == -2015:
            return "kFirmwareInvalidResponse"
        elif self.value == -10000:
            return "This StatusCode has not been initialized. Make sure the StatusCode is getting assigned to the return of a method."
        elif self.value == 10000:
            return "WarningNotInitialized"
        elif self.value == 10001:
            return "The timestamp reported by CANivore is at least 10ms older than the timestamp reported by the system, indicating it's fallen out of sync. This does not impact the data of this message, only the timing."
        elif self.value == 10002:
            return "Do not apply or refresh configs periodically, as configs are blocking."
        elif self.value == -10001:
            return "InvalidNetwork"
        elif self.value == -10002:
            return "The CAN bus does not support multi-signal synchronization."
        elif self.value == -10003:
            return "Could not cast from base value to this particular signal's type"
        elif self.value == -10004:
            return "Could not find this value when searching for it"
        elif self.value == -10005:
            return "This is not supported"
        elif self.value == -10006:
            return "Could not determine context from this device hash"
        elif self.value == -10007:
            return "Model name in license file does not match model name of selected device."
        elif self.value == -10008:
            return "Serial Number in license file does not match model name of selected device."
        elif self.value == -10009:
            return "Could not find specified file."
        elif self.value == -10010:
            return "License did not successfully download to Device."
        elif self.value == -10011:
            return "Self Test report does not have any values, is the firmware up to date?"
        elif self.value == -10012:
            return "Failed to lookup signal properties.  This can happen if the fimware is too new and supports signals that older APIs do not support."
        elif self.value == -10013:
            return "The current mode of the device is invalid for getting this signal."
        elif self.value == -10014:
            return "Device is not licensed. Cannot get any data from it."
        elif self.value == -10015:
            return "Size is invalid."
        elif self.value == -10016:
            return "InvalidLicenseResponse"
        elif self.value == -10017:
            return "InvalidContext"
        elif self.value == -10018:
            return "InternalError"
        elif self.value == -10019:
            return "kDeviceResponseIncorrect"
        elif self.value == -10020:
            return "kErrorPollingForDevices"
        elif self.value == -10021:
            return "Device firmware could not be retrieved. Check that the device is running v6 firmware, the device ID is correct, the specified CAN bus is correct, and the device is powered."
        elif self.value == -10022:
            return "Device firmware could not be decoded. Check that the device is running v6 firmware, the device ID is correct, the specified CAN bus is correct, and the device is powered."
        elif self.value == -10023:
            return "The values specified for master are in valid.  Make sure the Device ID of master are correct."
        elif self.value == -10024:
            return "Using a Pro only feature on an unlicensed device. The device may not behave as expected if it continues to operate while unlicensed."
        elif self.value == -10025:
            return "Firmware Too New.  Use Phoenix Tuner X to field upgrade your CTRE CAN device firmware(CRF) to a compatible version.  Then restart your robot application to clear this error."
        elif self.value == -10026:
            return "The data frame could not be serialized for transmit."
        elif self.value == -10027:
            return "The mechanism is disabled due to a fault in one of the devices."
        elif self.value == -10028:
            return "Firmware version is not compatible with this version of Phoenix. Make sure your firmware and API major versions match."
        elif self.value == -10029:
            return "Could not find specified directory."
        elif self.value == -10030:
            return "This API version is too old for the firmware on the device. Either upgrade the API to a newer version or downgrade the device firmware to an older version for correct behavior."
        elif self.value == -10031:
            return "The signal logger is not running. Start the signal logger before writing any signals."
        elif self.value == -10032:
            return "Blocking operations, such as configs, cannot have a timeout of 0. Pass in a non-zero timeout (typically 0.050+ seconds) for normal operation."
        elif self.value == -10033:
            return "Device cannot be licensed while it is control enabled. Disable and neutral the device to apply the licenses."
        elif self.value == -10034:
            return "Could not open or read the given file."
        elif self.value == -10035:
            return "The given hoot log requires an older version of Phoenix API."
        elif self.value == -10036:
            return "The given hoot log requires a newer version of Phoenix API."
        elif self.value == -10037:
            return "Hoot log is not licensed. Cannot get any data from it."
        elif self.value == -10038:
            return "The simulation timing cannot be advanced by a time step while unpaused. Pause the simulator before advancing time."
        elif self.value == -10039:
            return "Hoot replay does not support replaying multiple files. Ensure that only one file is loaded at a time."
        elif self.value == -10040:
            return "The maximum number of loggable user signals has been exceeded. Additional user signals will not be logged."
        elif self.value == -10041:
            return "The provided model was not a valid device type."
        else:
            return f"Status Code {self.value}"
