"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_code import StatusCode
from phoenix6.phoenix_native import Native
import ctypes
from phoenix6.units import *
from phoenix6.sim.device_type import DeviceType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from phoenix6.hardware.core.core_canrange import CoreCANrange

class CANrangeSimState:
    """
    Creates an object to control the state of a simulated CANrange.

    Note the recommended method of accessing simulation features is
    to use CANrange.sim_state.

    :param device: Device to which this simulation state is attached
    :type device: CoreCANrange
    """

    __device_type = DeviceType.P6_CANrangeType

    def __init__(self, device: 'CoreCANrange'):
        self._id = device.device_id

    def set_supply_voltage(self, volts: volt) -> StatusCode:
        """
        Sets the simulated supply voltage of the CANrange.

        The minimum allowed supply voltage is 4 V - values below this
        will be promoted to 4 V.

        :param volts: The supply voltage in Volts
        :type volts: volt
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"SupplyVoltage"), volts)
        )

    def set_distance(self, meters: meter) -> StatusCode:
        """
        Sets the simulated distance of the CANrange.

        :param meters: The distance in meters
        :type meters: meter
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"Distance"), meters)
        )
