"""
Contains the timestamp class for methods related to timing
and latency with StatusSignals
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from enum import Enum
from .utils import get_current_time_seconds
from .units import second

class TimestampSource(Enum):
    """
    Source of the timestamp.
    """

    """
    Timestamp as reported by the system.
    This timestamp is captured when the system
    receives the signal value.

    This timestamp is present on all systems and
    is guaranteed to be monotonic
    However, this timestamp is the least accurate
    due to latency from processing delays within
    the system.
    """
    System = (0,)

    """
    Timestamp as reported by the CANivore.
    This timestamp is captured when the CANivore
    receives the signal value.

    The CANivore is synchronized to the system
    monotonic clock and benefits from reduced latency
    over the :attr:System: timestamp.

    When used with CANivore, the only inaccuracy in this
    measurement is latency from CAN bus arbitration.
    """
    CANivore = (1,)
    """
    This timestamp source requires Phoenix Pro.

    Timestamp as reported by the device.
    This timestamp is captured when the device transmits
    the signal value. Because it is timestamped in the
    device, it is the most accurate timestamp source.

    This timestamp is synchronized to the CANivore clock,
    which itself is synchronized to the system monotonic
    clock. As a result, the this timestamp source requires
    a CANivore.

    It can be assumed there is no latency between this timestamp
    and when the data was taken.
    """
    Device = (2,)


class Timestamp:
    """
    Information about the timestamp of a signal.
    """

    def __init__(self, time: second, source: TimestampSource, is_valid: bool = True):
        """
        Construct a new Timestamp for the given source.

        :param time: The time in seconds
        :type time: second
        :param source: The timestamp source
        :type source: TimestampSource
        """
        self.__time: second = time
        self.__source: TimestampSource = source
        self.__valid: bool = is_valid

    def update(self, time: second, source: TimestampSource, valid: bool):
        """
        Update this timestamp with provided information

        :param time: Time in seconds
        :type time: second
        :param source: Timestamp source
        :type source: TimestampSource
        :param valid: Whether the timestamp is valid or not
        :type valid: bool
        """
        self.__time = time
        self.__source = source
        self.__valid = valid

    def get_latency(self) -> second:
        """
        Get the latency of this timestamp compared
        to now

        :return: Difference between now and this timestamp
        :rtype: second
        """
        return get_current_time_seconds() - self.__time

    @property
    def time(self) -> second:
        """
        Get the time of this timestamp

        :return: Time of this timestamp
        :rtype: second
        """
        return self.__time

    @property
    def source(self) -> TimestampSource:
        """
        Get the source of this timestamp

        :return: Source of this timestamp
        :rtype: TimestampSource
        """
        return self.__source

    @property
    def is_valid(self) -> bool:
        """
        Get whether this timestamp is valid or not

        :return: True if this timestamp is valid
        :rtype: bool
        """
        return self.__valid
