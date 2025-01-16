"""
Contains the class for controlling the signal logger.
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from phoenix6.units import second
from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode

class SignalLogger:
    """
    Static class for controlling the Phoenix 6 signal logger.

    This logs all the signals from the CAN buses into .hoot files.
    Each file name starts with the CANivore serial number or "rio"
    for the roboRIO CAN bus, followed by the timestamp. In the
    header of a hoot file, the CANivore name and firmware version
    are logged in plain text.

    During an FRC match, the log file will be renamed to include the
    event name, match type, and match number at the start of the file
    name. The match type will be 'P' for practice matches, 'Q' for
    qualification matches, and 'E' for elimination matches.
    """

    @staticmethod
    def set_path(path: str) -> StatusCode:
        """
        Sets the destination for logging, restarting logger if
        the path changed.

        If this is not called or the path is left empty, the default
        path will be used. The default path on the roboRIO is a logs
        folder on the first USB flash drive found, or /home/lvuser/logs
        if none is available. The default path on all other platforms
        is a logs folder in the current working directory.

        Typical use for this routine is to use a removable USB flash
        drive for logging.

        :param path: Folder path for the log files; path must exist
        :type path: str
        :returns: Status of setting the path and restarting the log
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_set_logger_path(ctypes.c_char_p(bytes(path, 'utf-8'))))

    @staticmethod
    def start() -> StatusCode:
        """
        Starts logging status signals. Starts regardless of auto
        logging status.

        If using a roboRIO 1, we recommend setting the logging path
        to an external drive using SetPath to avoid running out of
        internal storage space.

        If auto logging is enabled, the log will be stopped at the
        end of the match.

        :returns: Status of starting the logger
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_start_logger())

    @staticmethod
    def stop() -> StatusCode:
        """
        Stops logging status signals. Stops regardless of auto
        logging status.

        :returns: Status of stopping the logger
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_stop_logger())

    @staticmethod
    def enable_auto_logging(enable: bool) -> StatusCode:
        """
        Enables or disables auto logging.

        Auto logging is only supported on the roboRIO. When auto
        logging is enabled, logging is started at the beginning
        of an FRC match and stopped at the end.

        :param enable: Whether to enable auto logging
        :type enable: bool
        :returns: Status of auto logging enable/disable
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_enable_auto_logging(enable))

    @staticmethod
    def write_raw(name: str, data: bytes, size: int, latency_seconds: second = 0) -> StatusCode:
        """
        Writes the raw data bytes to the log file. The data cannot
        exceed 64 bytes.

        :param name: Name of the signal
        :type name: str
        :param data: Raw data bytes
        :type data: bytes
        :param size: Size of the raw data (in bytes)
        :type size: int
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        if size > 64:
            return StatusCode.INVALID_SIZE

        name_bytes = bytes(name, 'utf-8')
        # We can't create a const c_uint8 pointer directly from bytes,
        # but we can safely cast a c_char_p to a c_uint8 pointer.
        cdata = ctypes.cast(ctypes.c_char_p(data), ctypes.POINTER(ctypes.c_uint8))
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_raw(ctypes.c_char_p(name_bytes), cdata, size, latency_seconds))

    @staticmethod
    def write_boolean(name: str, value: bool, latency_seconds: second = 0) -> StatusCode:
        """
        Writes the boolean to the log file.

        :param name: Name of the signal
        :type name: str
        :param value: Value to write
        :type data: bool
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        name_bytes = bytes(name, 'utf-8')
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_boolean(ctypes.c_char_p(name_bytes), value, latency_seconds))

    @staticmethod
    def write_integer(name: str, value: int, units: str = "", latency_seconds: second = 0) -> StatusCode:
        """
        Writes the integer to the log file.

        :param name: Name of the signal
        :type name: str
        :param value: Value to write
        :type data: int
        :param units: Units of the signal
        :type units: str
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        name_bytes = bytes(name, 'utf-8')
        units_bytes = bytes(units, 'utf-8')
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_integer(ctypes.c_char_p(name_bytes), value, ctypes.c_char_p(units_bytes), latency_seconds))

    @staticmethod
    def write_float(name: str, value: float, units: str = "", latency_seconds: second = 0) -> StatusCode:
        """
        Writes the float to the log file.

        :param name: Name of the signal
        :type name: str
        :param value: Value to write
        :type data: float
        :param units: Units of the signal
        :type units: str
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        name_bytes = bytes(name, 'utf-8')
        units_bytes = bytes(units, 'utf-8')
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_float(ctypes.c_char_p(name_bytes), ctypes.c_float(value), ctypes.c_char_p(units_bytes), latency_seconds))

    @staticmethod
    def write_double(name: str, value: float, units: str = "", latency_seconds: second = 0) -> StatusCode:
        """
        Writes the double to the log file.

        :param name: Name of the signal
        :type name: str
        :param value: Value to write
        :type data: float
        :param units: Units of the signal
        :type units: str
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        name_bytes = bytes(name, 'utf-8')
        units_bytes = bytes(units, 'utf-8')
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_double(ctypes.c_char_p(name_bytes), ctypes.c_double(value), ctypes.c_char_p(units_bytes), latency_seconds))

    @staticmethod
    def write_string(name: str, value: str, latency_seconds: second = 0) -> StatusCode:
        """
        Writes the string to the log file. The string cannot
        exceed 64 characters.

        :param name: Name of the signal
        :type name: str
        :param value: Value to write
        :type data: bool
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        if len(value) > 64:
            return StatusCode.INVALID_SIZE

        name_bytes = bytes(name, 'utf-8')
        value_bytes = bytes(value, 'utf-8')
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_string(ctypes.c_char_p(name_bytes), ctypes.c_char_p(value_bytes), latency_seconds))

    @staticmethod
    def write_boolean_array(name: str, value: list[bool], latency_seconds: second = 0) -> StatusCode:
        """
        Writes the array of booleans to the log file. The array
        cannot exceed 64 elements.

        :param name: Name of the signal
        :type name: str
        :param value: Array of values to write
        :type data: list[bool]
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        count = len(value)
        if count > 64:
            return StatusCode.INVALID_SIZE

        name_bytes = bytes(name, 'utf-8')
        cvalue = (ctypes.c_bool * count)(*value)
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_boolean_array(ctypes.c_char_p(name_bytes), cvalue, count, latency_seconds))

    @staticmethod
    def write_integer_array(name: str, value: list[int], units: str = "", latency_seconds: second = 0) -> StatusCode:
        """
        Writes the array of integers to the log file. The array
        cannot exceed 8 elements.

        :param name: Name of the signal
        :type name: str
        :param value: Array of values to write
        :type data: list[int]
        :param units: Units of the signal
        :type units: str
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        count = len(value)
        if count > 8:
            return StatusCode.INVALID_SIZE

        name_bytes = bytes(name, 'utf-8')
        units_bytes = bytes(units, 'utf-8')
        cvalue = (ctypes.c_int64 * count)(*value)
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_integer_array(ctypes.c_char_p(name_bytes), cvalue, count, ctypes.c_char_p(units_bytes), latency_seconds))

    @staticmethod
    def write_float_array(name: str, value: list[float], units: str = "", latency_seconds: second = 0) -> StatusCode:
        """
        Writes the array of floats to the log file. The array
        cannot exceed 16 elements.

        :param name: Name of the signal
        :type name: str
        :param value: Array of values to write
        :type data: list[float]
        :param units: Units of the signal
        :type units: str
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        count = len(value)
        if count > 16:
            return StatusCode.INVALID_SIZE

        name_bytes = bytes(name, 'utf-8')
        units_bytes = bytes(units, 'utf-8')
        cvalue = (ctypes.c_float * count)(*value)
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_float_array(ctypes.c_char_p(name_bytes), cvalue, count, ctypes.c_char_p(units_bytes), latency_seconds))

    @staticmethod
    def write_double_array(name: str, value: list[float], units: str = "", latency_seconds: second = 0) -> StatusCode:
        """
        Writes the array of doubles to the log file. The array
        cannot exceed 8 elements.

        :param name: Name of the signal
        :type name: str
        :param value: Array of values to write
        :type data: list[float]
        :param units: Units of the signal
        :type units: str
        :param latency_seconds: Latency of the signal in seconds;
                                this value is subtracted from the
                                current time to get the timestamp
                                written to the log
        :type latency_seconds: second
        :returns: Status of writing the data
        :rtype: StatusCode
        """
        count = len(value)
        if count > 8:
            return StatusCode.INVALID_SIZE

        name_bytes = bytes(name, 'utf-8')
        units_bytes = bytes(units, 'utf-8')
        cvalue = (ctypes.c_double * count)(*value)
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_write_double_array(ctypes.c_char_p(name_bytes), cvalue, count, ctypes.c_char_p(units_bytes), latency_seconds))
