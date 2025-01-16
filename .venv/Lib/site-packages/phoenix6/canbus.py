"""
Contains the class for getting information about a CAN bus.
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from phoenix6.hoot_replay import HootReplay
from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode

class CANBusStatus:
    """
    Contains status information about a CAN bus.
    """

    def __init__(self):
        self.status: StatusCode = StatusCode.OK
        """
        Status code response of getting the data
        """

        self.bus_utilization: float = 0
        """
        CAN bus utilization, from 0.0 to 1.0
        """

        self.bus_off_count: int = 0
        """
        Bus off count
        """

        self.tx_full_count: int = 0
        """
        Transmit buffer full count
        """

        self.rec: int = 0
        """
        Receive Error Counter (REC)
        """

        self.tec: int = 0
        """
        Transmit Error Counter (TEC)
        """

class CANBus:
    """
    Class for getting information about an available CAN bus.

    A CANBus can optionally be constructed with an associated
    hoot file, which loads it for replay (equivalent to calling
    HootReplay.load_file).
    
    Only one hoot log may be replayed at a time, so only one CAN
    bus should be constructed with a hoot file.

    When using relative paths, the file path is typically relative
    to the top-level folder of the robot project.

    :param canbus: Name of the CAN bus. Possible CAN bus strings are:

        - "rio" for the native roboRIO CAN bus
        - CANivore name or serial number
        - SocketCAN interface (non-FRC Linux only)
        - "*" for any CANivore seen by the program
        - empty string (default) to select the default for the system:

            - "rio" on roboRIO
            - "can0" on Linux
            - "*" on Windows

    :type canbus: str, optional
    :param hoot_filepath: Path and name of the hoot file to load
    :type hoot_filepath: str | None, optional
    """

    def __init__(self, canbus: str = "", hoot_filepath: str | None = None):
        self.__name = canbus
        if hoot_filepath is not None:
            HootReplay.load_file(hoot_filepath)

    @property
    def name(self) -> str:
        """
        Get the name used to construct this CAN bus.
        
        :returns: Name of the CAN bus
        :rtype: str
        """
        return self.__name

    def is_network_fd(self) -> bool:
        """
        Gets whether the CAN bus is a CAN FD network.

        :returns: True if the CAN bus is CAN FD
        :rtype: bool
        """
        return Native.instance().c_ctre_phoenix6_platform_canbus_is_network_fd(ctypes.c_char_p(bytes(self.__name, 'utf-8')))

    def get_status(self) -> CANBusStatus:
        """
        Gets the status of the CAN bus, including the bus
        utilization and the error counters.

        This can block for up to 0.001 seconds (1 ms).

        :returns: Status of the CAN bus
        :rtype: CANBusStatus
        """
        canbus_cstr = ctypes.c_char_p(bytes(self.__name, 'utf-8'))

        bus_util_perc = ctypes.c_float()
        bus_off_cnt = ctypes.c_uint32()
        tx_full_cnt = ctypes.c_uint32()
        rec = ctypes.c_uint32()
        tec = ctypes.c_uint32()
        err = Native.instance().c_ctre_phoenix6_platform_canbus_get_status(ctypes.byref(bus_util_perc), ctypes.byref(bus_off_cnt), ctypes.byref(tx_full_cnt), ctypes.byref(rec), ctypes.byref(tec), canbus_cstr, True)

        status = CANBusStatus()
        status.bus_utilization = bus_util_perc.value
        status.bus_off_count = bus_off_cnt.value
        status.tx_full_count = tx_full_cnt.value
        status.rec = rec.value
        status.tec = tec.value

        if err != 0:
            status.status = StatusCode.INVALID_NETWORK
        else:
            status.status = StatusCode.OK

        return status
