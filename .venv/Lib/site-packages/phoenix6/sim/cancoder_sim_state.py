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
from phoenix6.signals.spn_enums import MagnetHealthValue
from phoenix6.sim.chassis_reference import ChassisReference
from phoenix6.sim.device_type import DeviceType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from phoenix6.hardware.core.core_cancoder import CoreCANcoder

class CANcoderSimState:
    """
    Creates an object to control the state of a simulated CANcoder.

    Note the recommended method of accessing simulation features is
    to use CANcoder.sim_state.

    :param device: Device to which this simulation state is attached
    :type device: CoreCANcoder
    :param orientation: Orientation of the device relative to the robot chassis
    :type orientation: ChassisReference
    """

    __device_type = DeviceType.P6_CANcoderType

    def __init__(self, device: 'CoreCANcoder', orientation: ChassisReference = ChassisReference.CounterClockwise_Positive):
        self._id = device.device_id

        self.orientation = orientation
        """
        The orientation of the CANcoder relative to the robot chassis.

        This value should not be changed based on the CANcoder invert.
        Rather, this value should be changed when the mechanical linkage
        between the CANcoder and the robot changes.
        """

    def set_supply_voltage(self, volts: volt) -> StatusCode:
        """
        Sets the simulated supply voltage of the CANcoder.

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

    def set_raw_position(self, rotations: rotation) -> StatusCode:
        """
        Sets the simulated raw position of the CANcoder.

        Inputs to this function over time should be continuous, as user calls of
        CANcoder.set_position will be accounted for in the callee.

        The CANcoder integrates this to calculate the true reported position.

        When using the WPI Sim GUI, you will notice a readonly position and settable rawPositionInput.
        The readonly signal is the emulated position which will match self-test in Tuner and the hardware API.
        Changes to rawPositionInput will be integrated into the emulated position.
        This way a simulator can modify the position without overriding hardware API calls for home-ing the sensor.

        :param rotations: The raw position in rotations
        :type rotations: rotation
        :returns: Status code
        :rtype: StatusCode
        """
        if self.orientation == ChassisReference.Clockwise_Positive:
            rotations = -rotations
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"RawPosition"), rotations)
        )

    def add_position(self, drotations: rotation) -> StatusCode:
        """
        Adds to the simulated position of the CANcoder.

        :param drotations: The change in position in rotations
        :type drotations: rotation
        :returns: Status code
        :rtype: StatusCode
        """
        if self.orientation == ChassisReference.Clockwise_Positive:
            drotations = -drotations
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"AddPosition"), drotations)
        )

    def set_velocity(self, rps: rotations_per_second) -> StatusCode:
        """
        Sets the simulated velocity of the CANcoder.

        :param rps: The new velocity in rotations per second
        :type rps: rotations_per_second
        :returns: Status code
        :rtype: StatusCode
        """
        if self.orientation == ChassisReference.Clockwise_Positive:
            rps = -rps
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"Velocity"), rps)
        )

    def set_magnet_health(self, value: MagnetHealthValue) -> StatusCode:
        """
        Sets the simulated magnet health of the CANcoder.

        :param value:   The magnet health to simulate. This directly correlates to the
                        red/green/orange state of the simulated LED.
        :type value: MagnetHealthValue
        :returns: Status code
        :rtype: StatusCode
        """
        return StatusCode(
            Native.instance().c_ctre_phoenix6_platform_sim_set_physics_input(self.__device_type.value, self._id, ctypes.c_char_p(b"MagnetHealth"), value.value)
        )
