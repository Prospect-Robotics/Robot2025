"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_signal import *
from phoenix6.units import *
from typing import overload
from phoenix6.status_code import StatusCode
from phoenix6.hardware.parent_device import SupportsSendRequest
from phoenix6.controls.duty_cycle_out import DutyCycleOut
from phoenix6.controls.voltage_out import VoltageOut
from phoenix6.controls.position_duty_cycle import PositionDutyCycle
from phoenix6.controls.position_voltage import PositionVoltage
from phoenix6.controls.velocity_duty_cycle import VelocityDutyCycle
from phoenix6.controls.velocity_voltage import VelocityVoltage
from phoenix6.controls.motion_magic_duty_cycle import MotionMagicDutyCycle
from phoenix6.controls.motion_magic_voltage import MotionMagicVoltage
from phoenix6.controls.motion_magic_velocity_duty_cycle import MotionMagicVelocityDutyCycle
from phoenix6.controls.motion_magic_velocity_voltage import MotionMagicVelocityVoltage
from phoenix6.controls.motion_magic_expo_duty_cycle import MotionMagicExpoDutyCycle
from phoenix6.controls.motion_magic_expo_voltage import MotionMagicExpoVoltage
from phoenix6.controls.dynamic_motion_magic_duty_cycle import DynamicMotionMagicDutyCycle
from phoenix6.controls.dynamic_motion_magic_voltage import DynamicMotionMagicVoltage
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
from phoenix6.controls.static_brake import StaticBrake
from phoenix6.controls.neutral_out import NeutralOut
from phoenix6.controls.coast_out import CoastOut
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

class HasTalonControls():
    """
    Contains all control functions available for devices that support Talon
    controls.
    """
    
    
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
        pass
    

