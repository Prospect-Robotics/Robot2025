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
from phoenix6.hardware.traits.common_talon_with_foc import CommonTalonWithFOC
from phoenix6.controls.duty_cycle_out import DutyCycleOut
from phoenix6.controls.torque_current_foc import TorqueCurrentFOC
from phoenix6.controls.voltage_out import VoltageOut
from phoenix6.controls.position_duty_cycle import PositionDutyCycle
from phoenix6.controls.position_voltage import PositionVoltage
from phoenix6.controls.position_torque_current_foc import PositionTorqueCurrentFOC
from phoenix6.controls.velocity_duty_cycle import VelocityDutyCycle
from phoenix6.controls.velocity_voltage import VelocityVoltage
from phoenix6.controls.velocity_torque_current_foc import VelocityTorqueCurrentFOC
from phoenix6.controls.motion_magic_duty_cycle import MotionMagicDutyCycle
from phoenix6.controls.motion_magic_voltage import MotionMagicVoltage
from phoenix6.controls.motion_magic_torque_current_foc import MotionMagicTorqueCurrentFOC
from phoenix6.controls.differential_duty_cycle import DifferentialDutyCycle
from phoenix6.controls.differential_voltage import DifferentialVoltage
from phoenix6.controls.differential_position_duty_cycle import DifferentialPositionDutyCycle
from phoenix6.controls.differential_position_voltage import DifferentialPositionVoltage
from phoenix6.controls.differential_velocity_duty_cycle import DifferentialVelocityDutyCycle
from phoenix6.controls.differential_velocity_voltage import DifferentialVelocityVoltage
from phoenix6.controls.differential_motion_magic_duty_cycle import DifferentialMotionMagicDutyCycle
from phoenix6.controls.differential_motion_magic_voltage import DifferentialMotionMagicVoltage
from phoenix6.controls.follower import Follower
from phoenix6.controls.strict_follower import StrictFollower
from phoenix6.controls.differential_follower import DifferentialFollower
from phoenix6.controls.differential_strict_follower import DifferentialStrictFollower
from phoenix6.controls.neutral_out import NeutralOut
from phoenix6.controls.coast_out import CoastOut
from phoenix6.controls.static_brake import StaticBrake
from phoenix6.controls.music_tone import MusicTone
from phoenix6.controls.motion_magic_velocity_duty_cycle import MotionMagicVelocityDutyCycle
from phoenix6.controls.motion_magic_velocity_torque_current_foc import MotionMagicVelocityTorqueCurrentFOC
from phoenix6.controls.motion_magic_velocity_voltage import MotionMagicVelocityVoltage
from phoenix6.controls.motion_magic_expo_duty_cycle import MotionMagicExpoDutyCycle
from phoenix6.controls.motion_magic_expo_voltage import MotionMagicExpoVoltage
from phoenix6.controls.motion_magic_expo_torque_current_foc import MotionMagicExpoTorqueCurrentFOC
from phoenix6.controls.dynamic_motion_magic_duty_cycle import DynamicMotionMagicDutyCycle
from phoenix6.controls.dynamic_motion_magic_voltage import DynamicMotionMagicVoltage
from phoenix6.controls.dynamic_motion_magic_torque_current_foc import DynamicMotionMagicTorqueCurrentFOC
from phoenix6.controls.compound.diff_duty_cycle_out_position import Diff_DutyCycleOut_Position
from phoenix6.controls.compound.diff_position_duty_cycle_position import Diff_PositionDutyCycle_Position
from phoenix6.controls.compound.diff_velocity_duty_cycle_position import Diff_VelocityDutyCycle_Position
from phoenix6.controls.compound.diff_motion_magic_duty_cycle_position import Diff_MotionMagicDutyCycle_Position
from phoenix6.controls.compound.diff_duty_cycle_out_velocity import Diff_DutyCycleOut_Velocity
from phoenix6.controls.compound.diff_position_duty_cycle_velocity import Diff_PositionDutyCycle_Velocity
from phoenix6.controls.compound.diff_velocity_duty_cycle_velocity import Diff_VelocityDutyCycle_Velocity
from phoenix6.controls.compound.diff_motion_magic_duty_cycle_velocity import Diff_MotionMagicDutyCycle_Velocity
from phoenix6.controls.compound.diff_voltage_out_position import Diff_VoltageOut_Position
from phoenix6.controls.compound.diff_position_voltage_position import Diff_PositionVoltage_Position
from phoenix6.controls.compound.diff_velocity_voltage_position import Diff_VelocityVoltage_Position
from phoenix6.controls.compound.diff_motion_magic_voltage_position import Diff_MotionMagicVoltage_Position
from phoenix6.controls.compound.diff_voltage_out_velocity import Diff_VoltageOut_Velocity
from phoenix6.controls.compound.diff_position_voltage_velocity import Diff_PositionVoltage_Velocity
from phoenix6.controls.compound.diff_velocity_voltage_velocity import Diff_VelocityVoltage_Velocity
from phoenix6.controls.compound.diff_motion_magic_voltage_velocity import Diff_MotionMagicVoltage_Velocity
from phoenix6.controls.compound.diff_torque_current_foc_position import Diff_TorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_position_torque_current_foc_position import Diff_PositionTorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_velocity_torque_current_foc_position import Diff_VelocityTorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_motion_magic_torque_current_foc_position import Diff_MotionMagicTorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_torque_current_foc_velocity import Diff_TorqueCurrentFOC_Velocity
from phoenix6.controls.compound.diff_position_torque_current_foc_velocity import Diff_PositionTorqueCurrentFOC_Velocity
from phoenix6.controls.compound.diff_velocity_torque_current_foc_velocity import Diff_VelocityTorqueCurrentFOC_Velocity
from phoenix6.controls.compound.diff_motion_magic_torque_current_foc_velocity import Diff_MotionMagicTorqueCurrentFOC_Velocity
from phoenix6.configs.talon_fx_configs import TalonFXConfigurator
from phoenix6.signals.spn_enums import ForwardLimitValue, ReverseLimitValue, AppliedRotorPolarityValue, ControlModeValue, MotionMagicIsRunningValue, DeviceEnableValue, MotorOutputStatusValue, DifferentialControlModeValue, BridgeOutputValue, ConnectedMotorValue
from phoenix6.sim.talon_fx_sim_state import TalonFXSimState

class CoreTalonFX(ParentDevice, CommonTalonWithFOC):
    """
    Constructs a new Talon FX motor controller object.

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
        super().__init__(device_id, "talon fx", canbus)
        self.configurator = TalonFXConfigurator(self._device_identifier)

        Native.instance().c_ctre_phoenix6_platform_sim_create(DeviceType.P6_TalonFXType.value, device_id)
        self.__sim_state = None


    @property
    def sim_state(self) -> TalonFXSimState:
        """
        Get the simulation state for this device.

        This function reuses an allocated simulation state
        object, so it is safe to call this function multiple
        times in a robot loop.

        :returns: Simulation state
        :rtype: TalonFXSimState
        """

        if self.__sim_state is None:
            self.__sim_state = TalonFXSimState(self)
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
    
    def get_motor_voltage(self, refresh: bool = True) -> StatusSignal[volt]:
        """
        The applied (output) motor voltage.
        
            - Minimum Value: -40.96
            - Maximum Value: 40.95
            - Default Value: 0
            - Units: V
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_MOTOR_VOLTAGE.value, None, "motor_voltage", volt, True, refresh)
    
    def get_forward_limit(self, refresh: bool = True) -> StatusSignal[ForwardLimitValue]:
        """
        Forward Limit Pin.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ForwardLimit Status Signal Object
        :rtype: StatusSignal[ForwardLimitValue]
        """
        return self._common_lookup(SpnValue.FORWARD_LIMIT.value, None, "forward_limit", ForwardLimitValue, True, refresh)
    
    def get_reverse_limit(self, refresh: bool = True) -> StatusSignal[ReverseLimitValue]:
        """
        Reverse Limit Pin.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ReverseLimit Status Signal Object
        :rtype: StatusSignal[ReverseLimitValue]
        """
        return self._common_lookup(SpnValue.REVERSE_LIMIT.value, None, "reverse_limit", ReverseLimitValue, True, refresh)
    
    def get_applied_rotor_polarity(self, refresh: bool = True) -> StatusSignal[AppliedRotorPolarityValue]:
        """
        The applied rotor polarity as seen from the front of the motor.  This
        typically is determined by the Inverted config, but can be overridden
        if using Follower features.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AppliedRotorPolarity Status Signal Object
        :rtype: StatusSignal[AppliedRotorPolarityValue]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_ROTOR_POLARITY.value, None, "applied_rotor_polarity", AppliedRotorPolarityValue, True, refresh)
    
    def get_duty_cycle(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The applied motor duty cycle.
        
            - Minimum Value: -2.0
            - Maximum Value: 1.9990234375
            - Default Value: 0
            - Units: fractional
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DutyCycle Status Signal Object
        :rtype: StatusSignal[float]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_DUTY_CYCLE.value, None, "duty_cycle", float, True, refresh)
    
    def get_torque_current(self, refresh: bool = True) -> StatusSignal[ampere]:
        """
        Current corresponding to the torque output by the motor. Similar to
        StatorCurrent. Users will likely prefer this current to calculate the
        applied torque to the rotor.
        
        Stator current where positive current means torque is applied in the
        forward direction as determined by the Inverted setting.
        
            - Minimum Value: -327.68
            - Maximum Value: 327.67
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: TorqueCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_TORQUE_CURRENT.value, None, "torque_current", ampere, True, refresh)
    
    def get_stator_current(self, refresh: bool = True) -> StatusSignal[ampere]:
        """
        Current corresponding to the stator windings. Similar to
        TorqueCurrent. Users will likely prefer TorqueCurrent over
        StatorCurrent.
        
        Stator current where Positive current indicates motoring regardless of
        direction. Negative current indicates regenerative braking regardless
        of direction.
        
            - Minimum Value: -327.68
            - Maximum Value: 327.66
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StatorCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_STATOR_CURRENT.value, None, "stator_current", ampere, True, refresh)
    
    def get_supply_current(self, refresh: bool = True) -> StatusSignal[ampere]:
        """
        Measured supply side current.
        
            - Minimum Value: -327.68
            - Maximum Value: 327.66
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: SupplyCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_SUPPLY_CURRENT.value, None, "supply_current", ampere, True, refresh)
    
    def get_supply_voltage(self, refresh: bool = True) -> StatusSignal[volt]:
        """
        Measured supply voltage to the device.
        
            - Minimum Value: 4
            - Maximum Value: 29.575
            - Default Value: 4
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
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_SUPPLY_VOLTAGE.value, None, "supply_voltage", volt, True, refresh)
    
    def get_device_temp(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of device.
        
        This is the temperature that the device measures itself to be at.
        Similar to Processor Temperature.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DeviceTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_DEVICE_TEMP.value, None, "device_temp", celsius, True, refresh)
    
    def get_processor_temp(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of the processor.
        
        This is the temperature that the processor measures itself to be at.
        Similar to Device Temperature.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ProcessorTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_PROCESSOR_TEMP.value, None, "processor_temp", celsius, True, refresh)
    
    def get_rotor_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the motor rotor. This velocity is not affected by any
        feedback configs.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RotorVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_ROTOR_POS_AND_VEL_VELOCITY.value, None, "rotor_velocity", rotations_per_second, True, refresh)
    
    def get_rotor_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Position of the motor rotor. This position is only affected by the
        RotorOffset config and calls to setPosition.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RotorPosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_ROTOR_POS_AND_VEL_POSITION.value, None, "rotor_position", rotation, True, refresh)
    
    def get_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the device in mechanism rotations per second. This can be
        the velocity of a remote sensor and is affected by the
        RotorToSensorRatio and SensorToMechanismRatio configs.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Velocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_POS_AND_VEL_VELOCITY.value, None, "velocity", rotations_per_second, True, refresh)
    
    def get_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Position of the device in mechanism rotations. This can be the
        position of a remote sensor and is affected by the RotorToSensorRatio
        and SensorToMechanismRatio configs, as well as calls to setPosition.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Position Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_POS_AND_VEL_POSITION.value, None, "position", rotation, True, refresh)
    
    def get_acceleration(self, refresh: bool = True) -> StatusSignal[rotations_per_second_squared]:
        """
        Acceleration of the device in mechanism rotations per second². This
        can be the acceleration of a remote sensor and is affected by the
        RotorToSensorRatio and SensorToMechanismRatio configs.
        
            - Minimum Value: -2048.0
            - Maximum Value: 2047.75
            - Default Value: 0
            - Units: rotations per second²
        
        Default Rates:
            - CAN 2.0: 50.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Acceleration Status Signal Object
        :rtype: StatusSignal[rotations_per_second_squared]
        """
        return self._common_lookup(SpnValue.PRO_POS_AND_VEL_ACCELERATION.value, None, "acceleration", rotations_per_second_squared, True, refresh)
    
    def get_control_mode(self, refresh: bool = True) -> StatusSignal[ControlModeValue]:
        """
        The active control mode of the motor controller.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ControlMode Status Signal Object
        :rtype: StatusSignal[ControlModeValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_CONTROL_MODE.value, None, "control_mode", ControlModeValue, True, refresh)
    
    def get_motion_magic_is_running(self, refresh: bool = True) -> StatusSignal[MotionMagicIsRunningValue]:
        """
        Check if Motion Magic® is running.  This is equivalent to checking
        that the reported control mode is a Motion Magic® based mode.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotionMagicIsRunning Status Signal Object
        :rtype: StatusSignal[MotionMagicIsRunningValue]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_IS_MOTION_MAGIC_RUNNING.value, None, "motion_magic_is_running", MotionMagicIsRunningValue, True, refresh)
    
    def get_device_enable(self, refresh: bool = True) -> StatusSignal[DeviceEnableValue]:
        """
        Indicates if device is actuator enabled.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DeviceEnable Status Signal Object
        :rtype: StatusSignal[DeviceEnableValue]
        """
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_DEVICE_ENABLE.value, None, "device_enable", DeviceEnableValue, True, refresh)
    
    def get_closed_loop_slot(self, refresh: bool = True) -> StatusSignal[int]:
        """
        The slot that the closed-loop PID is using.
        
            - Minimum Value: 0
            - Maximum Value: 2
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopSlot Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_SLOT.value, None, "closed_loop_slot", int, True, refresh)
    
    def get_motor_output_status(self, refresh: bool = True) -> StatusSignal[MotorOutputStatusValue]:
        """
        Assess the status of the motor output with respect to load and supply.
        
        This routine can be used to determine the general status of motor
        commutation.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorOutputStatus Status Signal Object
        :rtype: StatusSignal[MotorOutputStatusValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_MOTOR_OUTPUT_STATUS.value, None, "motor_output_status", MotorOutputStatusValue, True, refresh)
    
    def get_differential_control_mode(self, refresh: bool = True) -> StatusSignal[DifferentialControlModeValue]:
        """
        The active control mode of the differential controller.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialControlMode Status Signal Object
        :rtype: StatusSignal[DifferentialControlModeValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_DIFFERENTIAL_CONTROL_MODE.value, None, "differential_control_mode", DifferentialControlModeValue, True, refresh)
    
    def get_differential_average_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Average component of the differential velocity of device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialAverageVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_AVG_POS_AND_VEL_VELOCITY.value, None, "differential_average_velocity", rotations_per_second, True, refresh)
    
    def get_differential_average_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Average component of the differential position of device.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialAveragePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_AVG_POS_AND_VEL_POSITION.value, None, "differential_average_position", rotation, True, refresh)
    
    def get_differential_difference_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Difference component of the differential velocity of device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialDifferenceVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_POS_AND_VEL_VELOCITY.value, None, "differential_difference_velocity", rotations_per_second, True, refresh)
    
    def get_differential_difference_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Difference component of the differential position of device.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialDifferencePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_POS_AND_VEL_POSITION.value, None, "differential_difference_position", rotation, True, refresh)
    
    def get_differential_closed_loop_slot(self, refresh: bool = True) -> StatusSignal[int]:
        """
        The slot that the closed-loop differential PID is using.
        
            - Minimum Value: 0
            - Maximum Value: 2
            - Default Value: 0
            - Units: 
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopSlot Status Signal Object
        :rtype: StatusSignal[int]
        """
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_SLOT.value, None, "differential_closed_loop_slot", int, True, refresh)
    
    def get_motor_kt(self, refresh: bool = True) -> StatusSignal[newton_meters_per_ampere]:
        """
        The torque constant (K_T) of the motor.
        
            - Minimum Value: 0.0
            - Maximum Value: 0.025500000000000002
            - Default Value: 0
            - Units: Nm/A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorKT Status Signal Object
        :rtype: StatusSignal[newton_meters_per_ampere]
        """
        return self._common_lookup(SpnValue.TALON_FX_MOTOR_CONSTANTS_KT.value, None, "motor_kt", newton_meters_per_ampere, True, refresh)
    
    def get_motor_kv(self, refresh: bool = True) -> StatusSignal[rpm_per_volt]:
        """
        The velocity constant (K_V) of the motor.
        
            - Minimum Value: 0.0
            - Maximum Value: 2047.0
            - Default Value: 0
            - Units: RPM/V
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorKV Status Signal Object
        :rtype: StatusSignal[rpm_per_volt]
        """
        return self._common_lookup(SpnValue.TALON_FX_MOTOR_CONSTANTS_KV.value, None, "motor_kv", rpm_per_volt, True, refresh)
    
    def get_motor_stall_current(self, refresh: bool = True) -> StatusSignal[ampere]:
        """
        The stall current of the motor at 12 V output.
        
            - Minimum Value: 0.0
            - Maximum Value: 1023.0
            - Default Value: 0
            - Units: A
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorStallCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        return self._common_lookup(SpnValue.TALON_FX_MOTOR_CONSTANTS_STALL_CURRENT.value, None, "motor_stall_current", ampere, True, refresh)
    
    def get_bridge_output(self, refresh: bool = True) -> StatusSignal[BridgeOutputValue]:
        """
        The applied output of the bridge.
        
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: BridgeOutput Status Signal Object
        :rtype: StatusSignal[BridgeOutputValue]
        """
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_BRIDGE_TYPE_PUBLIC.value, None, "bridge_output", BridgeOutputValue, True, refresh)
    
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
    
    def get_ancillary_device_temp(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of device from second sensor.
        
        Newer versions of Talon have multiple temperature measurement methods.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AncillaryDeviceTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        return self._common_lookup(SpnValue.PRO_SUPPLY_AND_TEMP_DEVICE_TEMP2.value, None, "ancillary_device_temp", celsius, True, refresh)
    
    def get_connected_motor(self, refresh: bool = True) -> StatusSignal[ConnectedMotorValue]:
        """
        The type of motor attached to the Talon.
        
        This can be used to determine what motor is attached to the Talon FX. 
        Return will be "Unknown" if firmware is too old or device is not
        present.
        
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ConnectedMotor Status Signal Object
        :rtype: StatusSignal[ConnectedMotorValue]
        """
        return self._common_lookup(SpnValue.TALON_FX_CONNECTED_MOTOR.value, None, "connected_motor", ConnectedMotorValue, True, refresh)
    
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
    
    def get_fault_proc_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Processor temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ProcTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_PROC_TEMP.value, None, "fault_proc_temp", bool, True, refresh)
    
    def get_sticky_fault_proc_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Processor temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ProcTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_PROC_TEMP.value, None, "sticky_fault_proc_temp", bool, True, refresh)
    
    def get_fault_device_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_DeviceTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_DEVICE_TEMP.value, None, "fault_device_temp", bool, True, refresh)
    
    def get_sticky_fault_device_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device temperature exceeded limit
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_DeviceTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_DEVICE_TEMP.value, None, "sticky_fault_device_temp", bool, True, refresh)
    
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
    
    def get_fault_bridge_brownout(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bridge was disabled most likely due to supply voltage dropping too
        low.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BridgeBrownout Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_BRIDGE_BROWNOUT.value, None, "fault_bridge_brownout", bool, True, refresh)
    
    def get_sticky_fault_bridge_brownout(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bridge was disabled most likely due to supply voltage dropping too
        low.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BridgeBrownout Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_BRIDGE_BROWNOUT.value, None, "sticky_fault_bridge_brownout", bool, True, refresh)
    
    def get_fault_remote_sensor_reset(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor has reset.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_RemoteSensorReset Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REMOTE_SENSOR_RESET.value, None, "fault_remote_sensor_reset", bool, True, refresh)
    
    def get_sticky_fault_remote_sensor_reset(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor has reset.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_RemoteSensorReset Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REMOTE_SENSOR_RESET.value, None, "sticky_fault_remote_sensor_reset", bool, True, refresh)
    
    def get_fault_missing_differential_fx(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote Talon used for differential control is not present on CAN
        Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_MissingDifferentialFX Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_MISSING_DIFFERENTIAL_FX.value, None, "fault_missing_differential_fx", bool, True, refresh)
    
    def get_sticky_fault_missing_differential_fx(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote Talon used for differential control is not present on CAN
        Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_MissingDifferentialFX Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_MISSING_DIFFERENTIAL_FX.value, None, "sticky_fault_missing_differential_fx", bool, True, refresh)
    
    def get_fault_remote_sensor_pos_overflow(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor position has overflowed. Because of the nature of
        remote sensors, it is possible for the remote sensor position to
        overflow beyond what is supported by the status signal frame. However,
        this is rare and cannot occur over the course of an FRC match under
        normal use.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_RemoteSensorPosOverflow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REMOTE_SENSOR_POS_OVERFLOW.value, None, "fault_remote_sensor_pos_overflow", bool, True, refresh)
    
    def get_sticky_fault_remote_sensor_pos_overflow(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor position has overflowed. Because of the nature of
        remote sensors, it is possible for the remote sensor position to
        overflow beyond what is supported by the status signal frame. However,
        this is rare and cannot occur over the course of an FRC match under
        normal use.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_RemoteSensorPosOverflow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REMOTE_SENSOR_POS_OVERFLOW.value, None, "sticky_fault_remote_sensor_pos_overflow", bool, True, refresh)
    
    def get_fault_over_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage has exceeded the maximum voltage rating of device.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_OverSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_OVER_SUPPLYV.value, None, "fault_over_supply_v", bool, True, refresh)
    
    def get_sticky_fault_over_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage has exceeded the maximum voltage rating of device.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_OverSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_OVER_SUPPLYV.value, None, "sticky_fault_over_supply_v", bool, True, refresh)
    
    def get_fault_unstable_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage is unstable.  Ensure you are using a battery and
        current limited power supply.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_UnstableSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_UNSTABLE_SUPPLYV.value, None, "fault_unstable_supply_v", bool, True, refresh)
    
    def get_sticky_fault_unstable_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage is unstable.  Ensure you are using a battery and
        current limited power supply.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_UnstableSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_UNSTABLE_SUPPLYV.value, None, "sticky_fault_unstable_supply_v", bool, True, refresh)
    
    def get_fault_reverse_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ReverseHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REVERSE_HARD_LIMIT.value, None, "fault_reverse_hard_limit", bool, True, refresh)
    
    def get_sticky_fault_reverse_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ReverseHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REVERSE_HARD_LIMIT.value, None, "sticky_fault_reverse_hard_limit", bool, True, refresh)
    
    def get_fault_forward_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ForwardHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_FORWARD_HARD_LIMIT.value, None, "fault_forward_hard_limit", bool, True, refresh)
    
    def get_sticky_fault_forward_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ForwardHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_FORWARD_HARD_LIMIT.value, None, "sticky_fault_forward_hard_limit", bool, True, refresh)
    
    def get_fault_reverse_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ReverseSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_REVERSE_SOFT_LIMIT.value, None, "fault_reverse_soft_limit", bool, True, refresh)
    
    def get_sticky_fault_reverse_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ReverseSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_REVERSE_SOFT_LIMIT.value, None, "sticky_fault_reverse_soft_limit", bool, True, refresh)
    
    def get_fault_forward_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ForwardSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_FORWARD_SOFT_LIMIT.value, None, "fault_forward_soft_limit", bool, True, refresh)
    
    def get_sticky_fault_forward_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ForwardSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_FORWARD_SOFT_LIMIT.value, None, "sticky_fault_forward_soft_limit", bool, True, refresh)
    
    def get_fault_missing_soft_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote soft limit device is not present on CAN Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_MissingSoftLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_MISSING_REM_SOFT_LIM.value, None, "fault_missing_soft_limit_remote", bool, True, refresh)
    
    def get_sticky_fault_missing_soft_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote soft limit device is not present on CAN Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_MissingSoftLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_MISSING_REM_SOFT_LIM.value, None, "sticky_fault_missing_soft_limit_remote", bool, True, refresh)
    
    def get_fault_missing_hard_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote limit switch device is not present on CAN Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_MissingHardLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_MISSING_REM_HARD_LIM.value, None, "fault_missing_hard_limit_remote", bool, True, refresh)
    
    def get_sticky_fault_missing_hard_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote limit switch device is not present on CAN Bus.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_MissingHardLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_MISSING_REM_HARD_LIM.value, None, "sticky_fault_missing_hard_limit_remote", bool, True, refresh)
    
    def get_fault_remote_sensor_data_invalid(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor's data is no longer trusted. This can happen if the
        remote sensor disappears from the CAN bus or if the remote sensor
        indicates its data is no longer valid, such as when a CANcoder's
        magnet strength falls into the "red" range.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_RemoteSensorDataInvalid Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_MISSING_REMOTE_SENSOR.value, None, "fault_remote_sensor_data_invalid", bool, True, refresh)
    
    def get_sticky_fault_remote_sensor_data_invalid(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor's data is no longer trusted. This can happen if the
        remote sensor disappears from the CAN bus or if the remote sensor
        indicates its data is no longer valid, such as when a CANcoder's
        magnet strength falls into the "red" range.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_RemoteSensorDataInvalid Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_MISSING_REMOTE_SENSOR.value, None, "sticky_fault_remote_sensor_data_invalid", bool, True, refresh)
    
    def get_fault_fused_sensor_out_of_sync(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor used for fusion has fallen out of sync to the local
        sensor. A re-synchronization has occurred, which may cause a
        discontinuity. This typically happens if there is significant slop in
        the mechanism, or if the RotorToSensorRatio configuration parameter is
        incorrect.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_FusedSensorOutOfSync Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_FUSED_SENSOR_OUT_OF_SYNC.value, None, "fault_fused_sensor_out_of_sync", bool, True, refresh)
    
    def get_sticky_fault_fused_sensor_out_of_sync(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor used for fusion has fallen out of sync to the local
        sensor. A re-synchronization has occurred, which may cause a
        discontinuity. This typically happens if there is significant slop in
        the mechanism, or if the RotorToSensorRatio configuration parameter is
        incorrect.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_FusedSensorOutOfSync Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_FUSED_SENSOR_OUT_OF_SYNC.value, None, "sticky_fault_fused_sensor_out_of_sync", bool, True, refresh)
    
    def get_fault_stator_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Stator current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_StatorCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_STATOR_CURR_LIMIT.value, None, "fault_stator_curr_limit", bool, True, refresh)
    
    def get_sticky_fault_stator_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Stator current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_StatorCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_STATOR_CURR_LIMIT.value, None, "sticky_fault_stator_curr_limit", bool, True, refresh)
    
    def get_fault_supply_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_SupplyCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_SUPPLY_CURR_LIMIT.value, None, "fault_supply_curr_limit", bool, True, refresh)
    
    def get_sticky_fault_supply_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply current limit occured.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_SupplyCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_SUPPLY_CURR_LIMIT.value, None, "sticky_fault_supply_curr_limit", bool, True, refresh)
    
    def get_fault_using_fused_cancoder_while_unlicensed(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Using Fused CANcoder feature while unlicensed. Device has fallen back
        to remote CANcoder.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_UsingFusedCANcoderWhileUnlicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_USING_FUSED_CCWHILE_UNLICENSED.value, None, "fault_using_fused_cancoder_while_unlicensed", bool, True, refresh)
    
    def get_sticky_fault_using_fused_cancoder_while_unlicensed(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Using Fused CANcoder feature while unlicensed. Device has fallen back
        to remote CANcoder.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_UsingFusedCANcoderWhileUnlicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_USING_FUSED_CCWHILE_UNLICENSED.value, None, "sticky_fault_using_fused_cancoder_while_unlicensed", bool, True, refresh)
    
    def get_fault_static_brake_disabled(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Static brake was momentarily disabled due to excessive braking current
        while disabled.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_StaticBrakeDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.FAULT_TALONFX_STATIC_BRAKE_DISABLED.value, None, "fault_static_brake_disabled", bool, True, refresh)
    
    def get_sticky_fault_static_brake_disabled(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Static brake was momentarily disabled due to excessive braking current
        while disabled.
        
            - Default Value: False
        
        Default Rates:
            - CAN: 4.0 Hz
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_StaticBrakeDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        return self._common_lookup(SpnValue.STICKY_FAULT_TALONFX_STATIC_BRAKE_DISABLED.value, None, "sticky_fault_static_brake_disabled", bool, True, refresh)
    
    def get_closed_loop_proportional_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop proportional component
        
        The portion of the closed loop output that is the proportional to the
        error. Alternatively, the p-Contribution of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopProportionalOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_DC.value: "",
            SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_V.value: "",
            SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_PROPORTIONAL_OUTPUT_DC.value, map_filler, "closed_loop_proportional_output", float, True, refresh)
    
    def get_closed_loop_integrated_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop integrated component
        
        The portion of the closed loop output that is proportional to the
        integrated error. Alternatively, the i-Contribution of the closed loop
        output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopIntegratedOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_DC.value: "",
            SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_V.value: "",
            SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_INTEGRATED_ACCUM_DC.value, map_filler, "closed_loop_integrated_output", float, True, refresh)
    
    def get_closed_loop_feed_forward(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Feedforward passed by the user
        
        This is the general feedforward that the user provides for the closed
        loop.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopFeedForward Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_DC.value: "",
            SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_V.value: "",
            SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDSTATE_ENABLES_FEED_FORWARD_DC.value, map_filler, "closed_loop_feed_forward", float, True, refresh)
    
    def get_closed_loop_derivative_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop derivative component
        
        The portion of the closed loop output that is the proportional to the
        deriviative the error. Alternatively, the d-Contribution of the closed
        loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopDerivativeOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_DC.value: "",
            SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_V.value: "",
            SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_DERIVATIVE_OUTPUT_DC.value, map_filler, "closed_loop_derivative_output", float, True, refresh)
    
    def get_closed_loop_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop total output
        
        The total output of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDOUTPUT_OUTPUT_DC.value: "",
            SpnValue.PRO_PIDOUTPUT_OUTPUT_V.value: "",
            SpnValue.PRO_PIDOUTPUT_OUTPUT_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDOUTPUT_OUTPUT_DC.value, map_filler, "closed_loop_output", float, True, refresh)
    
    def get_closed_loop_reference(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Value that the closed loop is targeting
        
        This is the value that the closed loop PID controller targets.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopReference Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDREF_PIDERR_PIDREF_POSITION.value: "",
            SpnValue.PRO_PIDREF_PIDERR_PIDREF_VELOCITY.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDREF_PIDERR_PIDREF_POSITION.value, map_filler, "closed_loop_reference", float, True, refresh)
    
    def get_closed_loop_reference_slope(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Derivative of the target that the closed loop is targeting
        
        This is the change in the closed loop reference. This may be used in
        the feed-forward calculation, the derivative-error, or in application
        of the signage for kS. Typically, this represents the target velocity
        during Motion Magic®.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopReferenceSlope Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_POSITION.value: "",
            SpnValue.PRO_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_VELOCITY.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_POSITION.value, map_filler, "closed_loop_reference_slope", float, True, refresh)
    
    def get_closed_loop_error(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The difference between target reference and current measurement
        
        This is the value that is treated as the error in the PID loop.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopError Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_PIDREF_PIDERR_PIDERR_POSITION.value: "",
            SpnValue.PRO_PIDREF_PIDERR_PIDERR_VELOCITY.value: "",
        }
        return self._common_lookup(SpnValue.PRO_PIDREF_PIDERR_PIDERR_POSITION.value, map_filler, "closed_loop_error", float, True, refresh)
    
    def get_differential_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The calculated motor output for differential followers.
        
        This is a torque request when using the TorqueCurrentFOC control
        output type, and a duty cycle in all other control types.
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_DUTY_CYCLE.value: "",
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_TORQUE_CURRENT.value: "",
        }
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_DUTY_CYCLE.value, map_filler, "differential_output", float, True, refresh)
    
    def get_differential_closed_loop_proportional_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop proportional component
        
        The portion of the differential closed loop output that is the
        proportional to the error. Alternatively, the p-Contribution of the
        closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopProportionalOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_DC.value: "",
            SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_V.value: "",
            SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_PROPORTIONAL_OUTPUT_DC.value, map_filler, "differential_closed_loop_proportional_output", float, True, refresh)
    
    def get_differential_closed_loop_integrated_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop integrated component
        
        The portion of the differential closed loop output that is
        proportional to the integrated error. Alternatively, the
        i-Contribution of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopIntegratedOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_DC.value: "",
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_V.value: "",
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_INTEGRATED_ACCUM_DC.value, map_filler, "differential_closed_loop_integrated_output", float, True, refresh)
    
    def get_differential_closed_loop_feed_forward(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential Feedforward passed by the user
        
        This is the general feedforward that the user provides for the
        differential closed loop.
        
        Default Rates:
            - CAN 2.0: 100.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopFeedForward Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_DC.value: "",
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_V.value: "",
            SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_MOTOR_OUTPUT_PIDSTATE_DIFF_FEED_FORWARD_DC.value, map_filler, "differential_closed_loop_feed_forward", float, True, refresh)
    
    def get_differential_closed_loop_derivative_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop derivative component
        
        The portion of the differential closed loop output that is the
        proportional to the deriviative the error. Alternatively, the
        d-Contribution of the closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopDerivativeOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_DC.value: "",
            SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_V.value: "",
            SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_DERIVATIVE_OUTPUT_DC.value, map_filler, "differential_closed_loop_derivative_output", float, True, refresh)
    
    def get_differential_closed_loop_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop total output
        
        The total output of the differential closed loop output.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_DC.value: "",
            SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_V.value: "",
            SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_A.value: "",
        }
        return self._common_lookup(SpnValue.PRO_DIFF_PIDOUTPUT_OUTPUT_DC.value, map_filler, "differential_closed_loop_output", float, True, refresh)
    
    def get_differential_closed_loop_reference(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Value that the differential closed loop is targeting
        
        This is the value that the differential closed loop PID controller
        targets.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopReference Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDREF_POSITION.value: "",
            SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDREF_VELOCITY.value: "",
        }
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDREF_POSITION.value, map_filler, "differential_closed_loop_reference", float, True, refresh)
    
    def get_differential_closed_loop_reference_slope(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Derivative of the target that the differential closed loop is
        targeting
        
        This is the change in the closed loop reference. This may be used in
        the feed-forward calculation, the derivative-error, or in application
        of the signage for kS. Typically, this represents the target velocity
        during Motion Magic®.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopReferenceSlope Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_DIFF_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_POSITION.value: "",
            SpnValue.PRO_DIFF_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_VELOCITY.value: "",
        }
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_SLOPE_ECUTIME_REFERENCE_SLOPE_POSITION.value, map_filler, "differential_closed_loop_reference_slope", float, True, refresh)
    
    def get_differential_closed_loop_error(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The difference between target differential reference and current
        measurement
        
        This is the value that is treated as the error in the differential PID
        loop.
        
        Default Rates:
            - CAN 2.0: 4.0 Hz
            - CAN FD: 100.0 Hz (TimeSynced with Pro)
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopError Status Signal object
        :rtype: StatusSignal[float]
        """
        map_filler = lambda: {
            SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDERR_POSITION.value: "",
            SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDERR_VELOCITY.value: "",
        }
        return self._common_lookup(SpnValue.PRO_DIFF_PIDREF_PIDERR_PIDERR_POSITION.value, map_filler, "differential_closed_loop_error", float, True, refresh)
    

    
    @overload
    def set_control(self, request: DutyCycleOut) -> StatusCode:
        """
        Request a specified motor duty cycle.
        
        This control mode will output a proportion of the supplied voltage
        which is supplied by the user.
        
            - DutyCycleOut Parameters: 
                - output: Proportion of supply voltage to apply in fractional units
                          between -1 and +1
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DutyCycleOut
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: TorqueCurrentFOC) -> StatusCode:
        """
        Request a specified motor current (field oriented control).
        
        This control request will drive the motor to the requested motor
        (stator) current value.  This leverages field oriented control (FOC),
        which means greater peak power than what is documented.  This scales
        to torque based on Motor's kT constant.
        
            - TorqueCurrentFOC Parameters: 
                - output: Amount of motor current in Amperes
                - max_abs_duty_cycle: The maximum absolute motor output that can be
                                      applied, which effectively limits the velocity.
                                      For example, 0.50 means no more than 50% output in
                                      either direction.  This is useful for preventing
                                      the motor from spinning to its terminal velocity
                                      when there is no external torque applied unto the
                                      rotor.  Note this is absolute maximum, so the
                                      value should be between zero and one.
                - deadband: Deadband in Amperes.  If torque request is within deadband,
                            the bridge output is neutral. If deadband is set to zero
                            then there is effectively no deadband. Note if deadband is
                            zero, a free spinning motor will spin for quite a while as
                            the firmware attempts to hold the motor's bemf. If user
                            expects motor to cease spinning quickly with a demand of
                            zero, we recommend a deadband of one Ampere. This value will
                            be converted to an integral value of amps.
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: TorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: VoltageOut) -> StatusCode:
        """
        Request a specified voltage.
        
        This control mode will attempt to apply the specified voltage to the
        motor. If the supply voltage is below the requested voltage, the motor
        controller will output the supply voltage.
        
            - VoltageOut Parameters: 
                - output: Voltage to attempt to drive at
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: VoltageOut
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: PositionDutyCycle) -> StatusCode:
        """
        Request PID to target position with duty cycle feedforward.
        
        This control mode will set the motor's position setpoint to the
        position specified by the user. In addition, it will apply an
        additional duty cycle as an arbitrary feedforward value.
        
            - PositionDutyCycle Parameters: 
                - position: Position to drive toward in rotations.
                - velocity: Velocity to drive toward in rotations per second. This is
                            typically used for motion profiles generated by the robot
                            program.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in fractional units between -1 and
                                +1.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: PositionDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: PositionVoltage) -> StatusCode:
        """
        Request PID to target position with voltage feedforward
        
        This control mode will set the motor's position setpoint to the
        position specified by the user. In addition, it will apply an
        additional voltage as an arbitrary feedforward value.
        
            - PositionVoltage Parameters: 
                - position: Position to drive toward in rotations.
                - velocity: Velocity to drive toward in rotations per second. This is
                            typically used for motion profiles generated by the robot
                            program.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in volts
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: PositionVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: PositionTorqueCurrentFOC) -> StatusCode:
        """
        Request PID to target position with torque current feedforward.
        
        This control mode will set the motor's position setpoint to the
        position specified by the user. In addition, it will apply an
        additional torque current as an arbitrary feedforward value.
        
            - PositionTorqueCurrentFOC Parameters: 
                - position: Position to drive toward in rotations.
                - velocity: Velocity to drive toward in rotations per second. This is
                            typically used for motion profiles generated by the robot
                            program.
                - feed_forward: Feedforward to apply in torque current in Amperes.  User
                                can use motor's kT to scale Newton-meter to Amperes.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: PositionTorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: VelocityDutyCycle) -> StatusCode:
        """
        Request PID to target velocity with duty cycle feedforward.
        
        This control mode will set the motor's velocity setpoint to the
        velocity specified by the user. In addition, it will apply an
        additional voltage as an arbitrary feedforward value.
        
            - VelocityDutyCycle Parameters: 
                - velocity: Velocity to drive toward in rotations per second.
                - acceleration: Acceleration to drive toward in rotations per second
                                squared. This is typically used for motion profiles
                                generated by the robot program.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in fractional units between -1 and
                                +1.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: VelocityDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: VelocityVoltage) -> StatusCode:
        """
        Request PID to target velocity with voltage feedforward.
        
        This control mode will set the motor's velocity setpoint to the
        velocity specified by the user. In addition, it will apply an
        additional voltage as an arbitrary feedforward value.
        
            - VelocityVoltage Parameters: 
                - velocity: Velocity to drive toward in rotations per second.
                - acceleration: Acceleration to drive toward in rotations per second
                                squared. This is typically used for motion profiles
                                generated by the robot program.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in volts
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: VelocityVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: VelocityTorqueCurrentFOC) -> StatusCode:
        """
        Request PID to target velocity with torque current feedforward.
        
        This control mode will set the motor's velocity setpoint to the
        velocity specified by the user. In addition, it will apply an
        additional torque current as an arbitrary feedforward value.
        
            - VelocityTorqueCurrentFOC Parameters: 
                - velocity: Velocity to drive toward in rotations per second.
                - acceleration: Acceleration to drive toward in rotations per second
                                squared. This is typically used for motion profiles
                                generated by the robot program.
                - feed_forward: Feedforward to apply in torque current in Amperes.  User
                                can use motor's kT to scale Newton-meter to Amperes.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: VelocityTorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicDutyCycle) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile.  Users can optionally provide a duty cycle feedforward.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the Cruise Velocity, Acceleration, and (optional) Jerk
        specified via the Motion Magic® configuration values.  This control
        mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is duty cycle
        based, so relevant closed-loop gains will use fractional duty cycle
        for the numerator:  +1.0 represents full forward output.
        
            - MotionMagicDutyCycle Parameters: 
                - position: Position to drive toward in rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in fractional units between -1 and
                                +1.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicVoltage) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile.  Users can optionally provide a voltage feedforward.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the Cruise Velocity, Acceleration, and (optional) Jerk
        specified via the Motion Magic® configuration values.  This control
        mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is voltage-based,
        so relevant closed-loop gains will use Volts for the numerator.
        
            - MotionMagicVoltage Parameters: 
                - position: Position to drive toward in rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in volts
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicTorqueCurrentFOC) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile.  Users can optionally provide a torque current feedforward.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the Cruise Velocity, Acceleration, and (optional) Jerk
        specified via the Motion Magic® configuration values.  This control
        mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is based on torque
        current, so relevant closed-loop gains will use Amperes for the
        numerator.
        
            - MotionMagicTorqueCurrentFOC Parameters: 
                - position: Position to drive toward in rotations.
                - feed_forward: Feedforward to apply in torque current in Amperes.  User
                                can use motor's kT to scale Newton-meter to Amperes.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicTorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialDutyCycle) -> StatusCode:
        """
        Request a specified motor duty cycle with a differential position
        closed-loop.
        
        This control mode will output a proportion of the supplied voltage
        which is supplied by the user. It will also set the motor's
        differential position setpoint to the specified position.
        
            - DifferentialDutyCycle Parameters: 
                - target_output: Proportion of supply voltage to apply in fractional
                                 units between -1 and +1
                - differential_position: Differential position to drive towards in
                                         rotations
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialVoltage) -> StatusCode:
        """
        Request a specified voltage with a differential position closed-loop.
        
        This control mode will attempt to apply the specified voltage to the
        motor. If the supply voltage is below the requested voltage, the motor
        controller will output the supply voltage. It will also set the
        motor's differential position setpoint to the specified position.
        
            - DifferentialVoltage Parameters: 
                - target_output: Voltage to attempt to drive at
                - differential_position: Differential position to drive towards in
                                         rotations
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialPositionDutyCycle) -> StatusCode:
        """
        Request PID to target position with a differential position setpoint.
        
        This control mode will set the motor's position setpoint to the
        position specified by the user. It will also set the motor's
        differential position setpoint to the specified position.
        
            - DifferentialPositionDutyCycle Parameters: 
                - target_position: Average position to drive toward in rotations.
                - differential_position: Differential position to drive toward in
                                         rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - target_slot: Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialPositionDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialPositionVoltage) -> StatusCode:
        """
        Request PID to target position with a differential position setpoint
        
        This control mode will set the motor's position setpoint to the
        position specified by the user. It will also set the motor's
        differential position setpoint to the specified position.
        
            - DifferentialPositionVoltage Parameters: 
                - target_position: Average position to drive toward in rotations.
                - differential_position: Differential position to drive toward in
                                         rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - target_slot: Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialPositionVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialVelocityDutyCycle) -> StatusCode:
        """
        Request PID to target velocity with a differential position setpoint.
        
        This control mode will set the motor's velocity setpoint to the
        velocity specified by the user. It will also set the motor's
        differential position setpoint to the specified position.
        
            - DifferentialVelocityDutyCycle Parameters: 
                - target_velocity: Average velocity to drive toward in rotations per
                                   second.
                - differential_position: Differential position to drive toward in
                                         rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - target_slot: Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialVelocityDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialVelocityVoltage) -> StatusCode:
        """
        Request PID to target velocity with a differential position setpoint.
        
        This control mode will set the motor's velocity setpoint to the
        velocity specified by the user. It will also set the motor's
        differential position setpoint to the specified position.
        
            - DifferentialVelocityVoltage Parameters: 
                - target_velocity: Average velocity to drive toward in rotations per
                                   second.
                - differential_position: Differential position to drive toward in
                                         rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - target_slot: Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialVelocityVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialMotionMagicDutyCycle) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile, and PID to a differential position setpoint.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the Cruise Velocity, Acceleration, and (optional) Jerk
        specified via the Motion Magic® configuration values.  This control
        mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is duty cycle
        based, so relevant closed-loop gains will use fractional duty cycle
        for the numerator:  +1.0 represents full forward output.
        
            - DifferentialMotionMagicDutyCycle Parameters: 
                - target_position: Average position to drive toward in rotations.
                - differential_position: Differential position to drive toward in
                                         rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - target_slot: Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialMotionMagicDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialMotionMagicVoltage) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile, and PID to a differential position setpoint.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the Cruise Velocity, Acceleration, and (optional) Jerk
        specified via the Motion Magic® configuration values.  This control
        mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is voltage-based,
        so relevant closed-loop gains will use Volts for the numerator.
        
            - DifferentialMotionMagicVoltage Parameters: 
                - target_position: Average position to drive toward in rotations.
                - differential_position: Differential position to drive toward in
                                         rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - target_slot: Select which gains are applied to the primary controller
                               by selecting the slot.  Use the configuration api to set
                               the gain values for the selected slot before enabling
                               this feature. Slot must be within [0,2].
                - differential_slot: Select which gains are applied to the differential
                                     controller by selecting the slot.  Use the
                                     configuration api to set the gain values for the
                                     selected slot before enabling this feature. Slot
                                     must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DifferentialMotionMagicVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Follower) -> StatusCode:
        """
        Follow the motor output of another Talon.
        
        If Talon is in torque control, the torque is copied - which will
        increase the total torque applied. If Talon is in percent supply
        output control, the duty cycle is matched.  Motor direction either
        matches master's configured direction or opposes it based on
        OpposeMasterDirection.
        
            - Follower Parameters: 
                - master_id: Device ID of the master to follow.
                - oppose_master_direction: Set to false for motor invert to match the
                                           master's configured Invert - which is typical
                                           when master and follower are mechanically
                                           linked and spin in the same direction.  Set
                                           to true for motor invert to oppose the
                                           master's configured Invert - this is typical
                                           where the the master and follower
                                           mechanically spin in opposite directions.
    
        :param request: Control object to request of the device
        :type request: Follower
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: StrictFollower) -> StatusCode:
        """
        Follow the motor output of another Talon while ignoring the master's
        invert setting.
        
        If Talon is in torque control, the torque is copied - which will
        increase the total torque applied. If Talon is in percent supply
        output control, the duty cycle is matched.  Motor direction is
        strictly determined by the configured invert and not the master.  If
        you want motor direction to match or oppose the master, use
        FollowerRequest instead.
        
            - StrictFollower Parameters: 
                - master_id: Device ID of the master to follow.
    
        :param request: Control object to request of the device
        :type request: StrictFollower
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialFollower) -> StatusCode:
        """
        Follow the differential motor output of another Talon.
        
        If Talon is in torque control, the torque is copied - which will
        increase the total torque applied. If Talon is in percent supply
        output control, the duty cycle is matched.  Motor direction either
        matches master's configured direction or opposes it based on
        OpposeMasterDirection.
        
            - DifferentialFollower Parameters: 
                - master_id: Device ID of the differential master to follow.
                - oppose_master_direction: Set to false for motor invert to match the
                                           master's configured Invert - which is typical
                                           when master and follower are mechanically
                                           linked and spin in the same direction.  Set
                                           to true for motor invert to oppose the
                                           master's configured Invert - this is typical
                                           where the the master and follower
                                           mechanically spin in opposite directions.
    
        :param request: Control object to request of the device
        :type request: DifferentialFollower
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DifferentialStrictFollower) -> StatusCode:
        """
        Follow the differential motor output of another Talon while ignoring
        the master's invert setting.
        
        If Talon is in torque control, the torque is copied - which will
        increase the total torque applied. If Talon is in percent supply
        output control, the duty cycle is matched.  Motor direction is
        strictly determined by the configured invert and not the master.  If
        you want motor direction to match or oppose the master, use
        FollowerRequest instead.
        
            - DifferentialStrictFollower Parameters: 
                - master_id: Device ID of the differential master to follow.
    
        :param request: Control object to request of the device
        :type request: DifferentialStrictFollower
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: NeutralOut) -> StatusCode:
        """
        Request neutral output of actuator. The applied brake type is
        determined by the NeutralMode configuration.
        
            - NeutralOut Parameters: 
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: NeutralOut
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: CoastOut) -> StatusCode:
        """
        Request coast neutral output of actuator.  The bridge is disabled and
        the rotor is allowed to coast.
        
            - CoastOut Parameters: 
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: CoastOut
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: StaticBrake) -> StatusCode:
        """
        Applies full neutral-brake by shorting motor leads together.
        
            - StaticBrake Parameters: 
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: StaticBrake
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MusicTone) -> StatusCode:
        """
        Plays a single tone at the user specified frequency.
        
            - MusicTone Parameters: 
                - audio_frequency: Sound frequency to play.  A value of zero will
                                   silence the device. The effective frequency range is
                                   10-20000 Hz.  Any nonzero frequency less than 10 Hz
                                   will be capped to 10 Hz.  Any frequency above 20 kHz
                                   will be capped to 20 kHz.
    
        :param request: Control object to request of the device
        :type request: MusicTone
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicVelocityDutyCycle) -> StatusCode:
        """
        Requests Motion Magic® to target a final velocity using a motion
        profile.  This allows smooth transitions between velocity set points. 
        Users can optionally provide a duty cycle feedforward.
        
        Motion Magic® Velocity produces a motion profile in real-time while
        attempting to honor the specified Acceleration and (optional) Jerk. 
        This control mode does not use the CruiseVelocity, Expo_kV, or Expo_kA
        configs.
        
        If the specified acceleration is zero, the Acceleration under Motion
        Magic® configuration parameter is used instead.  This allows for
        runtime adjustment of acceleration for advanced users.  Jerk is also
        specified in the Motion Magic® persistent configuration values.  If
        Jerk is set to zero, Motion Magic® will produce a trapezoidal
        acceleration profile.
        
        Target velocity can also be changed on-the-fly and Motion Magic® will
        do its best to adjust the profile.  This control mode is duty cycle
        based, so relevant closed-loop gains will use fractional duty cycle
        for the numerator:  +1.0 represents full forward output.
        
            - MotionMagicVelocityDutyCycle Parameters: 
                - velocity: Target velocity to drive toward in rotations per second. 
                            This can be changed on-the fly.
                - acceleration: This is the absolute Acceleration to use generating the
                                profile.  If this parameter is zero, the Acceleration
                                persistent configuration parameter is used instead.
                                Acceleration is in rotations per second squared.  If
                                nonzero, the signage does not matter as the absolute
                                value is used.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in fractional units between -1 and
                                +1.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicVelocityDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicVelocityTorqueCurrentFOC) -> StatusCode:
        """
        Requests Motion Magic® to target a final velocity using a motion
        profile.  This allows smooth transitions between velocity set points. 
        Users can optionally provide a torque feedforward.
        
        Motion Magic® Velocity produces a motion profile in real-time while
        attempting to honor the specified Acceleration and (optional) Jerk. 
        This control mode does not use the CruiseVelocity, Expo_kV, or Expo_kA
        configs.
        
        If the specified acceleration is zero, the Acceleration under Motion
        Magic® configuration parameter is used instead.  This allows for
        runtime adjustment of acceleration for advanced users.  Jerk is also
        specified in the Motion Magic® persistent configuration values.  If
        Jerk is set to zero, Motion Magic® will produce a trapezoidal
        acceleration profile.
        
        Target velocity can also be changed on-the-fly and Motion Magic® will
        do its best to adjust the profile.  This control mode is based on
        torque current, so relevant closed-loop gains will use Amperes for the
        numerator.
        
            - MotionMagicVelocityTorqueCurrentFOC Parameters: 
                - velocity: Target velocity to drive toward in rotations per second. 
                            This can be changed on-the fly.
                - acceleration: This is the absolute Acceleration to use generating the
                                profile.  If this parameter is zero, the Acceleration
                                persistent configuration parameter is used instead.
                                Acceleration is in rotations per second squared.  If
                                nonzero, the signage does not matter as the absolute
                                value is used.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in torque current in Amperes.  User
                                can use motor's kT to scale Newton-meter to Amperes.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicVelocityTorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicVelocityVoltage) -> StatusCode:
        """
        Requests Motion Magic® to target a final velocity using a motion
        profile.  This allows smooth transitions between velocity set points. 
        Users can optionally provide a voltage feedforward.
        
        Motion Magic® Velocity produces a motion profile in real-time while
        attempting to honor the specified Acceleration and (optional) Jerk. 
        This control mode does not use the CruiseVelocity, Expo_kV, or Expo_kA
        configs.
        
        If the specified acceleration is zero, the Acceleration under Motion
        Magic® configuration parameter is used instead.  This allows for
        runtime adjustment of acceleration for advanced users.  Jerk is also
        specified in the Motion Magic® persistent configuration values.  If
        Jerk is set to zero, Motion Magic® will produce a trapezoidal
        acceleration profile.
        
        Target velocity can also be changed on-the-fly and Motion Magic® will
        do its best to adjust the profile.  This control mode is
        voltage-based, so relevant closed-loop gains will use Volts for the
        numerator.
        
            - MotionMagicVelocityVoltage Parameters: 
                - velocity: Target velocity to drive toward in rotations per second. 
                            This can be changed on-the fly.
                - acceleration: This is the absolute Acceleration to use generating the
                                profile.  If this parameter is zero, the Acceleration
                                persistent configuration parameter is used instead.
                                Acceleration is in rotations per second squared.  If
                                nonzero, the signage does not matter as the absolute
                                value is used.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in volts
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicVelocityVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicExpoDutyCycle) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using an exponential
        motion profile.  Users can optionally provide a duty cycle
        feedforward.
        
        Motion Magic® Expo produces a motion profile in real-time while
        attempting to honor the Cruise Velocity (optional) and the mechanism
        kV and kA, specified via the Motion Magic® configuration values.  Note
        that unlike the slot gains, the Expo_kV and Expo_kA configs are always
        in output units of Volts.
        
        Setting Cruise Velocity to 0 will allow the profile to run to the max
        possible velocity based on Expo_kV.  This control mode does not use
        the Acceleration or Jerk configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is duty cycle
        based, so relevant closed-loop gains will use fractional duty cycle
        for the numerator:  +1.0 represents full forward output.
        
            - MotionMagicExpoDutyCycle Parameters: 
                - position: Position to drive toward in rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in fractional units between -1 and
                                +1.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicExpoDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicExpoVoltage) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using an exponential
        motion profile.  Users can optionally provide a voltage feedforward.
        
        Motion Magic® Expo produces a motion profile in real-time while
        attempting to honor the Cruise Velocity (optional) and the mechanism
        kV and kA, specified via the Motion Magic® configuration values.  Note
        that unlike the slot gains, the Expo_kV and Expo_kA configs are always
        in output units of Volts.
        
        Setting Cruise Velocity to 0 will allow the profile to run to the max
        possible velocity based on Expo_kV.  This control mode does not use
        the Acceleration or Jerk configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is voltage-based,
        so relevant closed-loop gains will use Volts for the numerator.
        
            - MotionMagicExpoVoltage Parameters: 
                - position: Position to drive toward in rotations.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in volts
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicExpoVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: MotionMagicExpoTorqueCurrentFOC) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using an exponential
        motion profile.  Users can optionally provide a torque current
        feedforward.
        
        Motion Magic® Expo produces a motion profile in real-time while
        attempting to honor the Cruise Velocity (optional) and the mechanism
        kV and kA, specified via the Motion Magic® configuration values.  Note
        that unlike the slot gains, the Expo_kV and Expo_kA configs are always
        in output units of Volts.
        
        Setting Cruise Velocity to 0 will allow the profile to run to the max
        possible velocity based on Expo_kV.  This control mode does not use
        the Acceleration or Jerk configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is based on torque
        current, so relevant closed-loop gains will use Amperes for the
        numerator.
        
            - MotionMagicExpoTorqueCurrentFOC Parameters: 
                - position: Position to drive toward in rotations.
                - feed_forward: Feedforward to apply in torque current in Amperes.  User
                                can use motor's kT to scale Newton-meter to Amperes.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: MotionMagicExpoTorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DynamicMotionMagicDutyCycle) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile.  This dynamic request allows runtime changes to Cruise
        Velocity, Acceleration, and Jerk.  Users can optionally provide a duty
        cycle feedforward.  This control requires use of a CANivore.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the specified Cruise Velocity, Acceleration, and (optional)
        Jerk.  This control mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile. This control mode is duty cycle based,
        so relevant closed-loop gains will use fractional duty cycle for the
        numerator:  +1.0 represents full forward output.
        
            - DynamicMotionMagicDutyCycle Parameters: 
                - position: Position to drive toward in rotations.
                - velocity: Cruise velocity for profiling.  The signage does not matter
                            as the device will use the absolute value for profile
                            generation.
                - acceleration: Acceleration for profiling.  The signage does not matter
                                as the device will use the absolute value for profile
                                generation
                - jerk: Jerk for profiling.  The signage does not matter as the device
                        will use the absolute value for profile generation.
                        
                        Jerk is optional; if this is set to zero, then Motion Magic®
                        will not apply a Jerk limit.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in fractional units between -1 and
                                +1.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DynamicMotionMagicDutyCycle
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DynamicMotionMagicVoltage) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile.  This dynamic request allows runtime changes to Cruise
        Velocity, Acceleration, and Jerk.  Users can optionally provide a
        voltage feedforward.  This control requires use of a CANivore.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the specified Cruise Velocity, Acceleration, and (optional)
        Jerk.  This control mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile.  This control mode is voltage-based,
        so relevant closed-loop gains will use Volts for the numerator.
        
            - DynamicMotionMagicVoltage Parameters: 
                - position: Position to drive toward in rotations.
                - velocity: Cruise velocity for profiling.  The signage does not matter
                            as the device will use the absolute value for profile
                            generation.
                - acceleration: Acceleration for profiling.  The signage does not matter
                                as the device will use the absolute value for profile
                                generation.
                - jerk: Jerk for profiling.  The signage does not matter as the device
                        will use the absolute value for profile generation.
                        
                        Jerk is optional; if this is set to zero, then Motion Magic®
                        will not apply a Jerk limit.
                - enable_foc: Set to true to use FOC commutation (requires Phoenix Pro),
                              which increases peak power by ~15%. Set to false to use
                              trapezoidal commutation.
                              
                              FOC improves motor performance by leveraging torque
                              (current) control.  However, this may be inconvenient for
                              applications that require specifying duty cycle or
                              voltage.  CTR-Electronics has developed a hybrid method
                              that combines the performances gains of FOC while still
                              allowing applications to provide duty cycle or voltage
                              demand.  This not to be confused with simple sinusoidal
                              control or phase voltage control which lacks the
                              performance gains.
                - feed_forward: Feedforward to apply in volts
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_brake_dur_neutral: Set to true to static-brake the rotor when
                                              output is zero (or within deadband).  Set
                                              to false to use the NeutralMode
                                              configuration setting (default). This flag
                                              exists to provide the fundamental behavior
                                              of this control when output is zero, which
                                              is to provide 0V to the motor.
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DynamicMotionMagicVoltage
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: DynamicMotionMagicTorqueCurrentFOC) -> StatusCode:
        """
        Requests Motion Magic® to target a final position using a motion
        profile.  This dynamic request allows runtime changes to Cruise
        Velocity, Acceleration, and Jerk.  Users can optionally provide a
        torque current feedforward.  This control requires use of a CANivore.
        
        Motion Magic® produces a motion profile in real-time while attempting
        to honor the specified Cruise Velocity, Acceleration, and (optional)
        Jerk.  This control mode does not use the Expo_kV or Expo_kA configs.
        
        Target position can be changed on-the-fly and Motion Magic® will do
        its best to adjust the profile. This control mode is based on torque
        current, so relevant closed-loop gains will use Amperes for the
        numerator.
        
            - DynamicMotionMagicTorqueCurrentFOC Parameters: 
                - position: Position to drive toward in rotations.
                - velocity: Cruise velocity for profiling.  The signage does not matter
                            as the device will use the absolute value for profile
                            generation.
                - acceleration: Acceleration for profiling.  The signage does not matter
                                as the device will use the absolute value for profile
                                generation.
                - jerk: Jerk for profiling.  The signage does not matter as the device
                        will use the absolute value for profile generation.
                        
                        Jerk is optional; if this is set to zero, then Motion Magic®
                        will not apply a Jerk limit.
                - feed_forward: Feedforward to apply in torque current in Amperes.  User
                                can use motor's kT to scale Newton-meter to Amperes.
                - slot: Select which gains are applied by selecting the slot.  Use the
                        configuration api to set the gain values for the selected slot
                        before enabling this feature. Slot must be within [0,2].
                - override_coast_dur_neutral: Set to true to coast the rotor when output
                                              is zero (or within deadband).  Set to
                                              false to use the NeutralMode configuration
                                              setting (default). This flag exists to
                                              provide the fundamental behavior of this
                                              control when output is zero, which is to
                                              provide 0A (zero torque).
                - limit_forward_motion: Set to true to force forward limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - limit_reverse_motion: Set to true to force reverse limiting.  This
                                        allows users to use other limit switch sensors
                                        connected to robot controller.  This also allows
                                        use of active sensors that require external
                                        power.
                - ignore_hardware_limits: Set to true to ignore hardware limit switches
                                          and the LimitForwardMotion and
                                          LimitReverseMotion parameters, instead
                                          allowing motion.
                                          
                                          This can be useful on mechanisms such as an
                                          intake/feeder, where a limit switch stops
                                          motion while intaking but should be ignored
                                          when feeding to a shooter.
                                          
                                          The hardware limit faults and
                                          Forward/ReverseLimit signals will still report
                                          the values of the limit switches regardless of
                                          this parameter.
                - use_timesync: Set to true to delay applying this control request until
                                a timesync boundary (requires Phoenix Pro and CANivore).
                                This eliminates the impact of nondeterministic network
                                delays in exchange for a larger but deterministic
                                control latency.
                                
                                This requires setting the ControlTimesyncFreqHz config
                                in MotorOutputConfigs. Additionally, when this is
                                enabled, the UpdateFreqHz of this request should be set
                                to 0 Hz.
    
        :param request: Control object to request of the device
        :type request: DynamicMotionMagicTorqueCurrentFOC
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_DutyCycleOut_Position) -> StatusCode:
        """
        Differential control with duty cycle average target and position
        difference target.
        
            - Diff_DutyCycleOut_Position Parameters: 
                - average_request: Average DutyCycleOut request of the mechanism.
                - differential_request: Differential PositionDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_DutyCycleOut_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_PositionDutyCycle_Position) -> StatusCode:
        """
        Differential control with position average target and position
        difference target using dutycycle control.
        
            - Diff_PositionDutyCycle_Position Parameters: 
                - average_request: Average PositionDutyCycle request of the mechanism.
                - differential_request: Differential PositionDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_PositionDutyCycle_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VelocityDutyCycle_Position) -> StatusCode:
        """
        Differential control with velocity average target and position
        difference target using dutycycle control.
        
            - Diff_VelocityDutyCycle_Position Parameters: 
                - average_request: Average VelocityDutyCYcle request of the mechanism.
                - differential_request: Differential PositionDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VelocityDutyCycle_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_MotionMagicDutyCycle_Position) -> StatusCode:
        """
        Differential control with Motion Magic® average target and position
        difference target using dutycycle control.
        
            - Diff_MotionMagicDutyCycle_Position Parameters: 
                - average_request: Average MotionMagicDutyCycle request of the
                                   mechanism.
                - differential_request: Differential PositionDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_MotionMagicDutyCycle_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_DutyCycleOut_Velocity) -> StatusCode:
        """
        Differential control with duty cycle average target and velocity
        difference target.
        
            - Diff_DutyCycleOut_Velocity Parameters: 
                - average_request: Average DutyCycleOut request of the mechanism.
                - differential_request: Differential VelocityDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_DutyCycleOut_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_PositionDutyCycle_Velocity) -> StatusCode:
        """
        Differential control with position average target and velocity
        difference target using dutycycle control.
        
            - Diff_PositionDutyCycle_Velocity Parameters: 
                - average_request: Average PositionDutyCycle request of the mechanism.
                - differential_request: Differential VelocityDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_PositionDutyCycle_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VelocityDutyCycle_Velocity) -> StatusCode:
        """
        Differential control with velocity average target and velocity
        difference target using dutycycle control.
        
            - Diff_VelocityDutyCycle_Velocity Parameters: 
                - average_request: Average VelocityDutyCycle request of the mechanism.
                - differential_request: Differential VelocityDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VelocityDutyCycle_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_MotionMagicDutyCycle_Velocity) -> StatusCode:
        """
        Differential control with Motion Magic® average target and velocity
        difference target using dutycycle control.
        
            - Diff_MotionMagicDutyCycle_Velocity Parameters: 
                - average_request: Average MotionMagicDutyCycle request of the
                                   mechanism.
                - differential_request: Differential VelocityDutyCycle request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_MotionMagicDutyCycle_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VoltageOut_Position) -> StatusCode:
        """
        Differential control with voltage average target and position
        difference target.
        
            - Diff_VoltageOut_Position Parameters: 
                - average_request: Average VoltageOut request of the mechanism.
                - differential_request: Differential PositionVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VoltageOut_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_PositionVoltage_Position) -> StatusCode:
        """
        Differential control with position average target and position
        difference target using voltage control.
        
            - Diff_PositionVoltage_Position Parameters: 
                - average_request: Average PositionVoltage request of the mechanism.
                - differential_request: Differential PositionVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_PositionVoltage_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VelocityVoltage_Position) -> StatusCode:
        """
        Differential control with velocity average target and position
        difference target using voltage control.
        
            - Diff_VelocityVoltage_Position Parameters: 
                - average_request: Average VelocityVoltage request of the mechanism.
                - differential_request: Differential PositionVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VelocityVoltage_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_MotionMagicVoltage_Position) -> StatusCode:
        """
        Differential control with Motion Magic® average target and position
        difference target using voltage control.
        
            - Diff_MotionMagicVoltage_Position Parameters: 
                - average_request: Average MotionMagicVoltage request of the mechanism.
                - differential_request: Differential PositionVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_MotionMagicVoltage_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VoltageOut_Velocity) -> StatusCode:
        """
        Differential control with voltage average target and velocity
        difference target.
        
            - Diff_VoltageOut_Velocity Parameters: 
                - average_request: Average VoltageOut request of the mechanism.
                - differential_request: Differential VelocityVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VoltageOut_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_PositionVoltage_Velocity) -> StatusCode:
        """
        Differential control with position average target and velocity
        difference target using voltage control.
        
            - Diff_PositionVoltage_Velocity Parameters: 
                - average_request: Average PositionVoltage request of the mechanism.
                - differential_request: Differential VelocityVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_PositionVoltage_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VelocityVoltage_Velocity) -> StatusCode:
        """
        Differential control with velocity average target and velocity
        difference target using voltage control.
        
            - Diff_VelocityVoltage_Velocity Parameters: 
                - average_request: Average VelocityVoltage request of the mechanism.
                - differential_request: Differential VelocityVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VelocityVoltage_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_MotionMagicVoltage_Velocity) -> StatusCode:
        """
        Differential control with Motion Magic® average target and velocity
        difference target using voltage control.
        
            - Diff_MotionMagicVoltage_Velocity Parameters: 
                - average_request: Average MotionMagicVoltage request of the mechanism.
                - differential_request: Differential VelocityVoltage request of the
                                        mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_MotionMagicVoltage_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_TorqueCurrentFOC_Position) -> StatusCode:
        """
        Differential control with torque current average target and position
        difference target.
        
            - Diff_TorqueCurrentFOC_Position Parameters: 
                - average_request: Average TorqueCurrentFOC request of the mechanism.
                - differential_request: Differential PositionTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_TorqueCurrentFOC_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_PositionTorqueCurrentFOC_Position) -> StatusCode:
        """
        Differential control with position average target and position
        difference target using torque current control.
        
            - Diff_PositionTorqueCurrentFOC_Position Parameters: 
                - average_request: Average PositionTorqueCurrentFOC request of the
                                   mechanism.
                - differential_request: Differential PositionTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_PositionTorqueCurrentFOC_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VelocityTorqueCurrentFOC_Position) -> StatusCode:
        """
        Differential control with velocity average target and position
        difference target using torque current control.
        
            - Diff_VelocityTorqueCurrentFOC_Position Parameters: 
                - average_request: Average VelocityTorqueCurrentFOC request of the
                                   mechanism.
                - differential_request: Differential PositionTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VelocityTorqueCurrentFOC_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_MotionMagicTorqueCurrentFOC_Position) -> StatusCode:
        """
        Differential control with Motion Magic® average target and position
        difference target using torque current control.
        
            - Diff_MotionMagicTorqueCurrentFOC_Position Parameters: 
                - average_request: Average MotionMagicTorqueCurrentFOC request of the
                                   mechanism.
                - differential_request: Differential PositionTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_MotionMagicTorqueCurrentFOC_Position
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_TorqueCurrentFOC_Velocity) -> StatusCode:
        """
        Differential control with torque current average target and velocity
        difference target.
        
            - Diff_TorqueCurrentFOC_Velocity Parameters: 
                - average_request: Average TorqueCurrentFOC request of the mechanism.
                - differential_request: Differential VelocityTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_TorqueCurrentFOC_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_PositionTorqueCurrentFOC_Velocity) -> StatusCode:
        """
        Differential control with position average target and velocity
        difference target using torque current control.
        
            - Diff_PositionTorqueCurrentFOC_Velocity Parameters: 
                - average_request: Average PositionTorqueCurrentFOC request of the
                                   mechanism.
                - differential_request: Differential VelocityTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_PositionTorqueCurrentFOC_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_VelocityTorqueCurrentFOC_Velocity) -> StatusCode:
        """
        Differential control with velocity average target and velocity
        difference target using torque current control.
        
            - Diff_VelocityTorqueCurrentFOC_Velocity Parameters: 
                - average_request: Average VelocityTorqueCurrentFOC request of the
                                   mechanism.
                - differential_request: Differential VelocityTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_VelocityTorqueCurrentFOC_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...
    
    @overload
    def set_control(self, request: Diff_MotionMagicTorqueCurrentFOC_Velocity) -> StatusCode:
        """
        Differential control with Motion Magic® average target and velocity
        difference target using torque current control.
        
            - Diff_MotionMagicTorqueCurrentFOC_Velocity Parameters: 
                - average_request: Average MotionMagicTorqueCurrentFOC request of the
                                   mechanism.
                - differential_request: Differential VelocityTorqueCurrentFOC request of
                                        the mechanism.
    
        :param request: Control object to request of the device
        :type request: Diff_MotionMagicTorqueCurrentFOC_Velocity
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...

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
        if isinstance(request, (DutyCycleOut, TorqueCurrentFOC, VoltageOut, PositionDutyCycle, PositionVoltage, PositionTorqueCurrentFOC, VelocityDutyCycle, VelocityVoltage, VelocityTorqueCurrentFOC, MotionMagicDutyCycle, MotionMagicVoltage, MotionMagicTorqueCurrentFOC, DifferentialDutyCycle, DifferentialVoltage, DifferentialPositionDutyCycle, DifferentialPositionVoltage, DifferentialVelocityDutyCycle, DifferentialVelocityVoltage, DifferentialMotionMagicDutyCycle, DifferentialMotionMagicVoltage, Follower, StrictFollower, DifferentialFollower, DifferentialStrictFollower, NeutralOut, CoastOut, StaticBrake, MusicTone, MotionMagicVelocityDutyCycle, MotionMagicVelocityTorqueCurrentFOC, MotionMagicVelocityVoltage, MotionMagicExpoDutyCycle, MotionMagicExpoVoltage, MotionMagicExpoTorqueCurrentFOC, DynamicMotionMagicDutyCycle, DynamicMotionMagicVoltage, DynamicMotionMagicTorqueCurrentFOC, Diff_DutyCycleOut_Position, Diff_PositionDutyCycle_Position, Diff_VelocityDutyCycle_Position, Diff_MotionMagicDutyCycle_Position, Diff_DutyCycleOut_Velocity, Diff_PositionDutyCycle_Velocity, Diff_VelocityDutyCycle_Velocity, Diff_MotionMagicDutyCycle_Velocity, Diff_VoltageOut_Position, Diff_PositionVoltage_Position, Diff_VelocityVoltage_Position, Diff_MotionMagicVoltage_Position, Diff_VoltageOut_Velocity, Diff_PositionVoltage_Velocity, Diff_VelocityVoltage_Velocity, Diff_MotionMagicVoltage_Velocity, Diff_TorqueCurrentFOC_Position, Diff_PositionTorqueCurrentFOC_Position, Diff_VelocityTorqueCurrentFOC_Position, Diff_MotionMagicTorqueCurrentFOC_Position, Diff_TorqueCurrentFOC_Velocity, Diff_PositionTorqueCurrentFOC_Velocity, Diff_VelocityTorqueCurrentFOC_Velocity, Diff_MotionMagicTorqueCurrentFOC_Velocity)):
            return self._set_control_private(request)
        return StatusCode.NOT_SUPPORTED

    
    def set_position(self, new_value: rotation, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Sets the mechanism position of the device in mechanism rotations.
        
        :param new_value: Value to set to. Units are in rotations.
        :type new_value: rotation
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.set_position(new_value, timeout_seconds)
    
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
    
    def clear_sticky_fault_proc_temp(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Processor temperature exceeded limit
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_proc_temp(timeout_seconds)
    
    def clear_sticky_fault_device_temp(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device temperature exceeded limit
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_device_temp(timeout_seconds)
    
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
    
    def clear_sticky_fault_bridge_brownout(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Bridge was disabled most likely due to supply
        voltage dropping too low.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_bridge_brownout(timeout_seconds)
    
    def clear_sticky_fault_remote_sensor_reset(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor has reset.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_remote_sensor_reset(timeout_seconds)
    
    def clear_sticky_fault_missing_differential_fx(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote Talon used for differential control is
        not present on CAN Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_missing_differential_fx(timeout_seconds)
    
    def clear_sticky_fault_remote_sensor_pos_overflow(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor position has overflowed. Because
        of the nature of remote sensors, it is possible for the remote sensor
        position to overflow beyond what is supported by the status signal
        frame. However, this is rare and cannot occur over the course of an
        FRC match under normal use.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_remote_sensor_pos_overflow(timeout_seconds)
    
    def clear_sticky_fault_over_supply_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage has exceeded the maximum voltage
        rating of device.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_over_supply_v(timeout_seconds)
    
    def clear_sticky_fault_unstable_supply_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage is unstable.  Ensure you are using
        a battery and current limited power supply.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_unstable_supply_v(timeout_seconds)
    
    def clear_sticky_fault_reverse_hard_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Reverse limit switch has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_reverse_hard_limit(timeout_seconds)
    
    def clear_sticky_fault_forward_hard_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Forward limit switch has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_forward_hard_limit(timeout_seconds)
    
    def clear_sticky_fault_reverse_soft_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Reverse soft limit has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_reverse_soft_limit(timeout_seconds)
    
    def clear_sticky_fault_forward_soft_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Forward soft limit has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_forward_soft_limit(timeout_seconds)
    
    def clear_sticky_fault_missing_soft_limit_remote(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote soft limit device is not present on CAN
        Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_missing_soft_limit_remote(timeout_seconds)
    
    def clear_sticky_fault_missing_hard_limit_remote(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote limit switch device is not present on
        CAN Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_missing_hard_limit_remote(timeout_seconds)
    
    def clear_sticky_fault_remote_sensor_data_invalid(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor's data is no longer trusted.
        This can happen if the remote sensor disappears from the CAN bus or if
        the remote sensor indicates its data is no longer valid, such as when
        a CANcoder's magnet strength falls into the "red" range.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_remote_sensor_data_invalid(timeout_seconds)
    
    def clear_sticky_fault_fused_sensor_out_of_sync(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor used for fusion has fallen out
        of sync to the local sensor. A re-synchronization has occurred, which
        may cause a discontinuity. This typically happens if there is
        significant slop in the mechanism, or if the RotorToSensorRatio
        configuration parameter is incorrect.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_fused_sensor_out_of_sync(timeout_seconds)
    
    def clear_sticky_fault_stator_curr_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Stator current limit occured.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_stator_curr_limit(timeout_seconds)
    
    def clear_sticky_fault_supply_curr_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply current limit occured.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_supply_curr_limit(timeout_seconds)
    
    def clear_sticky_fault_using_fused_cancoder_while_unlicensed(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Using Fused CANcoder feature while unlicensed.
        Device has fallen back to remote CANcoder.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_using_fused_cancoder_while_unlicensed(timeout_seconds)
    
    def clear_sticky_fault_static_brake_disabled(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Static brake was momentarily disabled due to
        excessive braking current while disabled.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        return self.configurator.clear_sticky_fault_static_brake_disabled(timeout_seconds)

