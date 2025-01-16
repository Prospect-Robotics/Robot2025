"""
Contains the class for controlling hoot log replay.
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from typing import Generic, TypeVar
from phoenix6.units import second
from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode

T = TypeVar("T")

class HootReplay:
    """
    Static class for controlling Phoenix 6 hoot log replay.

    This replays the given hoot log in simulation. Hoot logs can be
    created by a robot program using SignalLogger. Only one hoot log,
    corresponding to one CAN bus, may be replayed at a time.

    This replays all signals in the given hoot log in simulation. Hoot
    logs can be created by a robot program using SignalLogger. Only one
    hoot log, corresponding to one CAN bus, may be replayed at a time.

    During replay, all transmits from the robot program are ignored.
    This includes features such as control requests, configs, and setting
    signal update frequency. Additionally, Tuner X is not functional
    during log replay.

    To use Hoot Replay, call load_file(str) before any devices are constructed
    to load a hoot file and start replay. Alternatively, the CANBus(str, str)
    constructor can be used when constructing devices.

    After devices are constructed, Hoot Replay can be controlled using play(), pause(), 
    stop(), and restart(). Additionally, Hoot Replay supports step_timing(second) while paused.
    The current file can be closed using close_file(), after which a new file may be loaded.
    """

    @staticmethod
    def load_file(filepath: str) -> StatusCode:
        """
        Loads the given file and starts signal log replay. Only one hoot
        log, corresponding to one CAN bus, may be replayed at a time.

        This must be called before constructing any devices or checking
        CAN bus status. The CANBus(canbus, hoot_filepath) constructor
        can be used when constructing devices to guarantee that this API
        is called first.

        When using relative paths, the file path is typically relative
        to the top-level folder of the robot project.

        This API is blocking on the file read.

        :param filepath: Path and name of the hoot file to load
        :type filepath: str
        :returns: Status of opening and reading the file for replay
        :rtype: StatusCode
        :raises ValueError: The file is invalid, unlicensed, or targets
                            a different version of Phoenix 6
        """
        retval = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_load_file(ctypes.c_char_p(bytes(filepath, 'utf-8'))))
        if (
            retval == StatusCode.INVALID_FILE or
            retval == StatusCode.UNLICENSED_HOOT_LOG or
            retval == StatusCode.HOOT_LOG_TOO_OLD or
            retval == StatusCode.HOOT_LOG_TOO_NEW
        ):
            raise ValueError(retval.description)
        return retval

    @staticmethod
    def close_file():
        """
        Ends the hoot log replay. This stops the replay if it is running,
        closes the hoot log, and clears all signals read from the file.
        """
        Native.instance().c_ctre_phoenix6_platform_replay_close_file()

    @staticmethod
    def is_file_loaded() -> bool:
        """
        Gets whether a valid hoot log file is currently loaded.

        :returns: True if a valid hoot log file is loaded
        :rtype: bool
        """
        return Native.instance().c_ctre_phoenix6_platform_replay_is_file_loaded()

    @staticmethod
    def play() -> StatusCode:
        """
        Starts or resumes the hoot log replay.

        :returns: Status of starting or resuming replay
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_play())

    @staticmethod
    def pause() -> StatusCode:
        """
        Pauses the hoot log replay. This maintains the current position
        in the log replay so it can be resumed later.

        :returns: Status of pausing replay
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_pause())

    @staticmethod
    def stop() -> StatusCode:
        """
        Stops the hoot log replay. This resets the current position in
        the log replay to the start.

        :returns: Status of stopping replay
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_stop())

    @classmethod
    def restart(clazz) -> StatusCode:
        """
        Restarts the hoot log replay from the start of the log.
        This is equivalent to calling stop() followed by play().

        :returns: Status of restarting replay
        :rtype: StatusCode
        """
        retval = clazz.stop()
        if retval.is_ok():
            retval = clazz.play()
        return retval

    @classmethod
    def is_playing(clazz) -> bool:
        """
        Gets whether hoot log replay is actively playing.

        This API will return true in programs that do not support
        replay, making it safe to call without first checking if
        the program supports replay.

        :returns: True if replay is playing back signals
        :rtype: bool
        """
        return clazz.wait_for_playing(0.0)

    @staticmethod
    def wait_for_playing(timeout: second) -> bool:
        """
        Waits until hoot log replay is actively playing.

        This API will immediately return true in programs that do
        not support replay, making it safe to call without first
        checking if the program supports replay.

        Since this can block the calling thread, this should not
        be called with a non-zero timeout on the main thread.

        This can also be used with a timeout of 0 to perform
        a non-blocking check, which is equivalent to is_playing().

        :param timeout: Max time to wait for replay to start playing
        :type timeout: second
        :returns: True if replay is playing back signals
        :rtype: bool
        """
        return Native.instance().c_ctre_phoenix6_platform_replay_is_running(int(timeout * 1000.0))

    @staticmethod
    def set_speed(speed: float):
        """
        Sets the speed of the hoot log replay. A speed of 1.0 corresponds
        to replaying the file in real time, and larger values increase
        the speed.

            - Minimum Value: 0.01
            - Maximum Value: 100.0
            - Default Value: 1.0

        :param speed: Speed of the hoot log replay
        :type speed: float
        """
        Native.instance().c_ctre_phoenix6_platform_replay_set_speed(speed)

    @staticmethod
    def step_timing(step_time_seconds: second) -> StatusCode:
        """
        Advances the hoot log replay time by the given value. Replay must
        be paused or stopped before advancing its time.

        :param step_time_seconds: The amount of time to advance
        :type step_time_seconds: second
        :returns: Status of advancing the replay time
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_step_timing(step_time_seconds))

    class SignalData(Generic[T]):
        """
        Stores information about a user signal from replay.
        """

        def __init__(self):
            self.name: str = ""
            """The name of the signal"""

            self.units: str = ""
            """The units of the signal"""

            self.timestamp: second = 0
            """The timestamp of the signal, in seconds"""

            self.status: StatusCode = StatusCode.OK
            """Status code response of getting the signal"""

            self.value: T = None
            """The value of the signal"""

    @classmethod
    def get_raw(clazz, name: str) -> SignalData[bytearray]:
        """
        Gets a raw-bytes user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[bytearray]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        data = (ctypes.c_uint8 * 64)()
        len = ctypes.c_uint8()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_raw(name_cstr, ctypes.byref(units), data, ctypes.byref(len), ctypes.byref(timestamp)))

        sig = clazz.SignalData[bytearray]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = bytearray(data)[:len.value]

        return sig

    @classmethod
    def get_boolean(clazz, name: str) -> SignalData[bool]:
        """
        Gets a boolean user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[bool]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        value = ctypes.c_bool()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_boolean(name_cstr, ctypes.byref(units), ctypes.byref(value), ctypes.byref(timestamp)))

        sig = clazz.SignalData[bool]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = value

        return sig

    @classmethod
    def get_integer(clazz, name: str) -> SignalData[int]:
        """
        Gets an integer user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[int]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        value = ctypes.c_int64()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_integer(name_cstr, ctypes.byref(units), ctypes.byref(value), ctypes.byref(timestamp)))

        sig = clazz.SignalData[int]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = value

        return sig

    @classmethod
    def get_float(clazz, name: str) -> SignalData[float]:
        """
        Gets a float user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[float]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        value = ctypes.c_float()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_float(name_cstr, ctypes.byref(units), ctypes.byref(value), ctypes.byref(timestamp)))

        sig = clazz.SignalData[float]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = value

        return sig

    @classmethod
    def get_double(clazz, name: str) -> SignalData[float]:
        """
        Gets a double user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[float]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        value = ctypes.c_double()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_double(name_cstr, ctypes.byref(units), ctypes.byref(value), ctypes.byref(timestamp)))

        sig = clazz.SignalData[float]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = value

        return sig

    @classmethod
    def get_string(clazz, name: str) -> SignalData[str]:
        """
        Gets a string user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[str]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        value = (ctypes.c_char * 65)()
        len = ctypes.c_uint8()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_string(name_cstr, ctypes.byref(units), value, ctypes.byref(len), ctypes.byref(timestamp)))

        sig = clazz.SignalData[str]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = str(value.value, encoding='utf-8')[:len.value]

        return sig

    @classmethod
    def get_boolean_array(clazz, name: str) -> SignalData[list[bool]]:
        """
        Gets a boolean array user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[list[bool]]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        values = (ctypes.c_bool * 64)()
        count = ctypes.c_uint8()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_boolean_array(name_cstr, ctypes.byref(units), values, ctypes.byref(count), ctypes.byref(timestamp)))

        sig = clazz.SignalData[list[bool]]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = values[:count.value]

        return sig

    @classmethod
    def get_integer_array(clazz, name: str) -> SignalData[list[int]]:
        """
        Gets an integer array user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[list[int]]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        values = (ctypes.c_int64 * 8)()
        count = ctypes.c_uint8()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_integer_array(name_cstr, ctypes.byref(units), values, ctypes.byref(count), ctypes.byref(timestamp)))

        sig = clazz.SignalData[list[int]]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = values[:count.value]

        return sig

    @classmethod
    def get_float_array(clazz, name: str) -> SignalData[list[float]]:
        """
        Gets a float array user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[list[float]]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        values = (ctypes.c_float * 16)()
        count = ctypes.c_uint8()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_float_array(name_cstr, ctypes.byref(units), values, ctypes.byref(count), ctypes.byref(timestamp)))

        sig = clazz.SignalData[list[float]]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = values[:count.value]

        return sig

    @classmethod
    def get_double_array(clazz, name: str) -> SignalData[list[float]]:
        """
        Gets a double array user signal.

        :param name: Name of the signal
        :type name: str
        :returns: Structure with all information about the signal
        :rtype: SignalData[list[float]]
        """
        name_cstr = ctypes.c_char_p(bytes(name, 'utf-8'))
        units = ctypes.c_char_p()
        values = (ctypes.c_double * 8)()
        count = ctypes.c_uint8()
        timestamp = ctypes.c_double()
        status = StatusCode(Native.instance().c_ctre_phoenix6_platform_replay_get_double_array(name_cstr, ctypes.byref(units), values, ctypes.byref(count), ctypes.byref(timestamp)))

        sig = clazz.SignalData[list[float]]()
        sig.name = name
        if units.value is not None:
            sig.units = str(units.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(units))
        sig.timestamp = timestamp
        sig.status = status
        sig.value = values[:count.value]

        return sig
