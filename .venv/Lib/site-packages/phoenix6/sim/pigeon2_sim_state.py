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
    from phoenix6.hardware.core.core_pigeon2 import CorePigeon2

class Pigeon2SimState:
    """
    Creates an object to control the state of a simulated Pigeon2.

    Note the recommended method of accessing simulation features is
    to use Pigeon2.sim_state.

    :param device: Device to which this simulation state is attached
    :type device: CorePigeon2
    """

    __device_type = DeviceType.P6_Pigeon2Type

    def __init__(self, device: 'CorePigeon2'):
        self._id = device.device_id

    def set_supply_voltage(self, volts: volt) -> StatusCode:
        """
        Sets the simulated supply voltage of the Pigeon2.

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

    def set_raw_yaw(self, deg: degree) -> StatusCode:
        """
        Sets the simulated raw yaw of the Pigeon2.

        Inputs to this function over time should be continuous, as user calls of
        Pigeon2.set_yaw will be accounted for in the callee.

        The Pigeon2 integrates this to calculate the true reported yaw.

        When using the WPI Sim GUI, you will notice a readonly yaw and settable rawYawInput.
        The readonly signal is the emulated yaw which will match self-test in Tuner and the hardware API.
        Changes to rawYawInput will be integrated into the emulated yaw.
        This way a simulator can modify the yaw without overriding hardware API calls for home-ing the sensor.

        :param deg: The yaw in degrees
        :type deg: degree
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"RawYaw"), deg)
        )

    def add_yaw(self, ddeg: degree) -> StatusCode:
        """
        Adds to the simulated yaw of the Pigeon2.

        :param ddeg: The change in position in rotations
        :type ddeg: degree
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"AddYaw"), ddeg)
        )

    def set_pitch(self, deg: degree) -> StatusCode:
        """
        Sets the simulated pitch of the Pigeon2.

        :param deg: The pitch in degrees
        :type deg: degree
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"Pitch"), deg)
        )

    def set_roll(self, deg: degree) -> StatusCode:
        """
        Sets the simulated roll of the Pigeon2.

        :param deg: The roll in degrees
        :type deg: degree
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"Roll"), deg)
        )

    def set_angular_velocity_x(self, dps: degrees_per_second) -> StatusCode:
        """
        Sets the simulated angular velocity X component of the Pigeon2.

        :param dps: The X component of the angular velocity in degrees per second
        :type deg: degrees_per_second
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"AngularVelocityX"), dps)
        )

    def set_angular_velocity_y(self, dps: degrees_per_second) -> StatusCode:
        """
        Sets the simulated angular velocity Y component of the Pigeon2.

        :param dps: The Y component of the angular velocity in degrees per second
        :type deg: degrees_per_second
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"AngularVelocityY"), dps)
        )

    def set_angular_velocity_z(self, dps: degrees_per_second) -> StatusCode:
        """
        Sets the simulated angular velocity Z component of the Pigeon2.

        :param dps: The Z component of the angular velocity in degrees per second
        :type deg: degrees_per_second
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"AngularVelocityZ"), dps)
        )
