"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_signal import *
from phoenix6.units import *
from phoenix6.signals.spn_enums import ForwardLimitValue, ReverseLimitValue, AppliedRotorPolarityValue, ControlModeValue, MotionMagicIsRunningValue, DeviceEnableValue, MotorOutputStatusValue, DifferentialControlModeValue, BridgeOutputValue, ConnectedMotorValue

class HasTalonSignals():
    """
    Contains all status signals available for devices that support Talon signals.
    """
    def get_version_major(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Major Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionMajor Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_version_minor(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Minor Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionMinor Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_version_bugfix(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Bugfix Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionBugfix Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_version_build(self, refresh: bool = True) -> StatusSignal[int]:
        """
        App Build Version number.
        
            - Minimum Value: 0
            - Maximum Value: 255
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: VersionBuild Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_version(self, refresh: bool = True) -> StatusSignal[int]:
        """
        Full Version of firmware in device.  The format is a four byte value.
        
            - Minimum Value: 0
            - Maximum Value: 4294967295
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Version Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_fault_field(self, refresh: bool = True) -> StatusSignal[int]:
        """
        Integer representing all fault flags reported by the device.
        
        These are device specific and are not used directly in typical
        applications. Use the signal specific GetFault_*() methods instead.
        
            - Minimum Value: 0
            - Maximum Value: 4294967295
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: FaultField Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
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
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFaultField Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_motor_voltage(self, refresh: bool = True) -> StatusSignal[volt]:
        """
        The applied (output) motor voltage.
        
            - Minimum Value: -40.96
            - Maximum Value: 40.95
            - Default Value: 0
            - Units: V
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        pass
    
    def get_forward_limit(self, refresh: bool = True) -> StatusSignal[ForwardLimitValue]:
        """
        Forward Limit Pin.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ForwardLimit Status Signal Object
        :rtype: StatusSignal[ForwardLimitValue]
        """
        pass
    
    def get_reverse_limit(self, refresh: bool = True) -> StatusSignal[ReverseLimitValue]:
        """
        Reverse Limit Pin.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ReverseLimit Status Signal Object
        :rtype: StatusSignal[ReverseLimitValue]
        """
        pass
    
    def get_applied_rotor_polarity(self, refresh: bool = True) -> StatusSignal[AppliedRotorPolarityValue]:
        """
        The applied rotor polarity as seen from the front of the motor.  This
        typically is determined by the Inverted config, but can be overridden
        if using Follower features.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AppliedRotorPolarity Status Signal Object
        :rtype: StatusSignal[AppliedRotorPolarityValue]
        """
        pass
    
    def get_duty_cycle(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The applied motor duty cycle.
        
            - Minimum Value: -2.0
            - Maximum Value: 1.9990234375
            - Default Value: 0
            - Units: fractional
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DutyCycle Status Signal Object
        :rtype: StatusSignal[float]
        """
        pass
    
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
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: TorqueCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        pass
    
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
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StatorCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        pass
    
    def get_supply_current(self, refresh: bool = True) -> StatusSignal[ampere]:
        """
        Measured supply side current.
        
            - Minimum Value: -327.68
            - Maximum Value: 327.66
            - Default Value: 0
            - Units: A
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: SupplyCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        pass
    
    def get_supply_voltage(self, refresh: bool = True) -> StatusSignal[volt]:
        """
        Measured supply voltage to the device.
        
            - Minimum Value: 4
            - Maximum Value: 29.575
            - Default Value: 4
            - Units: V
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: SupplyVoltage Status Signal Object
        :rtype: StatusSignal[volt]
        """
        pass
    
    def get_device_temp(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of device.
        
        This is the temperature that the device measures itself to be at.
        Similar to Processor Temperature.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DeviceTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        pass
    
    def get_processor_temp(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of the processor.
        
        This is the temperature that the processor measures itself to be at.
        Similar to Device Temperature.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ProcessorTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        pass
    
    def get_rotor_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the motor rotor. This velocity is not affected by any
        feedback configs.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RotorVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        pass
    
    def get_rotor_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Position of the motor rotor. This position is only affected by the
        RotorOffset config and calls to setPosition.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: RotorPosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        pass
    
    def get_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Velocity of the device in mechanism rotations per second. This can be
        the velocity of a remote sensor and is affected by the
        RotorToSensorRatio and SensorToMechanismRatio configs.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Velocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        pass
    
    def get_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Position of the device in mechanism rotations. This can be the
        position of a remote sensor and is affected by the RotorToSensorRatio
        and SensorToMechanismRatio configs, as well as calls to setPosition.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Position Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        pass
    
    def get_acceleration(self, refresh: bool = True) -> StatusSignal[rotations_per_second_squared]:
        """
        Acceleration of the device in mechanism rotations per second². This
        can be the acceleration of a remote sensor and is affected by the
        RotorToSensorRatio and SensorToMechanismRatio configs.
        
            - Minimum Value: -2048.0
            - Maximum Value: 2047.75
            - Default Value: 0
            - Units: rotations per second²
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Acceleration Status Signal Object
        :rtype: StatusSignal[rotations_per_second_squared]
        """
        pass
    
    def get_control_mode(self, refresh: bool = True) -> StatusSignal[ControlModeValue]:
        """
        The active control mode of the motor controller.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ControlMode Status Signal Object
        :rtype: StatusSignal[ControlModeValue]
        """
        pass
    
    def get_motion_magic_is_running(self, refresh: bool = True) -> StatusSignal[MotionMagicIsRunningValue]:
        """
        Check if Motion Magic® is running.  This is equivalent to checking
        that the reported control mode is a Motion Magic® based mode.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotionMagicIsRunning Status Signal Object
        :rtype: StatusSignal[MotionMagicIsRunningValue]
        """
        pass
    
    def get_device_enable(self, refresh: bool = True) -> StatusSignal[DeviceEnableValue]:
        """
        Indicates if device is actuator enabled.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DeviceEnable Status Signal Object
        :rtype: StatusSignal[DeviceEnableValue]
        """
        pass
    
    def get_closed_loop_slot(self, refresh: bool = True) -> StatusSignal[int]:
        """
        The slot that the closed-loop PID is using.
        
            - Minimum Value: 0
            - Maximum Value: 2
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopSlot Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_motor_output_status(self, refresh: bool = True) -> StatusSignal[MotorOutputStatusValue]:
        """
        Assess the status of the motor output with respect to load and supply.
        
        This routine can be used to determine the general status of motor
        commutation.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorOutputStatus Status Signal Object
        :rtype: StatusSignal[MotorOutputStatusValue]
        """
        pass
    
    def get_differential_control_mode(self, refresh: bool = True) -> StatusSignal[DifferentialControlModeValue]:
        """
        The active control mode of the differential controller.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialControlMode Status Signal Object
        :rtype: StatusSignal[DifferentialControlModeValue]
        """
        pass
    
    def get_differential_average_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Average component of the differential velocity of device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialAverageVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        pass
    
    def get_differential_average_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Average component of the differential position of device.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialAveragePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        pass
    
    def get_differential_difference_velocity(self, refresh: bool = True) -> StatusSignal[rotations_per_second]:
        """
        Difference component of the differential velocity of device.
        
            - Minimum Value: -512.0
            - Maximum Value: 511.998046875
            - Default Value: 0
            - Units: rotations per second
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialDifferenceVelocity Status Signal Object
        :rtype: StatusSignal[rotations_per_second]
        """
        pass
    
    def get_differential_difference_position(self, refresh: bool = True) -> StatusSignal[rotation]:
        """
        Difference component of the differential position of device.
        
            - Minimum Value: -16384.0
            - Maximum Value: 16383.999755859375
            - Default Value: 0
            - Units: rotations
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialDifferencePosition Status Signal Object
        :rtype: StatusSignal[rotation]
        """
        pass
    
    def get_differential_closed_loop_slot(self, refresh: bool = True) -> StatusSignal[int]:
        """
        The slot that the closed-loop differential PID is using.
        
            - Minimum Value: 0
            - Maximum Value: 2
            - Default Value: 0
            - Units: 
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopSlot Status Signal Object
        :rtype: StatusSignal[int]
        """
        pass
    
    def get_motor_kt(self, refresh: bool = True) -> StatusSignal[newton_meters_per_ampere]:
        """
        The torque constant (K_T) of the motor.
        
            - Minimum Value: 0.0
            - Maximum Value: 0.025500000000000002
            - Default Value: 0
            - Units: Nm/A
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorKT Status Signal Object
        :rtype: StatusSignal[newton_meters_per_ampere]
        """
        pass
    
    def get_motor_kv(self, refresh: bool = True) -> StatusSignal[rpm_per_volt]:
        """
        The velocity constant (K_V) of the motor.
        
            - Minimum Value: 0.0
            - Maximum Value: 2047.0
            - Default Value: 0
            - Units: RPM/V
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorKV Status Signal Object
        :rtype: StatusSignal[rpm_per_volt]
        """
        pass
    
    def get_motor_stall_current(self, refresh: bool = True) -> StatusSignal[ampere]:
        """
        The stall current of the motor at 12 V output.
        
            - Minimum Value: 0.0
            - Maximum Value: 1023.0
            - Default Value: 0
            - Units: A
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: MotorStallCurrent Status Signal Object
        :rtype: StatusSignal[ampere]
        """
        pass
    
    def get_bridge_output(self, refresh: bool = True) -> StatusSignal[BridgeOutputValue]:
        """
        The applied output of the bridge.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: BridgeOutput Status Signal Object
        :rtype: StatusSignal[BridgeOutputValue]
        """
        pass
    
    def get_is_pro_licensed(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Whether the device is Phoenix Pro licensed.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: IsProLicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_ancillary_device_temp(self, refresh: bool = True) -> StatusSignal[celsius]:
        """
        Temperature of device from second sensor.
        
        Newer versions of Talon have multiple temperature measurement methods.
        
            - Minimum Value: 0.0
            - Maximum Value: 255.0
            - Default Value: 0
            - Units: ℃
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: AncillaryDeviceTemp Status Signal Object
        :rtype: StatusSignal[celsius]
        """
        pass
    
    def get_connected_motor(self, refresh: bool = True) -> StatusSignal[ConnectedMotorValue]:
        """
        The type of motor attached to the Talon.
        
        This can be used to determine what motor is attached to the Talon FX. 
        Return will be "Unknown" if firmware is too old or device is not
        present.
        
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ConnectedMotor Status Signal Object
        :rtype: StatusSignal[ConnectedMotorValue]
        """
        pass
    
    def get_fault_hardware(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_Hardware Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_hardware(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Hardware fault occurred
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_Hardware Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_proc_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Processor temperature exceeded limit
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ProcTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_proc_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Processor temperature exceeded limit
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ProcTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_device_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device temperature exceeded limit
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_DeviceTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_device_temp(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device temperature exceeded limit
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_DeviceTemp Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_undervoltage(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_Undervoltage Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_undervoltage(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device supply voltage dropped to near brownout levels
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_Undervoltage Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_boot_during_enable(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BootDuringEnable Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_boot_during_enable(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Device boot while detecting the enable signal
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BootDuringEnable Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_unlicensed_feature_in_use(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_UnlicensedFeatureInUse Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_unlicensed_feature_in_use(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        An unlicensed feature is in use, device may not behave as expected.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_UnlicensedFeatureInUse Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_bridge_brownout(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bridge was disabled most likely due to supply voltage dropping too
        low.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_BridgeBrownout Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_bridge_brownout(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Bridge was disabled most likely due to supply voltage dropping too
        low.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_BridgeBrownout Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_remote_sensor_reset(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor has reset.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_RemoteSensorReset Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_remote_sensor_reset(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor has reset.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_RemoteSensorReset Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_missing_differential_fx(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote Talon used for differential control is not present on CAN
        Bus.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_MissingDifferentialFX Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_missing_differential_fx(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote Talon used for differential control is not present on CAN
        Bus.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_MissingDifferentialFX Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_remote_sensor_pos_overflow(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor position has overflowed. Because of the nature of
        remote sensors, it is possible for the remote sensor position to
        overflow beyond what is supported by the status signal frame. However,
        this is rare and cannot occur over the course of an FRC match under
        normal use.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_RemoteSensorPosOverflow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_remote_sensor_pos_overflow(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor position has overflowed. Because of the nature of
        remote sensors, it is possible for the remote sensor position to
        overflow beyond what is supported by the status signal frame. However,
        this is rare and cannot occur over the course of an FRC match under
        normal use.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_RemoteSensorPosOverflow Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_over_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage has exceeded the maximum voltage rating of device.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_OverSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_over_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage has exceeded the maximum voltage rating of device.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_OverSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_unstable_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage is unstable.  Ensure you are using a battery and
        current limited power supply.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_UnstableSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_unstable_supply_v(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply Voltage is unstable.  Ensure you are using a battery and
        current limited power supply.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_UnstableSupplyV Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_reverse_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ReverseHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_reverse_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ReverseHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_forward_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ForwardHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_forward_hard_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward limit switch has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ForwardHardLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_reverse_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ReverseSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_reverse_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Reverse soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ReverseSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_forward_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_ForwardSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_forward_soft_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Forward soft limit has been asserted.  Output is set to neutral.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_ForwardSoftLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_missing_soft_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote soft limit device is not present on CAN Bus.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_MissingSoftLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_missing_soft_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote soft limit device is not present on CAN Bus.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_MissingSoftLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_missing_hard_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote limit switch device is not present on CAN Bus.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_MissingHardLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_missing_hard_limit_remote(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote limit switch device is not present on CAN Bus.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_MissingHardLimitRemote Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_remote_sensor_data_invalid(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor's data is no longer trusted. This can happen if the
        remote sensor disappears from the CAN bus or if the remote sensor
        indicates its data is no longer valid, such as when a CANcoder's
        magnet strength falls into the "red" range.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_RemoteSensorDataInvalid Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_remote_sensor_data_invalid(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor's data is no longer trusted. This can happen if the
        remote sensor disappears from the CAN bus or if the remote sensor
        indicates its data is no longer valid, such as when a CANcoder's
        magnet strength falls into the "red" range.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_RemoteSensorDataInvalid Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_fused_sensor_out_of_sync(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor used for fusion has fallen out of sync to the local
        sensor. A re-synchronization has occurred, which may cause a
        discontinuity. This typically happens if there is significant slop in
        the mechanism, or if the RotorToSensorRatio configuration parameter is
        incorrect.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_FusedSensorOutOfSync Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_fused_sensor_out_of_sync(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        The remote sensor used for fusion has fallen out of sync to the local
        sensor. A re-synchronization has occurred, which may cause a
        discontinuity. This typically happens if there is significant slop in
        the mechanism, or if the RotorToSensorRatio configuration parameter is
        incorrect.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_FusedSensorOutOfSync Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_stator_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Stator current limit occured.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_StatorCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_stator_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Stator current limit occured.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_StatorCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_supply_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply current limit occured.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_SupplyCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_supply_curr_limit(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Supply current limit occured.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_SupplyCurrLimit Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_using_fused_cancoder_while_unlicensed(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Using Fused CANcoder feature while unlicensed. Device has fallen back
        to remote CANcoder.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_UsingFusedCANcoderWhileUnlicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_using_fused_cancoder_while_unlicensed(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Using Fused CANcoder feature while unlicensed. Device has fallen back
        to remote CANcoder.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_UsingFusedCANcoderWhileUnlicensed Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_fault_static_brake_disabled(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Static brake was momentarily disabled due to excessive braking current
        while disabled.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: Fault_StaticBrakeDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_sticky_fault_static_brake_disabled(self, refresh: bool = True) -> StatusSignal[bool]:
        """
        Static brake was momentarily disabled due to excessive braking current
        while disabled.
        
            - Default Value: False
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: StickyFault_StaticBrakeDisabled Status Signal Object
        :rtype: StatusSignal[bool]
        """
        pass
    
    def get_closed_loop_proportional_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop proportional component
        
        The portion of the closed loop output that is the proportional to the
        error. Alternatively, the p-Contribution of the closed loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopProportionalOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_integrated_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop integrated component
        
        The portion of the closed loop output that is proportional to the
        integrated error. Alternatively, the i-Contribution of the closed loop
        output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopIntegratedOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_feed_forward(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Feedforward passed by the user
        
        This is the general feedforward that the user provides for the closed
        loop.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopFeedForward Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_derivative_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop derivative component
        
        The portion of the closed loop output that is the proportional to the
        deriviative the error. Alternatively, the d-Contribution of the closed
        loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopDerivativeOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Closed loop total output
        
        The total output of the closed loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_reference(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Value that the closed loop is targeting
        
        This is the value that the closed loop PID controller targets.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopReference Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_reference_slope(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Derivative of the target that the closed loop is targeting
        
        This is the change in the closed loop reference. This may be used in
        the feed-forward calculation, the derivative-error, or in application
        of the signage for kS. Typically, this represents the target velocity
        during Motion Magic®.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopReferenceSlope Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_closed_loop_error(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The difference between target reference and current measurement
        
        This is the value that is treated as the error in the PID loop.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: ClosedLoopError Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The calculated motor output for differential followers.
        
        This is a torque request when using the TorqueCurrentFOC control
        output type, and a duty cycle in all other control types.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_proportional_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop proportional component
        
        The portion of the differential closed loop output that is the
        proportional to the error. Alternatively, the p-Contribution of the
        closed loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopProportionalOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_integrated_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop integrated component
        
        The portion of the differential closed loop output that is
        proportional to the integrated error. Alternatively, the
        i-Contribution of the closed loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopIntegratedOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_feed_forward(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential Feedforward passed by the user
        
        This is the general feedforward that the user provides for the
        differential closed loop.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopFeedForward Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_derivative_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop derivative component
        
        The portion of the differential closed loop output that is the
        proportional to the deriviative the error. Alternatively, the
        d-Contribution of the closed loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopDerivativeOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_output(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Differential closed loop total output
        
        The total output of the differential closed loop output.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopOutput Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_reference(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Value that the differential closed loop is targeting
        
        This is the value that the differential closed loop PID controller
        targets.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopReference Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_reference_slope(self, refresh: bool = True) -> StatusSignal[float]:
        """
        Derivative of the target that the differential closed loop is
        targeting
        
        This is the change in the closed loop reference. This may be used in
        the feed-forward calculation, the derivative-error, or in application
        of the signage for kS. Typically, this represents the target velocity
        during Motion Magic®.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopReferenceSlope Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    def get_differential_closed_loop_error(self, refresh: bool = True) -> StatusSignal[float]:
        """
        The difference between target differential reference and current
        measurement
        
        This is the value that is treated as the error in the differential PID
        loop.
        
        This refreshes and returns a cached StatusSignal object.
        
        :param refresh: Whether to refresh the StatusSignal before returning it; defaults to true
        :type refresh: bool
        :returns: DifferentialClosedLoopError Status Signal object
        :rtype: StatusSignal[float]
        """
        pass
    
    

    
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
        pass
    
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
        pass
    
    def clear_sticky_fault_hardware(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Hardware fault occurred
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_proc_temp(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Processor temperature exceeded limit
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_device_temp(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device temperature exceeded limit
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_undervoltage(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device supply voltage dropped to near brownout
        levels
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_boot_during_enable(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device boot while detecting the enable signal
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_unlicensed_feature_in_use(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: An unlicensed feature is in use, device may not
        behave as expected.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_bridge_brownout(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Bridge was disabled most likely due to supply
        voltage dropping too low.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_remote_sensor_reset(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor has reset.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_missing_differential_fx(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote Talon used for differential control is
        not present on CAN Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
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
        pass
    
    def clear_sticky_fault_over_supply_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage has exceeded the maximum voltage
        rating of device.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_unstable_supply_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage is unstable.  Ensure you are using
        a battery and current limited power supply.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_reverse_hard_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Reverse limit switch has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_forward_hard_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Forward limit switch has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_reverse_soft_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Reverse soft limit has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_forward_soft_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Forward soft limit has been asserted.  Output is
        set to neutral.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_missing_soft_limit_remote(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote soft limit device is not present on CAN
        Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_missing_hard_limit_remote(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote limit switch device is not present on
        CAN Bus.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
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
        pass
    
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
        pass
    
    def clear_sticky_fault_stator_curr_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Stator current limit occured.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_supply_curr_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply current limit occured.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_using_fused_cancoder_while_unlicensed(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Using Fused CANcoder feature while unlicensed.
        Device has fallen back to remote CANcoder.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass
    
    def clear_sticky_fault_static_brake_disabled(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Static brake was momentarily disabled due to
        excessive braking current while disabled.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
        pass

