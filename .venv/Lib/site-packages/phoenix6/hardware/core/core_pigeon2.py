"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from typing import overload
from phoenix6.canbus import CANBus
from phoenix6.hardware.parent_device import ParentDevice, SupportsSendRequest
from phoenix6.spns.spn_value import SpnValue
from phoenix6.status_code import StatusCode
from phoenix6.status_signal import *
from phoenix6.units import *
from phoenix6.sim.device_type import DeviceType
from phoenix6.configs.pigeon2_configs import Pigeon2Configurator
from phoenix6.sim.pigeon2_sim_state import Pigeon2SimState

class CorePigeon2(ParentDevice):
    """
    Constructs a new Pigeon 2 sensor object.

    :param device_id: ID of the device, as configured in Phoenix Tuner.
    :type device_id: int
    :param canbus: Name of the CAN bus this device is on. Possible CAN bus strings are:

        - "rio" for the native roboRIO CAN bus
        - CANivore name or serial number
        - SocketCAN interface (non-FRC Linux only)
        - "*" for any CANivore seen by the program
        - empty string (default) to select the default for the system:

            - "rio" on roboRIO
            - "can0" on Linux
            - "*" on Windows

    :type canbus: str | CANBus, optional
    """

    def __init__(self, device_id: int, canbus: str | CANBus = ""):
        if isinstance(canbus, CANBus):
            canbus = canbus.name
        super().__init__(device_id, "pigeon 2", canbus)
        self.configurator = Pigeon2Configurator(self._device_identifier)

        Native.instance().c_ctre_phoenix6_platform_sim_create(DeviceType.P6_Pigeon2Type.value, device_id)
        self.__sim_state = None


    @property
    def sim_state(self) -> Pigeon2SimState:
        """
        Get the simulation state for this device.

        This function reuses an allocated simulation state
        object, so it is safe to call this function multiple
        times in a robot loop.

        :returns: Simulation state
        :rtype: Pigeon2SimState
        """

        if self.__sim_state is None:
            self.__sim_state = Pigeon2SimState(self)
        return self.__sim_state


    def get_version_major(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Major Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionMajor Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_MAJOR.value, None, "version_major", int, False, refresh)
    
    def get_version_minor(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Minor Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionMinor Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_MINOR.value, None, "version_minor", int, False, refresh)
    
    def get_version_bugfix(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Bugfix Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionBugfix Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_BUGFIX.value, None, "version_bugfix", int, False, refresh)
    
    def get_version_build(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Build Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionBuild Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_BUILD.value, None, "version_build", int, False, refresh)
    
    def get_version(self, refresh: bool = True) -> StatusSignal[int]:
        """
        Full Version of firmware in device.  The format is a four byte value.
        
            - Minimum Value: 0
            - Maximum Value: 4294967295
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Version Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.VERSION_FULL.value, None, "version", int, False, refresh)
    
    def get_fault_field(self, refresh: bool = True) -> StatusSignal[int]:
        """
        Integer representing all fault flags reported by the device.
        
        These are device specific and are not used directly in typical
        applications. Use the signal specific GetFault_*() methods instead.
        
            - Minimum Value: 0
            - Maximum Value: 4294967295
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: FaultField Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.ALL_FAULTS.value, None, "fault_field", int, True, refresh)
    
    def get_sticky_fault_field(self, refresh: bool = True) -> StatusSignal[int]:
        """
        Integer representing all (persistent) sticky fault flags reported by
        the device.
        
        These are device specific and are not used directly in typical
        applications. Use the signal specific GetStickyFault_*() methods
        instead.
        
            - Minimum Value: 0
            - Maximum Value: 4294967295
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFaultField Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.ALL_STICKY_FAULTS.value, None, "sticky_fault_field", int, True, refresh)
    
    def get_yaw(self, refresh: bool = True) -> StatusSignal[degree]:
        """
        Current reported yaw of the Pigeon2.
        
            - Minimum Value: -368640.0
            - Maximum Value: 368639.99725341797
            - Default Value: 0
            - Units: deg
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Yaw Status Signal Object
        :rtype: StatusSignal[degree]
        """
        return self._common_lookup(SpnValue.PIGEON2_YAW.value, None, "yaw", degree, True, refresh)
    
    def get_pitch(self, refresh: bool = True) -> StatusSignal[degree]:
        """
        Current reported pitch of the Pigeon2.
        
            - Minimum Value: -90.0
            - Maximum Value: 89.9560546875
            - Default Value: 0
            - Units: deg
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Pitch Status Signal Object
        :rtype: StatusSignal[degree]
        """
        return self._common_lookup(SpnValue.PIGEON2_PITCH.value, None, "pitch", degree, True, refresh)
    
    def get_roll(self, refresh: bool = True) -> StatusSignal[degree]:
        """
        Current reported roll of the Pigeon2.
        
            - Minimum Value: -180.0
            - Maximum Value: 179.9560546875
            - Default Value: 0
            - Units: deg
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Roll Status Signal Object
        :rtype: StatusSignal[degree]
        """
        return self._common_lookup(SpnValue.PIGEON2_ROLL.value, None, "roll", degree, True, refresh)
    
    def get_quat_w(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The W component of the reported Quaternion.
        
            - Minimum Value: -1.0001220852154804
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: QuatW Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATW.value, None, "quat_w", float, True, refresh)
    
    def get_quat_x(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The X component of the reported Quaternion.
        
            - Minimum Value: -1.0001220852154804
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: QuatX Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATX.value, None, "quat_x", float, True, refresh)
    
    def get_quat_y(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The Y component of the reported Quaternion.
        
            - Minimum Value: -1.0001220852154804
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: QuatY Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATY.value, None, "quat_y", float, True, refresh)
    
    def get_quat_z(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The Z component of the reported Quaternion.
        
            - Minimum Value: -1.0001220852154804
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: QuatZ Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_QUATZ.value, None, "quat_z", float, True, refresh)
    
    def get_gravity_vector_x(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The X component of the gravity vector.
        
        This is the X component of the reported gravity-vector. The gravity
        vector is not the acceleration experienced by the Pigeon2, rather it
        is where the Pigeon2 believes "Down" is. This can be used for
        mechanisms that are linearly related to gravity, such as an arm
        pivoting about a point, as the contribution of gravity to the arm is
        directly proportional to the contribution of gravity about one of
        these primary axis.
        
            - Minimum Value: -1.000030518509476
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: GravityVectorX Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_GRAVITY_VECTORX.value, None, "gravity_vector_x", float, True, refresh)
    
    def get_gravity_vector_y(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The Y component of the gravity vector.
        
        This is the X component of the reported gravity-vector. The gravity
        vector is not the acceleration experienced by the Pigeon2, rather it
        is where the Pigeon2 believes "Down" is. This can be used for
        mechanisms that are linearly related to gravity, such as an arm
        pivoting about a point, as the contribution of gravity to the arm is
        directly proportional to the contribution of gravity about one of
        these primary axis.
        
            - Minimum Value: -1.000030518509476
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: GravityVectorY Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_GRAVITY_VECTORY.value, None, "gravity_vector_y", float, True, refresh)
    
    def get_gravity_vector_z(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The Z component of the gravity vector.
        
        This is the Z component of the reported gravity-vector. The gravity
        vector is not the acceleration experienced by the Pigeon2, rather it
        is where the Pigeon2 believes "Down" is. This can be used for
        mechanisms that are linearly related to gravity, such as an arm
        pivoting about a point, as the contribution of gravity to the arm is
        directly proportional to the contribution of gravity about one of
        these primary axis.
        
            - Minimum Value: -1.000030518509476
            - Maximum Value: 1.0
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: GravityVectorZ Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_GRAVITY_VECTORZ.value, None, "gravity_vector_z", float, True, refresh)
    
    def get_temperature(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of the Pigeon 2.
        
            - Minimum Value: -128.0
            - Maximum Value: 127.99609375
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Temperature Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PIGEON2_TEMPERATURE.value, None, "temperature", celsius, True, refresh)
    
    def get_no_motion_enabled(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Whether the no-motion calibration feature is enabled.
        
            - Default Value: 0
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: NoMotionEnabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.PIGEON2_NO_MOTION_CAL_ENABLED.value, None, "no_motion_enabled", bool, True, refresh)
    
    def get_no_motion_count(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The number of times a no-motion event occurred, wraps at 15.
        
            - Minimum Value: 0
            - Maximum Value: 15
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: NoMotionCount Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PIGEON2_NO_MOTION_COUNT.value, None, "no_motion_count", float, True, refresh)
    
    def get_temperature_compensation_disabled(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Whether the temperature-compensation feature is disabled.
        
            - Default Value: 0
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: TemperatureCompensationDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.PIGEON2_TEMP_COMP_DISABLED.value, None, "temperature_compensation_disabled", bool, True, refresh)
    
    def get_up_time(self, refresh: bool = True) -> StatusSignal[second]:
        """
        How long the Pigeon 2's been up in seconds, caps at 255 seconds.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: s
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: UpTime Status Signal Object
        :rtype: StatusSignal[second]
        """
        return self._common_lookup(SpnValue.PIGEON2_UP_TIME.value, None, "up_time", second, True, refresh)
    
    def get_accum_gyro_x(self, refresh: bool = True) -> StatusSignal[degree]:
        """
        The accumulated gyro about the X axis without any sensor fusing.
        
            - Minimum Value: -23040.0
            - Maximum Value: 23039.9560546875
            - Default Value: 0
            - Units: deg
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AccumGyroX Status Signal Object
        :rtype: StatusSignal[degree]
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCUM_GYROX.value, None, "accum_gyro_x", degree, True, refresh)
    
    def get_accum_gyro_y(self, refresh: bool = True) -> StatusSignal[degree]:
        """
        The accumulated gyro about the Y axis without any sensor fusing.
        
            - Minimum Value: -23040.0
            - Maximum Value: 23039.9560546875
            - Default Value: 0
            - Units: deg
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AccumGyroY Status Signal Object
        :rtype: StatusSignal[degree]
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCUM_GYROY.value, None, "accum_gyro_y", degree, True, refresh)
    
    def get_accum_gyro_z(self, refresh: bool = True) -> StatusSignal[degree]:
        """
        The accumulated gyro about the Z axis without any sensor fusing.
        
            - Minimum Value: -23040.0
            - Maximum Value: 23039.9560546875
            - Default Value: 0
            - Units: deg
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AccumGyroZ Status Signal Object
        :rtype: StatusSignal[degree]
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCUM_GYROZ.value, None, "accum_gyro_z", degree, True, refresh)
    
    def get_angular_velocity_x_world(self, refresh: bool = True) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the X axis with respect
        to the world frame.  This value is mount-calibrated.
        
            - Minimum Value: -2048.0
            - Maximum Value: 2047.99609375
            - Default Value: 0
            - Units: dps
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AngularVelocityXWorld Status Signal Object
        :rtype: StatusSignal[degrees_per_second]
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITY_XWORLD.value, None, "angular_velocity_x_world", degrees_per_second, True, refresh)
    
    def get_angular_velocity_y_world(self, refresh: bool = True) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the Y axis with respect
        to the world frame.  This value is mount-calibrated.
        
            - Minimum Value: -2048.0
            - Maximum Value: 2047.99609375
            - Default Value: 0
            - Units: dps
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AngularVelocityYWorld Status Signal Object
        :rtype: StatusSignal[degrees_per_second]
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITY_YWORLD.value, None, "angular_velocity_y_world", degrees_per_second, True, refresh)
    
    def get_angular_velocity_z_world(self, refresh: bool = True) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the Z axis with respect
        to the world frame.  This value is mount-calibrated.
        
            - Minimum Value: -2048.0
            - Maximum Value: 2047.99609375
            - Default Value: 0
            - Units: dps
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AngularVelocityZWorld Status Signal Object
        :rtype: StatusSignal[degrees_per_second]
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITY_ZWORLD.value, None, "angular_velocity_z_world", degrees_per_second, True, refresh)
    
    def get_acceleration_x(self, refresh: bool = True) -> StatusSignal[g]:
        """
        The acceleration measured by Pigeon2 in the X direction.
        
        This value includes the acceleration due to gravity. If this is
        undesirable, get the gravity vector and subtract out the contribution
        in this direction.
        
            - Minimum Value: -2.0
            - Maximum Value: 1.99993896484375
            - Default Value: 0
            - Units: g
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AccelerationX Status Signal Object
        :rtype: StatusSignal[g]
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCELERATIONX.value, None, "acceleration_x", g, True, refresh)
    
    def get_acceleration_y(self, refresh: bool = True) -> StatusSignal[g]:
        """
        The acceleration measured by Pigeon2 in the Y direction.
        
        This value includes the acceleration due to gravity. If this is
        undesirable, get the gravity vector and subtract out the contribution
        in this direction.
        
            - Minimum Value: -2.0
            - Maximum Value: 1.99993896484375
            - Default Value: 0
            - Units: g
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AccelerationY Status Signal Object
        :rtype: StatusSignal[g]
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCELERATIONY.value, None, "acceleration_y", g, True, refresh)
    
    def get_acceleration_z(self, refresh: bool = True) -> StatusSignal[g]:
        """
        The acceleration measured by Pigeon2 in the Z direction.
        
        This value includes the acceleration due to gravity. If this is
        undesirable, get the gravity vector and subtract out the contribution
        in this direction.
        
            - Minimum Value: -2.0
            - Maximum Value: 1.99993896484375
            - Default Value: 0
            - Units: g
        
        Default Rates:
            - CAN 2.0: 10.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AccelerationZ Status Signal Object
        :rtype: StatusSignal[g]
        """
        return self._common_lookup(SpnValue.PIGEON2_ACCELERATIONZ.value, None, "acceleration_z", g, True, refresh)
    
    def get_supply_voltage(self, refresh: bool = True) -> StatusSignal[volt]:
        """
        Measured supply voltage to the Pigeon2.
        
            - Minimum Value: 0.0
            - Maximum Value: 31.99951171875
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: SupplyVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PIGEON2_SUPPLY_VOLTAGE.value, None, "supply_voltage", volt, True, refresh)
    
    def get_angular_velocity_x_device(self, refresh: bool = True) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the device's X axis.
        
        This value is not mount-calibrated.
        
            - Minimum Value: -1998.048780487805
            - Maximum Value: 1997.987804878049
            - Default Value: 0
            - Units: dps
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AngularVelocityXDevice Status Signal Object
        :rtype: StatusSignal[degrees_per_second]
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITYX.value, None, "angular_velocity_x_device", degrees_per_second, True, refresh)
    
    def get_angular_velocity_y_device(self, refresh: bool = True) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the device's Y axis.
        
        This value is not mount-calibrated.
        
            - Minimum Value: -1998.048780487805
            - Maximum Value: 1997.987804878049
            - Default Value: 0
            - Units: dps
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AngularVelocityYDevice Status Signal Object
        :rtype: StatusSignal[degrees_per_second]
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITYY.value, None, "angular_velocity_y_device", degrees_per_second, True, refresh)
    
    def get_angular_velocity_z_device(self, refresh: bool = True) -> StatusSignal[degrees_per_second]:
        """
        The angular velocity (ω) of the Pigeon 2 about the device's Z axis.
        
        This value is not mount-calibrated.
        
            - Minimum Value: -1998.048780487805
            - Maximum Value: 1997.987804878049
            - Default Value: 0
            - Units: dps
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AngularVelocityZDevice Status Signal Object
        :rtype: StatusSignal[degrees_per_second]
        """
        return self._common_lookup(SpnValue.PIGEON2_ANGULAR_VELOCITYZ.value, None, "angular_velocity_z_device", degrees_per_second, True, refresh)
    
    def get_magnetic_field_x(self, refresh: bool = True) -> StatusSignal[microtesla]:
        """
        The biased magnitude of the magnetic field measured by the Pigeon 2 in
        the X direction. This is only valid after performing a magnetometer
        calibration.
        
            - Minimum Value: -19660.8
            - Maximum Value: 19660.2
            - Default Value: 0
            - Units: uT
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MagneticFieldX Status Signal Object
        :rtype: StatusSignal[microtesla]
        """
        return self._common_lookup(SpnValue.PIGEON2_MAGNETIC_FIELDX.value, None, "magnetic_field_x", microtesla, True, refresh)
    
    def get_magnetic_field_y(self, refresh: bool = True) -> StatusSignal[microtesla]:
        """
        The biased magnitude of the magnetic field measured by the Pigeon 2 in
        the Y direction. This is only valid after performing a magnetometer
        calibration.
        
            - Minimum Value: -19660.8
            - Maximum Value: 19660.2
            - Default Value: 0
            - Units: uT
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MagneticFieldY Status Signal Object
        :rtype: StatusSignal[microtesla]
        """
        return self._common_lookup(SpnValue.PIGEON2_MAGNETIC_FIELDY.value, None, "magnetic_field_y", microtesla, True, refresh)
    
    def get_magnetic_field_z(self, refresh: bool = True) -> StatusSignal[microtesla]:
        """
        The biased magnitude of the magnetic field measured by the Pigeon 2 in
        the Z direction. This is only valid after performing a magnetometer
        calibration.
        
            - Minimum Value: -19660.8
            - Maximum Value: 19660.2
            - Default Value: 0
            - Units: uT
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MagneticFieldZ Status Signal Object
        :rtype: StatusSignal[microtesla]
        """
        return self._common_lookup(SpnValue.PIGEON2_MAGNETIC_FIELDZ.value, None, "magnetic_field_z", microtesla, True, refresh)
    
    def get_raw_magnetic_field_x(self, refresh: bool = True) -> StatusSignal[microtesla]:
        """
        The raw magnitude of the magnetic field measured by the Pigeon 2 in
        the X direction. This is only valid after performing a magnetometer
        calibration.
        
            - Minimum Value: -19660.8
            - Maximum Value: 19660.2
            - Default Value: 0
            - Units: uT
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RawMagneticFieldX Status Signal Object
        :rtype: StatusSignal[microtesla]
        """
        return self._common_lookup(SpnValue.PIGEON2_RAW_MAGNETIC_FIELDX.value, None, "raw_magnetic_field_x", microtesla, True, refresh)
    
    def get_raw_magnetic_field_y(self, refresh: bool = True) -> StatusSignal[microtesla]:
        """
        The raw magnitude of the magnetic field measured by the Pigeon 2 in
        the Y direction. This is only valid after performing a magnetometer
        calibration.
        
            - Minimum Value: -19660.8
            - Maximum Value: 19660.2
            - Default Value: 0
            - Units: uT
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RawMagneticFieldY Status Signal Object
        :rtype: StatusSignal[microtesla]
        """
        return self._common_lookup(SpnValue.PIGEON2_RAW_MAGNETIC_FIELDY.value, None, "raw_magnetic_field_y", microtesla, True, refresh)
    
    def get_raw_magnetic_field_z(self, refresh: bool = True) -> StatusSignal[microtesla]:
        """
        The raw magnitude of the magnetic field measured by the Pigeon 2 in
        the Z direction. This is only valid after performing a magnetometer
        calibration.
        
            - Minimum Value: -19660.8
            - Maximum Value: 19660.2
            - Default Value: 0
            - Units: uT
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RawMagneticFieldZ Status Signal Object
        :rtype: StatusSignal[microtesla]
        """
        return self._common_lookup(SpnValue.PIGEON2_RAW_MAGNETIC_FIELDZ.value, None, "raw_magnetic_field_z", microtesla, True, refresh)
    
    def get_is_pro_licensed(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Whether the device is Phoenix Pro licensed.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: IsProLicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.VERSION_IS_PRO_LICENSED.value, None, "is_pro_licensed", bool, True, refresh)
    
    def get_fault_hardware(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_Hardware Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_HARDWARE.value, None, "fault_hardware", bool, True, refresh)
    
    def get_sticky_fault_hardware(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_Hardware Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_HARDWARE.value, None, "sticky_fault_hardware", bool, True, refresh)
    
    def get_fault_undervoltage(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_Undervoltage Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_UNDERVOLTAGE.value, None, "fault_undervoltage", bool, True, refresh)
    
    def get_sticky_fault_undervoltage(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_Undervoltage Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_UNDERVOLTAGE.value, None, "sticky_fault_undervoltage", bool, True, refresh)
    
    def get_fault_boot_during_enable(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BootDuringEnable Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_BOOT_DURING_ENABLE.value, None, "fault_boot_during_enable", bool, True, refresh)
    
    def get_sticky_fault_boot_during_enable(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BootDuringEnable Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_BOOT_DURING_ENABLE.value, None, "sticky_fault_boot_during_enable", bool, True, refresh)
    
    def get_fault_unlicensed_feature_in_use(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_UnlicensedFeatureInUse Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_UNLICENSED_FEATURE_IN_USE.value, None, "fault_unlicensed_feature_in_use", bool, True, refresh)
    
    def get_sticky_fault_unlicensed_feature_in_use(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_UnlicensedFeatureInUse Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_UNLICENSED_FEATURE_IN_USE.value, None, "sticky_fault_unlicensed_feature_in_use", bool, True, refresh)
    
    def get_fault_bootup_accelerometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bootup checks failed: Accelerometer
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BootupAccelerometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOTUP_ACCEL.value, None, "fault_bootup_accelerometer", bool, True, refresh)
    
    def get_sticky_fault_bootup_accelerometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bootup checks failed: Accelerometer
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BootupAccelerometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOTUP_ACCEL.value, None, "sticky_fault_bootup_accelerometer", bool, True, refresh)
    
    def get_fault_bootup_gyroscope(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bootup checks failed: Gyroscope
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BootupGyroscope Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOTUP_GYROS.value, None, "fault_bootup_gyroscope", bool, True, refresh)
    
    def get_sticky_fault_bootup_gyroscope(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bootup checks failed: Gyroscope
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BootupGyroscope Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOTUP_GYROS.value, None, "sticky_fault_bootup_gyroscope", bool, True, refresh)
    
    def get_fault_bootup_magnetometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bootup checks failed: Magnetometer
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BootupMagnetometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOTUP_MAGNE.value, None, "fault_bootup_magnetometer", bool, True, refresh)
    
    def get_sticky_fault_bootup_magnetometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bootup checks failed: Magnetometer
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BootupMagnetometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOTUP_MAGNE.value, None, "sticky_fault_bootup_magnetometer", bool, True, refresh)
    
    def get_fault_boot_into_motion(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Motion Detected during bootup.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BootIntoMotion Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_BOOT_INTO_MOTION.value, None, "fault_boot_into_motion", bool, True, refresh)
    
    def get_sticky_fault_boot_into_motion(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Motion Detected during bootup.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BootIntoMotion Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_BOOT_INTO_MOTION.value, None, "sticky_fault_boot_into_motion", bool, True, refresh)
    
    def get_fault_data_acquired_late(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Motion stack data acquisition was slower than expected
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_DataAcquiredLate Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_DATA_ACQUIRED_LATE.value, None, "fault_data_acquired_late", bool, True, refresh)
    
    def get_sticky_fault_data_acquired_late(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Motion stack data acquisition was slower than expected
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_DataAcquiredLate Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_DATA_ACQUIRED_LATE.value, None, "sticky_fault_data_acquired_late", bool, True, refresh)
    
    def get_fault_loop_time_slow(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Motion stack loop time was slower than expected.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_LoopTimeSlow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_LOOP_TIME_SLOW.value, None, "fault_loop_time_slow", bool, True, refresh)
    
    def get_sticky_fault_loop_time_slow(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Motion stack loop time was slower than expected.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_LoopTimeSlow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_LOOP_TIME_SLOW.value, None, "sticky_fault_loop_time_slow", bool, True, refresh)
    
    def get_fault_saturated_magnetometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Magnetometer values are saturated
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_SaturatedMagnetometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_SATURATED_MAGNE.value, None, "fault_saturated_magnetometer", bool, True, refresh)
    
    def get_sticky_fault_saturated_magnetometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Magnetometer values are saturated
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_SaturatedMagnetometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_SATURATED_MAGNE.value, None, "sticky_fault_saturated_magnetometer", bool, True, refresh)
    
    def get_fault_saturated_accelerometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Accelerometer values are saturated
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_SaturatedAccelerometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_SATURATED_ACCEL.value, None, "fault_saturated_accelerometer", bool, True, refresh)
    
    def get_sticky_fault_saturated_accelerometer(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Accelerometer values are saturated
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_SaturatedAccelerometer Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_SATURATED_ACCEL.value, None, "sticky_fault_saturated_accelerometer", bool, True, refresh)
    
    def get_fault_saturated_gyroscope(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Gyroscope values are saturated
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_SaturatedGyroscope Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PIGEON2_SATURATED_GYROS.value, None, "fault_saturated_gyroscope", bool, True, refresh)
    
    def get_sticky_fault_saturated_gyroscope(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Gyroscope values are saturated
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_SaturatedGyroscope Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PIGEON2_SATURATED_GYROS.value, None, "sticky_fault_saturated_gyroscope", bool, True, refresh)
    

    

    @overload
    def set_control(self, request: SupportsSendRequest) -> StatusCode:
        """
        Control device with generic control request object.

        If control request is not supported by device, this request
        will fail with StatusCode NotSupported

        :param request: Control object to request of the device
        :type request: SupportsSendRequest
        :returns: StatusCode of the request
        :rtype: StatusCode
        """
        ...

    def set_control(self, request: SupportsSendRequest) -> StatusCode:
        if isinstance(request, ()):
            return self._set_control_private(request)
        return StatusCode.NOT_SUPPORTED

    
    def set_yaw(self, new_value: degree, timeout_seconds: second = 0.100) -> StatusCode:
        """
        The yaw to set the Pigeon2 to right now.
        
        :param new_value: Value to set to. Units are in deg.
        :type new_value: degree
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.set_yaw(new_value, timeout_seconds)
    
    def clear_sticky_faults(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear the sticky faults in the device.
        
        This typically has no impact on the device functionality.  Instead, it
        just clears telemetry faults that are accessible via API and Tuner
        Self-Test.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_faults(timeout_seconds)
    
    def clear_sticky_fault_hardware(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Hardware fault occurred
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_hardware(timeout_seconds)
    
    def clear_sticky_fault_undervoltage(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device supply voltage dropped to near brownout
        levels
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_undervoltage(timeout_seconds)
    
    def clear_sticky_fault_boot_during_enable(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device boot while detecting the enable signal
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_boot_during_enable(timeout_seconds)
    
    def clear_sticky_fault_unlicensed_feature_in_use(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: An unlicensed feature is in use, device may not
        behave as expected.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_unlicensed_feature_in_use(timeout_seconds)
    
    def clear_sticky_fault_bootup_accelerometer(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Bootup checks failed: Accelerometer
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_bootup_accelerometer(timeout_seconds)
    
    def clear_sticky_fault_bootup_gyroscope(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Bootup checks failed: Gyroscope
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_bootup_gyroscope(timeout_seconds)
    
    def clear_sticky_fault_bootup_magnetometer(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Bootup checks failed: Magnetometer
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_bootup_magnetometer(timeout_seconds)
    
    def clear_sticky_fault_boot_into_motion(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Motion Detected during bootup.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_boot_into_motion(timeout_seconds)
    
    def clear_sticky_fault_data_acquired_late(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Motion stack data acquisition was slower than
        expected
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_data_acquired_late(timeout_seconds)
    
    def clear_sticky_fault_loop_time_slow(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Motion stack loop time was slower than expected.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_loop_time_slow(timeout_seconds)
    
    def clear_sticky_fault_saturated_magnetometer(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Magnetometer values are saturated
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_saturated_magnetometer(timeout_seconds)
    
    def clear_sticky_fault_saturated_accelerometer(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Accelerometer values are saturated
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_saturated_accelerometer(timeout_seconds)
    
    def clear_sticky_fault_saturated_gyroscope(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Gyroscope values are saturated
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_saturated_gyroscope(timeout_seconds)

