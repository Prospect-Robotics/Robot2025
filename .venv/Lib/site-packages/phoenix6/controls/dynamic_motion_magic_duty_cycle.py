"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
from phoenix6.units import *
import ctypes


class DynamicMotionMagicDutyCycle:
    """
    Requires Phoenix Pro and CANivore;
    Requests Motion Magic® to target a final position using a motion profile.  This
    dynamic request allows runtime changes to Cruise Velocity, Acceleration, and
    Jerk.  Users can optionally provide a duty cycle feedforward.  This control
    requires use of a CANivore.
    
    Motion Magic® produces a motion profile in real-time while attempting to honor
    the specified Cruise Velocity, Acceleration, and (optional) Jerk.  This control
    mode does not use the Expo_kV or Expo_kA configs.
    
    Target position can be changed on-the-fly and Motion Magic® will do its best to
    adjust the profile. This control mode is duty cycle based, so relevant
    closed-loop gains will use fractional duty cycle for the numerator:  +1.0
    represents full forward output.
    
    :param position:    Position to drive toward in rotations.
    :type position: rotation
    :param velocity:    Cruise velocity for profiling.  The signage does not matter
                        as the device will use the absolute value for profile
                        generation.
    :type velocity: rotations_per_second
    :param acceleration:    Acceleration for profiling.  The signage does not matter
                            as the device will use the absolute value for profile
                            generation
    :type acceleration: rotations_per_second_squared
    :param jerk:    Jerk for profiling.  The signage does not matter as the device
                    will use the absolute value for profile generation.
                    
                    Jerk is optional; if this is set to zero, then Motion Magic®
                    will not apply a Jerk limit.
    :type jerk: rotations_per_second_cubed
    :param enable_foc:    Set to true to use FOC commutation (requires Phoenix Pro),
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
    :type enable_foc: bool
    :param feed_forward:    Feedforward to apply in fractional units between -1 and
                            +1.
    :type feed_forward: float
    :param slot:    Select which gains are applied by selecting the slot.  Use the
                    configuration api to set the gain values for the selected slot
                    before enabling this feature. Slot must be within [0,2].
    :type slot: int
    :param override_brake_dur_neutral:    Set to true to static-brake the rotor when
                                          output is zero (or within deadband).  Set
                                          to false to use the NeutralMode
                                          configuration setting (default). This flag
                                          exists to provide the fundamental behavior
                                          of this control when output is zero, which
                                          is to provide 0V to the motor.
    :type override_brake_dur_neutral: bool
    :param limit_forward_motion:    Set to true to force forward limiting.  This
                                    allows users to use other limit switch sensors
                                    connected to robot controller.  This also allows
                                    use of active sensors that require external
                                    power.
    :type limit_forward_motion: bool
    :param limit_reverse_motion:    Set to true to force reverse limiting.  This
                                    allows users to use other limit switch sensors
                                    connected to robot controller.  This also allows
                                    use of active sensors that require external
                                    power.
    :type limit_reverse_motion: bool
    :param ignore_hardware_limits:    Set to true to ignore hardware limit switches
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
    :type ignore_hardware_limits: bool
    :param use_timesync:    Set to true to delay applying this control request until
                            a timesync boundary (requires Phoenix Pro and CANivore).
                            This eliminates the impact of nondeterministic network
                            delays in exchange for a larger but deterministic
                            control latency.
                            
                            This requires setting the ControlTimesyncFreqHz config
                            in MotorOutputConfigs. Additionally, when this is
                            enabled, the UpdateFreqHz of this request should be set
                            to 0 Hz.
    :type use_timesync: bool
    """

    def __init__(self, position: rotation, velocity: rotations_per_second, acceleration: rotations_per_second_squared, jerk: rotations_per_second_cubed, enable_foc: bool = True, feed_forward: float = 0.0, slot: int = 0, override_brake_dur_neutral: bool = False, limit_forward_motion: bool = False, limit_reverse_motion: bool = False, ignore_hardware_limits: bool = False, use_timesync: bool = False):
        self._name = "DynamicMotionMagicDutyCycle"
        self.update_freq_hz: hertz = 100.0
        """
        The period at which this control will update at.
        This is designated in Hertz, with a minimum of 20 Hz
        (every 50 ms) and a maximum of 1000 Hz (every 1 ms).

        If this field is set to 0 Hz, the control request will
        be sent immediately as a one-shot frame. This may be useful
        for advanced applications that require outputs to be
        synchronized with data acquisition. In this case, we
        recommend not exceeding 50 ms between control calls.
        """
        
        self.position = position
        """
        Position to drive toward in rotations.
        """
        self.velocity = velocity
        """
        Cruise velocity for profiling.  The signage does not matter as the device will
        use the absolute value for profile generation.
        """
        self.acceleration = acceleration
        """
        Acceleration for profiling.  The signage does not matter as the device will use
        the absolute value for profile generation
        """
        self.jerk = jerk
        """
        Jerk for profiling.  The signage does not matter as the device will use the
        absolute value for profile generation.
        
        Jerk is optional; if this is set to zero, then Motion Magic® will not apply a
        Jerk limit.
        """
        self.enable_foc = enable_foc
        """
        Set to true to use FOC commutation (requires Phoenix Pro), which increases peak
        power by ~15%. Set to false to use trapezoidal commutation.
        
        FOC improves motor performance by leveraging torque (current) control.  However,
        this may be inconvenient for applications that require specifying duty cycle or
        voltage.  CTR-Electronics has developed a hybrid method that combines the
        performances gains of FOC while still allowing applications to provide duty
        cycle or voltage demand.  This not to be confused with simple sinusoidal control
        or phase voltage control which lacks the performance gains.
        """
        self.feed_forward = feed_forward
        """
        Feedforward to apply in fractional units between -1 and +1.
        """
        self.slot = slot
        """
        Select which gains are applied by selecting the slot.  Use the configuration api
        to set the gain values for the selected slot before enabling this feature. Slot
        must be within [0,2].
        """
        self.override_brake_dur_neutral = override_brake_dur_neutral
        """
        Set to true to static-brake the rotor when output is zero (or within deadband). 
        Set to false to use the NeutralMode configuration setting (default). This flag
        exists to provide the fundamental behavior of this control when output is zero,
        which is to provide 0V to the motor.
        """
        self.limit_forward_motion = limit_forward_motion
        """
        Set to true to force forward limiting.  This allows users to use other limit
        switch sensors connected to robot controller.  This also allows use of active
        sensors that require external power.
        """
        self.limit_reverse_motion = limit_reverse_motion
        """
        Set to true to force reverse limiting.  This allows users to use other limit
        switch sensors connected to robot controller.  This also allows use of active
        sensors that require external power.
        """
        self.ignore_hardware_limits = ignore_hardware_limits
        """
        Set to true to ignore hardware limit switches and the LimitForwardMotion and
        LimitReverseMotion parameters, instead allowing motion.
        
        This can be useful on mechanisms such as an intake/feeder, where a limit switch
        stops motion while intaking but should be ignored when feeding to a shooter.
        
        The hardware limit faults and Forward/ReverseLimit signals will still report the
        values of the limit switches regardless of this parameter.
        """
        self.use_timesync = use_timesync
        """
        Set to true to delay applying this control request until a timesync boundary
        (requires Phoenix Pro and CANivore). This eliminates the impact of
        nondeterministic network delays in exchange for a larger but deterministic
        control latency.
        
        This requires setting the ControlTimesyncFreqHz config in MotorOutputConfigs.
        Additionally, when this is enabled, the UpdateFreqHz of this request should be
        set to 0 Hz.
        """

    @property
    def name(self) -> str:
        """
        Gets the name of this control request.

        :returns: Name of the control request
        :rtype: str
        """
        return self._name

    def __str__(self) -> str:
        ss = []
        ss.append("Control: DynamicMotionMagicDutyCycle")
        ss.append("    position: " + str(self.position) + " rotations")
        ss.append("    velocity: " + str(self.velocity) + " rotations per second")
        ss.append("    acceleration: " + str(self.acceleration) + " rotations per second²")
        ss.append("    jerk: " + str(self.jerk) + " rotations per second³")
        ss.append("    enable_foc: " + str(self.enable_foc))
        ss.append("    feed_forward: " + str(self.feed_forward) + " fractional")
        ss.append("    slot: " + str(self.slot))
        ss.append("    override_brake_dur_neutral: " + str(self.override_brake_dur_neutral))
        ss.append("    limit_forward_motion: " + str(self.limit_forward_motion))
        ss.append("    limit_reverse_motion: " + str(self.limit_reverse_motion))
        ss.append("    ignore_hardware_limits: " + str(self.ignore_hardware_limits))
        ss.append("    use_timesync: " + str(self.use_timesync))
        return "\n".join(ss)

    def _send_request(self, network: str, device_hash: int) -> StatusCode:
        """
        Sends this request out over CAN bus to the device for
        the device to apply.

        :param network: Network to send request over
        :type network: str
        :param device_hash: Device to send request to
        :type device_hash: int
        :returns: Status of the send operation
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlDynamicMotionMagicDutyCycle(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, self.position, self.velocity, self.acceleration, self.jerk, self.enable_foc, self.feed_forward, self.slot, self.override_brake_dur_neutral, self.limit_forward_motion, self.limit_reverse_motion, self.ignore_hardware_limits, self.use_timesync))

    
    def with_position(self, new_position: rotation) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's position parameter and returns itself for
        method-chaining and easier to use request API.
    
        Position to drive toward in rotations.
    
        :param new_position: Parameter to modify
        :type new_position: rotation
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.position = new_position
        return self
    
    def with_velocity(self, new_velocity: rotations_per_second) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's velocity parameter and returns itself for
        method-chaining and easier to use request API.
    
        Cruise velocity for profiling.  The signage does not matter as the device will
        use the absolute value for profile generation.
    
        :param new_velocity: Parameter to modify
        :type new_velocity: rotations_per_second
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.velocity = new_velocity
        return self
    
    def with_acceleration(self, new_acceleration: rotations_per_second_squared) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's acceleration parameter and returns itself for
        method-chaining and easier to use request API.
    
        Acceleration for profiling.  The signage does not matter as the device will use
        the absolute value for profile generation
    
        :param new_acceleration: Parameter to modify
        :type new_acceleration: rotations_per_second_squared
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.acceleration = new_acceleration
        return self
    
    def with_jerk(self, new_jerk: rotations_per_second_cubed) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's jerk parameter and returns itself for
        method-chaining and easier to use request API.
    
        Jerk for profiling.  The signage does not matter as the device will use the
        absolute value for profile generation.
        
        Jerk is optional; if this is set to zero, then Motion Magic® will not apply a
        Jerk limit.
    
        :param new_jerk: Parameter to modify
        :type new_jerk: rotations_per_second_cubed
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.jerk = new_jerk
        return self
    
    def with_enable_foc(self, new_enable_foc: bool) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's enable_foc parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to use FOC commutation (requires Phoenix Pro), which increases peak
        power by ~15%. Set to false to use trapezoidal commutation.
        
        FOC improves motor performance by leveraging torque (current) control.  However,
        this may be inconvenient for applications that require specifying duty cycle or
        voltage.  CTR-Electronics has developed a hybrid method that combines the
        performances gains of FOC while still allowing applications to provide duty
        cycle or voltage demand.  This not to be confused with simple sinusoidal control
        or phase voltage control which lacks the performance gains.
    
        :param new_enable_foc: Parameter to modify
        :type new_enable_foc: bool
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.enable_foc = new_enable_foc
        return self
    
    def with_feed_forward(self, new_feed_forward: float) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's feed_forward parameter and returns itself for
        method-chaining and easier to use request API.
    
        Feedforward to apply in fractional units between -1 and +1.
    
        :param new_feed_forward: Parameter to modify
        :type new_feed_forward: float
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.feed_forward = new_feed_forward
        return self
    
    def with_slot(self, new_slot: int) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's slot parameter and returns itself for
        method-chaining and easier to use request API.
    
        Select which gains are applied by selecting the slot.  Use the configuration api
        to set the gain values for the selected slot before enabling this feature. Slot
        must be within [0,2].
    
        :param new_slot: Parameter to modify
        :type new_slot: int
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.slot = new_slot
        return self
    
    def with_override_brake_dur_neutral(self, new_override_brake_dur_neutral: bool) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's override_brake_dur_neutral parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to static-brake the rotor when output is zero (or within deadband). 
        Set to false to use the NeutralMode configuration setting (default). This flag
        exists to provide the fundamental behavior of this control when output is zero,
        which is to provide 0V to the motor.
    
        :param new_override_brake_dur_neutral: Parameter to modify
        :type new_override_brake_dur_neutral: bool
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.override_brake_dur_neutral = new_override_brake_dur_neutral
        return self
    
    def with_limit_forward_motion(self, new_limit_forward_motion: bool) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's limit_forward_motion parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to force forward limiting.  This allows users to use other limit
        switch sensors connected to robot controller.  This also allows use of active
        sensors that require external power.
    
        :param new_limit_forward_motion: Parameter to modify
        :type new_limit_forward_motion: bool
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.limit_forward_motion = new_limit_forward_motion
        return self
    
    def with_limit_reverse_motion(self, new_limit_reverse_motion: bool) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's limit_reverse_motion parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to force reverse limiting.  This allows users to use other limit
        switch sensors connected to robot controller.  This also allows use of active
        sensors that require external power.
    
        :param new_limit_reverse_motion: Parameter to modify
        :type new_limit_reverse_motion: bool
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.limit_reverse_motion = new_limit_reverse_motion
        return self
    
    def with_ignore_hardware_limits(self, new_ignore_hardware_limits: bool) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's ignore_hardware_limits parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to ignore hardware limit switches and the LimitForwardMotion and
        LimitReverseMotion parameters, instead allowing motion.
        
        This can be useful on mechanisms such as an intake/feeder, where a limit switch
        stops motion while intaking but should be ignored when feeding to a shooter.
        
        The hardware limit faults and Forward/ReverseLimit signals will still report the
        values of the limit switches regardless of this parameter.
    
        :param new_ignore_hardware_limits: Parameter to modify
        :type new_ignore_hardware_limits: bool
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.ignore_hardware_limits = new_ignore_hardware_limits
        return self
    
    def with_use_timesync(self, new_use_timesync: bool) -> 'DynamicMotionMagicDutyCycle':
        """
        Modifies this Control Request's use_timesync parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to delay applying this control request until a timesync boundary
        (requires Phoenix Pro and CANivore). This eliminates the impact of
        nondeterministic network delays in exchange for a larger but deterministic
        control latency.
        
        This requires setting the ControlTimesyncFreqHz config in MotorOutputConfigs.
        Additionally, when this is enabled, the UpdateFreqHz of this request should be
        set to 0 Hz.
    
        :param new_use_timesync: Parameter to modify
        :type new_use_timesync: bool
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.use_timesync = new_use_timesync
        return self

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'DynamicMotionMagicDutyCycle':
        """
        Sets the period at which this control will update at.
        This is designated in Hertz, with a minimum of 20 Hz
        (every 50 ms) and a maximum of 1000 Hz (every 1 ms).

        If this field is set to 0 Hz, the control request will
        be sent immediately as a one-shot frame. This may be useful
        for advanced applications that require outputs to be
        synchronized with data acquisition. In this case, we
        recommend not exceeding 50 ms between control calls.

        :param new_update_freq_hz: Parameter to modify
        :type new_update_freq_hz: hertz
        :returns: Itself
        :rtype: DynamicMotionMagicDutyCycle
        """
        self.update_freq_hz = new_update_freq_hz
        return self

    @property
    def control_info(self) -> dict:
        """
        Gets information about this control request.

        :returns: Dictonary of control parameter names and corresponding applied values
        :rtype: dict
        """
        control_info = {}
        control_info["name"] = self._name
        control_info["position"] = self.position
        control_info["velocity"] = self.velocity
        control_info["acceleration"] = self.acceleration
        control_info["jerk"] = self.jerk
        control_info["enable_foc"] = self.enable_foc
        control_info["feed_forward"] = self.feed_forward
        control_info["slot"] = self.slot
        control_info["override_brake_dur_neutral"] = self.override_brake_dur_neutral
        control_info["limit_forward_motion"] = self.limit_forward_motion
        control_info["limit_reverse_motion"] = self.limit_reverse_motion
        control_info["ignore_hardware_limits"] = self.ignore_hardware_limits
        control_info["use_timesync"] = self.use_timesync
        return control_info
