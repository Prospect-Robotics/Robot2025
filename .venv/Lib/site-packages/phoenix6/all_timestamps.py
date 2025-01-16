"""
A collection of timestamps, including system and CANivore timestamp
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.timestamp import Timestamp, TimestampSource
from phoenix6.units import second

class AllTimestamps:
    """
    A collection of timestamps for a received signal.
    """

    def __init__(self):
        """
        Constructs a new AllTimestamps object.
        """
        self.__system_timestamp = Timestamp(0, TimestampSource.System, False)
        self.__canivore_timestamp = Timestamp(0, TimestampSource.CANivore, False)
        self.__device_timestamp = Timestamp(0, TimestampSource.Device, False)

    def update(
        self,
        system_timestamp_seconds: second,
        system_timestamp_source: TimestampSource,
        system_timestamp_valid: bool,
        canivore_timestamp_seconds: second,
        canivore_timestamp_source: TimestampSource,
        canivore_timestamp_valid: bool,
        device_timestamp_seconds: second,
        device_timestamp_source: TimestampSource,
        device_timestamp_valid: bool,
    ):
        """
        Update this timestamp with the new timestamps

        :param system_timestamp_seconds: New system timestamp seconds
        :type system_timestamp_seconds: second
        :param system_timestamp_source: New System timestamp source
        :type system_timestamp_source: TimestampSource
        :param system_timestamp_valid: Whether new System timestamp is valid
        :type system_timestamp_valid: bool
        :param canivore_timestamp_seconds: New CANivore timestamp seconds
        :type canivore_timestamp_seconds: second
        :param canivore_timestamp_source: New CANivore timestamp source
        :type canivore_timestamp_source: TimestampSource
        :param canivore_timestamp_valid: Whether new CANivore timestamp is valid
        :type canivore_timestamp_valid: bool
        :param device_timestamp_seconds: New Device timestamp seconds
        :type device_timestamp_seconds: second
        :param device_timestamp_source: New Device timestamp source
        :type device_timestamp_source: TimestampSource
        :param device_timestamp_valid: Whether new Device timestamp is valid
        :type device_timestamp_valid: bool
        """
        self.__system_timestamp = Timestamp(
            system_timestamp_seconds, system_timestamp_source, system_timestamp_valid
        )
        self.__canivore_timestamp = Timestamp(
            canivore_timestamp_seconds,
            canivore_timestamp_source,
            canivore_timestamp_valid,
        )
        self.__device_timestamp = Timestamp(
            device_timestamp_seconds, device_timestamp_source, device_timestamp_valid
        )

    def get_best_timestamp(self) -> Timestamp:
        """
        Gets the most accurate timestamp available.

        The timestamp sources from most to least accurate are:

            - TimestampSource.Device
            - TimestampSource.CANivore
            - TimestampSource.System

        Note that some of these sources may not be available.

        :return: The most accurate timestamp available
        :rtype: Timestamp
        """
        if self.__device_timestamp.is_valid:
            return self.__device_timestamp
        if self.__canivore_timestamp.is_valid:
            return self.__canivore_timestamp
        return self.__system_timestamp

    def get_system_timestamp(self) -> Timestamp:
        """
        Get the timestamp as reported by the TimestampSource.System source.

        :return: Timestamp as reported by system
        :rtype: Timestamp
        """
        return self.__system_timestamp

    def get_canivore_timestamp(self) -> Timestamp:
        """
        Get the timestamp as reported by the TimestampSource.CANivore source.

        :return: Timestamp as reported by the CANivore
        :rtype: Timestamp
        """
        return self.__canivore_timestamp

    def get_device_timestamp(self) -> Timestamp:
        """
        Get the timestamp as reported by the TimestampSource.Device source.

        :return: Timestamp as reported by the device
        :rtype: Timestamp
        """
        return self.__device_timestamp
