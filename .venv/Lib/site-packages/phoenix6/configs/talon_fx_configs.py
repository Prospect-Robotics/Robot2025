"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.configs.config_groups import *
from phoenix6.configs.parent_configurator import ParentConfigurator
from phoenix6.hardware.device_identifier import DeviceIdentifier
from phoenix6.status_code import StatusCode
from phoenix6.units import *


class TalonFXConfiguration:
    """
    Class description for the Talon FX integrated motor controller.

    This handles the configurations for TalonFX
    """

    def __init__(self):

        self.future_proof_configs: bool = True
        """
        True if we should factory default newer unsupported configs,
        false to leave newer unsupported configs alone.

        This flag addresses a corner case where the device may have
        firmware with newer configs that didn't exist when this
        version of the API was built. If this occurs and this
        flag is true, unsupported new configs will be factory
        defaulted to avoid unexpected behavior.

        This is also the behavior in Phoenix 5, so this flag
        is defaulted to true to match.
        """

        
        self.motor_output: MotorOutputConfigs = MotorOutputConfigs()
        """
        Configs that directly affect motor output.
        
        Includes motor invert, neutral mode, and other features related to
        motor output.
        """
        
        
        self.current_limits: CurrentLimitsConfigs = CurrentLimitsConfigs()
        """
        Configs that directly affect current limiting features.
        
        Contains the supply/stator current limit thresholds and whether to
        enable them.
        """
        
        
        self.voltage: VoltageConfigs = VoltageConfigs()
        """
        Configs that affect Voltage control types.
        
        Includes peak output voltages and other configs affecting voltage
        measurements.
        """
        
        
        self.torque_current: TorqueCurrentConfigs = TorqueCurrentConfigs()
        """
        Configs that affect Torque Current control types.
        
        Includes the maximum and minimum applied torque output and the neutral
        deadband used during TorqueCurrentFOC requests.
        """
        
        
        self.feedback: FeedbackConfigs = FeedbackConfigs()
        """
        Configs that affect the feedback of this motor controller.
        
        Includes feedback sensor source, any offsets for the feedback sensor,
        and various ratios to describe the relationship between the sensor and
        the mechanism for closed looping.
        """
        
        
        self.differential_sensors: DifferentialSensorsConfigs = DifferentialSensorsConfigs()
        """
        Configs related to sensors used for differential control of a
        mechanism.
        
        Includes the differential sensor sources and IDs.
        """
        
        
        self.differential_constants: DifferentialConstantsConfigs = DifferentialConstantsConfigs()
        """
        Configs related to constants used for differential control of a
        mechanism.
        
        Includes the differential peak outputs.
        """
        
        
        self.open_loop_ramps: OpenLoopRampsConfigs = OpenLoopRampsConfigs()
        """
        Configs that affect the open-loop control of this motor controller.
        
        Open-loop ramp rates for the various control types.
        """
        
        
        self.closed_loop_ramps: ClosedLoopRampsConfigs = ClosedLoopRampsConfigs()
        """
        Configs that affect the closed-loop control of this motor controller.
        
        Closed-loop ramp rates for the various control types.
        """
        
        
        self.hardware_limit_switch: HardwareLimitSwitchConfigs = HardwareLimitSwitchConfigs()
        """
        Configs that change how the motor controller behaves under different
        limit switch states.
        
        Includes configs such as enabling limit switches, configuring the
        remote sensor ID, the source, and the position to set on limit.
        """
        
        
        self.audio: AudioConfigs = AudioConfigs()
        """
        Configs that affect audible components of the device.
        
        Includes configuration for the beep on boot.
        """
        
        
        self.software_limit_switch: SoftwareLimitSwitchConfigs = SoftwareLimitSwitchConfigs()
        """
        Configs that affect how software-limit switches behave.
        
        Includes enabling software-limit switches and the threshold at which
        they are tripped.
        """
        
        
        self.motion_magic: MotionMagicConfigs = MotionMagicConfigs()
        """
        Configs for Motion Magic®.
        
        Includes Velocity, Acceleration, Jerk, and Expo parameters.
        """
        
        
        self.custom_params: CustomParamsConfigs = CustomParamsConfigs()
        """
        Custom Params.
        
        Custom paramaters that have no real impact on controller.
        """
        
        
        self.closed_loop_general: ClosedLoopGeneralConfigs = ClosedLoopGeneralConfigs()
        """
        Configs that affect general behavior during closed-looping.
        
        Includes Continuous Wrap features.
        """
        
        
        self.slot0: Slot0Configs = Slot0Configs()
        """
        Gains for the specified slot.
        
        If this slot is selected, these gains are used in closed loop control
        requests.
        """
        
        
        self.slot1: Slot1Configs = Slot1Configs()
        """
        Gains for the specified slot.
        
        If this slot is selected, these gains are used in closed loop control
        requests.
        """
        
        
        self.slot2: Slot2Configs = Slot2Configs()
        """
        Gains for the specified slot.
        
        If this slot is selected, these gains are used in closed loop control
        requests.
        """
        
    
    def with_motor_output(self, new_motor_output: MotorOutputConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's motor_output parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that directly affect motor output.
        
        Includes motor invert, neutral mode, and other features related to
        motor output.
    
        :param new_motor_output: Parameter to modify
        :type new_motor_output: MotorOutputConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.motor_output = new_motor_output
        return self
    
    def with_current_limits(self, new_current_limits: CurrentLimitsConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's current_limits parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that directly affect current limiting features.
        
        Contains the supply/stator current limit thresholds and whether to
        enable them.
    
        :param new_current_limits: Parameter to modify
        :type new_current_limits: CurrentLimitsConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.current_limits = new_current_limits
        return self
    
    def with_voltage(self, new_voltage: VoltageConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's voltage parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect Voltage control types.
        
        Includes peak output voltages and other configs affecting voltage
        measurements.
    
        :param new_voltage: Parameter to modify
        :type new_voltage: VoltageConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.voltage = new_voltage
        return self
    
    def with_torque_current(self, new_torque_current: TorqueCurrentConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's torque_current parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect Torque Current control types.
        
        Includes the maximum and minimum applied torque output and the neutral
        deadband used during TorqueCurrentFOC requests.
    
        :param new_torque_current: Parameter to modify
        :type new_torque_current: TorqueCurrentConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.torque_current = new_torque_current
        return self
    
    def with_feedback(self, new_feedback: FeedbackConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's feedback parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect the feedback of this motor controller.
        
        Includes feedback sensor source, any offsets for the feedback sensor,
        and various ratios to describe the relationship between the sensor and
        the mechanism for closed looping.
    
        :param new_feedback: Parameter to modify
        :type new_feedback: FeedbackConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.feedback = new_feedback
        return self
    
    def with_differential_sensors(self, new_differential_sensors: DifferentialSensorsConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's differential_sensors parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs related to sensors used for differential control of a
        mechanism.
        
        Includes the differential sensor sources and IDs.
    
        :param new_differential_sensors: Parameter to modify
        :type new_differential_sensors: DifferentialSensorsConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.differential_sensors = new_differential_sensors
        return self
    
    def with_differential_constants(self, new_differential_constants: DifferentialConstantsConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's differential_constants parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs related to constants used for differential control of a
        mechanism.
        
        Includes the differential peak outputs.
    
        :param new_differential_constants: Parameter to modify
        :type new_differential_constants: DifferentialConstantsConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.differential_constants = new_differential_constants
        return self
    
    def with_open_loop_ramps(self, new_open_loop_ramps: OpenLoopRampsConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's open_loop_ramps parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect the open-loop control of this motor controller.
        
        Open-loop ramp rates for the various control types.
    
        :param new_open_loop_ramps: Parameter to modify
        :type new_open_loop_ramps: OpenLoopRampsConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.open_loop_ramps = new_open_loop_ramps
        return self
    
    def with_closed_loop_ramps(self, new_closed_loop_ramps: ClosedLoopRampsConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's closed_loop_ramps parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect the closed-loop control of this motor controller.
        
        Closed-loop ramp rates for the various control types.
    
        :param new_closed_loop_ramps: Parameter to modify
        :type new_closed_loop_ramps: ClosedLoopRampsConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.closed_loop_ramps = new_closed_loop_ramps
        return self
    
    def with_hardware_limit_switch(self, new_hardware_limit_switch: HardwareLimitSwitchConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's hardware_limit_switch parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that change how the motor controller behaves under different
        limit switch states.
        
        Includes configs such as enabling limit switches, configuring the
        remote sensor ID, the source, and the position to set on limit.
    
        :param new_hardware_limit_switch: Parameter to modify
        :type new_hardware_limit_switch: HardwareLimitSwitchConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.hardware_limit_switch = new_hardware_limit_switch
        return self
    
    def with_audio(self, new_audio: AudioConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's audio parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect audible components of the device.
        
        Includes configuration for the beep on boot.
    
        :param new_audio: Parameter to modify
        :type new_audio: AudioConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.audio = new_audio
        return self
    
    def with_software_limit_switch(self, new_software_limit_switch: SoftwareLimitSwitchConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's software_limit_switch parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect how software-limit switches behave.
        
        Includes enabling software-limit switches and the threshold at which
        they are tripped.
    
        :param new_software_limit_switch: Parameter to modify
        :type new_software_limit_switch: SoftwareLimitSwitchConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.software_limit_switch = new_software_limit_switch
        return self
    
    def with_motion_magic(self, new_motion_magic: MotionMagicConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's motion_magic parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs for Motion Magic®.
        
        Includes Velocity, Acceleration, Jerk, and Expo parameters.
    
        :param new_motion_magic: Parameter to modify
        :type new_motion_magic: MotionMagicConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.motion_magic = new_motion_magic
        return self
    
    def with_custom_params(self, new_custom_params: CustomParamsConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's custom_params parameter and returns itself for
        method-chaining and easier to use config API.
    
        Custom Params.
        
        Custom paramaters that have no real impact on controller.
    
        :param new_custom_params: Parameter to modify
        :type new_custom_params: CustomParamsConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.custom_params = new_custom_params
        return self
    
    def with_closed_loop_general(self, new_closed_loop_general: ClosedLoopGeneralConfigs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's closed_loop_general parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect general behavior during closed-looping.
        
        Includes Continuous Wrap features.
    
        :param new_closed_loop_general: Parameter to modify
        :type new_closed_loop_general: ClosedLoopGeneralConfigs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.closed_loop_general = new_closed_loop_general
        return self
    
    def with_slot0(self, new_slot0: Slot0Configs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's slot0 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gains for the specified slot.
        
        If this slot is selected, these gains are used in closed loop control
        requests.
    
        :param new_slot0: Parameter to modify
        :type new_slot0: Slot0Configs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.slot0 = new_slot0
        return self
    
    def with_slot1(self, new_slot1: Slot1Configs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's slot1 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gains for the specified slot.
        
        If this slot is selected, these gains are used in closed loop control
        requests.
    
        :param new_slot1: Parameter to modify
        :type new_slot1: Slot1Configs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.slot1 = new_slot1
        return self
    
    def with_slot2(self, new_slot2: Slot2Configs) -> 'TalonFXConfiguration':
        """
        Modifies this configuration's slot2 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Gains for the specified slot.
        
        If this slot is selected, these gains are used in closed loop control
        requests.
    
        :param new_slot2: Parameter to modify
        :type new_slot2: Slot2Configs
        :returns: Itself
        :rtype: TalonFXConfiguration
        """
        self.slot2 = new_slot2
        return self

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :returns: String representation of this object
        :rtype: str
        """
        ss = []
        ss.append("TalonFXConfiguration")
        ss.append(str(self.motor_output))
        ss.append(str(self.current_limits))
        ss.append(str(self.voltage))
        ss.append(str(self.torque_current))
        ss.append(str(self.feedback))
        ss.append(str(self.differential_sensors))
        ss.append(str(self.differential_constants))
        ss.append(str(self.open_loop_ramps))
        ss.append(str(self.closed_loop_ramps))
        ss.append(str(self.hardware_limit_switch))
        ss.append(str(self.audio))
        ss.append(str(self.software_limit_switch))
        ss.append(str(self.motion_magic))
        ss.append(str(self.custom_params))
        ss.append(str(self.closed_loop_general))
        ss.append(str(self.slot0))
        ss.append(str(self.slot1))
        ss.append(str(self.slot2))
        return "\n".join(ss)


    def serialize(self) -> str:
        """
        Get the serialized form of this configuration

        :returns: Serialized form of this config group
        :rtype: str
        """
        ss = []
        ss.append(self.motor_output.serialize())
        ss.append(self.current_limits.serialize())
        ss.append(self.voltage.serialize())
        ss.append(self.torque_current.serialize())
        ss.append(self.feedback.serialize())
        ss.append(self.differential_sensors.serialize())
        ss.append(self.differential_constants.serialize())
        ss.append(self.open_loop_ramps.serialize())
        ss.append(self.closed_loop_ramps.serialize())
        ss.append(self.hardware_limit_switch.serialize())
        ss.append(self.audio.serialize())
        ss.append(self.software_limit_switch.serialize())
        ss.append(self.motion_magic.serialize())
        ss.append(self.custom_params.serialize())
        ss.append(self.closed_loop_general.serialize())
        ss.append(self.slot0.serialize())
        ss.append(self.slot1.serialize())
        ss.append(self.slot2.serialize())
        return "".join(ss)

    def deserialize(self, to_deserialize: str) -> StatusCode:
        """
        Take a string and deserialize it to this configuration

        :returns: Return code of the deserialize method
        :rtype: str
        """
        err: StatusCode = StatusCode.OK
        err = self.motor_output.deserialize(to_deserialize)
        err = self.current_limits.deserialize(to_deserialize)
        err = self.voltage.deserialize(to_deserialize)
        err = self.torque_current.deserialize(to_deserialize)
        err = self.feedback.deserialize(to_deserialize)
        err = self.differential_sensors.deserialize(to_deserialize)
        err = self.differential_constants.deserialize(to_deserialize)
        err = self.open_loop_ramps.deserialize(to_deserialize)
        err = self.closed_loop_ramps.deserialize(to_deserialize)
        err = self.hardware_limit_switch.deserialize(to_deserialize)
        err = self.audio.deserialize(to_deserialize)
        err = self.software_limit_switch.deserialize(to_deserialize)
        err = self.motion_magic.deserialize(to_deserialize)
        err = self.custom_params.deserialize(to_deserialize)
        err = self.closed_loop_general.deserialize(to_deserialize)
        err = self.slot0.deserialize(to_deserialize)
        err = self.slot1.deserialize(to_deserialize)
        err = self.slot2.deserialize(to_deserialize)
        return err



class TalonFXConfigurator(ParentConfigurator):
    """
 * Class description for the Talon FX integrated motor controller.

    This handles the configurations for TalonFX
    """

    def __init__(self, id: DeviceIdentifier):
        super().__init__(id)

    def refresh(self, configs: SupportsSerialization, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Refreshes the values of the specified config group.

        Call to refresh the selected configs from the device.

        :param configs: The configs to refresh
        :type configs: name
        :param timeout_seconds: Maximum amount of time to wait when performing configuration
        :type timeout_seconds: second
        :returns: StatusCode of refreshing the configs
        :rtype: StatusCode
        """
        err, serialized_string = self._get_configs_private(timeout_seconds)
        if err.is_ok():
            # Only deserialize if we successfully got configs
            configs.deserialize(serialized_string)
        return err

    def apply(self, configs: SupportsSerialization, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Applies the contents of the specified config to the device.

        Call to apply the selected configs.

        :param configs: Configs to apply
        :type configs: SupportsSerialization
        :param timeout_seconds: Maximum amount of time to wait when performing configuration
        :type timeout_seconds: second
        :returns: StatusCode of the apply method
        :rtype: StatusCode
        """
        if hasattr(configs, "future_proof_configs"):
            # If this object has a future_proof_configs member variable, use it
            future_proof_configs = getattr(configs, "future_proof_configs")
        else:
            # Otherwise default to not using it so our config-groups don't overwrite other groups
            future_proof_configs = False
        return self._set_configs_private(configs.serialize(), timeout_seconds, future_proof_configs, False)

    
    def set_position(self, new_value: rotation, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Sets the mechanism position of the device in mechanism rotations.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param new_value: Value to set to. Units are in rotations.
        :type new_value: rotation
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.TALON_FX_SET_SENSOR_POSITION.value, new_value, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    def clear_sticky_faults(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear the sticky faults in the device.
        
        This typically has no impact on the device functionality.  Instead, it
        just clears telemetry faults that are accessible via API and Tuner
        Self-Test.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.SPN_CLEAR_STICKY_FAULTS.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_hardware(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Hardware fault occurred
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_HARDWARE.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_proc_temp(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Processor temperature exceeded limit
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_PROC_TEMP.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_device_temp(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device temperature exceeded limit
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_DEVICE_TEMP.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_undervoltage(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device supply voltage dropped to near brownout
        levels
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_UNDERVOLTAGE.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_boot_during_enable(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Device boot while detecting the enable signal
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_BOOT_DURING_ENABLE.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_unlicensed_feature_in_use(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: An unlicensed feature is in use, device may not
        behave as expected.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_UNLICENSED_FEATURE_IN_USE.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_bridge_brownout(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Bridge was disabled most likely due to supply
        voltage dropping too low.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_BRIDGE_BROWNOUT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_remote_sensor_reset(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor has reset.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_REMOTE_SENSOR_RESET.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_missing_differential_fx(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote Talon used for differential control is
        not present on CAN Bus.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_MISSING_DIFFERENTIAL_FX.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_remote_sensor_pos_overflow(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor position has overflowed. Because
        of the nature of remote sensors, it is possible for the remote sensor
        position to overflow beyond what is supported by the status signal
        frame. However, this is rare and cannot occur over the course of an
        FRC match under normal use.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_REMOTE_SENSOR_POS_OVERFLOW.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_over_supply_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage has exceeded the maximum voltage
        rating of device.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_OVER_SUPPLYV.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_unstable_supply_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply Voltage is unstable.  Ensure you are using
        a battery and current limited power supply.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_UNSTABLE_SUPPLYV.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_reverse_hard_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Reverse limit switch has been asserted.  Output is
        set to neutral.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_REVERSE_HARD_LIMIT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_forward_hard_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Forward limit switch has been asserted.  Output is
        set to neutral.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_FORWARD_HARD_LIMIT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_reverse_soft_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Reverse soft limit has been asserted.  Output is
        set to neutral.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_REVERSE_SOFT_LIMIT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_forward_soft_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Forward soft limit has been asserted.  Output is
        set to neutral.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_FORWARD_SOFT_LIMIT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_missing_soft_limit_remote(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote soft limit device is not present on CAN
        Bus.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_MISSING_REM_SOFT_LIM.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_missing_hard_limit_remote(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote limit switch device is not present on
        CAN Bus.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_MISSING_REM_HARD_LIM.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_remote_sensor_data_invalid(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor's data is no longer trusted.
        This can happen if the remote sensor disappears from the CAN bus or if
        the remote sensor indicates its data is no longer valid, such as when
        a CANcoder's magnet strength falls into the "red" range.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_MISSING_REMOTE_SENSOR.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_fused_sensor_out_of_sync(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The remote sensor used for fusion has fallen out
        of sync to the local sensor. A re-synchronization has occurred, which
        may cause a discontinuity. This typically happens if there is
        significant slop in the mechanism, or if the RotorToSensorRatio
        configuration parameter is incorrect.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_FUSED_SENSOR_OUT_OF_SYNC.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_stator_curr_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Stator current limit occured.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_STATOR_CURR_LIMIT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_supply_curr_limit(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Supply current limit occured.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_SUPPLY_CURR_LIMIT.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_using_fused_cancoder_while_unlicensed(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Using Fused CANcoder feature while unlicensed.
        Device has fallen back to remote CANcoder.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_USING_FUSED_CCWHILE_UNLICENSED.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    
    
    def clear_sticky_fault_static_brake_disabled(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: Static brake was momentarily disabled due to
        excessive braking current while disabled.
        
        This is available in the configurator in case the user wants
        to initialize their device entirely without passing a device
        reference down to the code that performs the initialization.
        In this case, the user passes down the configurator object
        and performs all the initialization code on the object.
        
        :param timeout_seconds: Maximum time to wait up to in seconds.
        :type timeout_seconds: second
        :returns: StatusCode of the set command
        :rtype: StatusCode
        """
    
        value = ctypes.c_char_p()
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_TALONFX_STATIC_BRAKE_DISABLED.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    

