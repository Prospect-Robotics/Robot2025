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
from phoenix6.controls.torque_current_foc import TorqueCurrentFOC
from phoenix6.controls.position_torque_current_foc import PositionTorqueCurrentFOC
from phoenix6.controls.velocity_torque_current_foc import VelocityTorqueCurrentFOC
from phoenix6.controls.motion_magic_torque_current_foc import MotionMagicTorqueCurrentFOC
from phoenix6.controls.motion_magic_velocity_torque_current_foc import MotionMagicVelocityTorqueCurrentFOC
from phoenix6.controls.motion_magic_expo_torque_current_foc import MotionMagicExpoTorqueCurrentFOC
from phoenix6.controls.dynamic_motion_magic_torque_current_foc import DynamicMotionMagicTorqueCurrentFOC
from phoenix6.controls.compound.diff_torque_current_foc_position import Diff_TorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_position_torque_current_foc_position import Diff_PositionTorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_velocity_torque_current_foc_position import Diff_VelocityTorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_motion_magic_torque_current_foc_position import Diff_MotionMagicTorqueCurrentFOC_Position
from phoenix6.controls.compound.diff_torque_current_foc_velocity import Diff_TorqueCurrentFOC_Velocity
from phoenix6.controls.compound.diff_position_torque_current_foc_velocity import Diff_PositionTorqueCurrentFOC_Velocity
from phoenix6.controls.compound.diff_velocity_torque_current_foc_velocity import Diff_VelocityTorqueCurrentFOC_Velocity
from phoenix6.controls.compound.diff_motion_magic_torque_current_foc_velocity import Diff_MotionMagicTorqueCurrentFOC_Velocity

class SupportsFOC():
    """
    Requires Phoenix Pro; Contains all FOC-exclusive control functions available for
    devices that support FOC.
    """
    
    
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
        pass
    

