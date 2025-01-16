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


class CANdiConfiguration:
    """
    Class for CANdi, a CAN digital input device that detects when a digital signal
    is asserted or deasserted.

    This handles the configurations for CANdi
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

        
        self.custom_params: CustomParamsConfigs = CustomParamsConfigs()
        """
        Custom Params.
        
        Custom paramaters that have no real impact on controller.
        """
        
        
        self.digital_inputs: DigitalInputsConfigs = DigitalInputsConfigs()
        """
        Configs related to CANdi digital I/O settings
        
        Contains float-state settings and when to assert the S1/S2 inputs.
        """
        
        
        self.quadrature: QuadratureConfigs = QuadratureConfigs()
        """
        Configs related to CANdi's quadrature interface using both the S1IN
        and S2IN inputs
        
        All the configs related to the quadrature interface for CANdi,
        including encoder edges per revolution and sensor direction.
        """
        
        
        self.pwm1: PWM1Configs = PWM1Configs()
        """
        Configs related to CANdi's PWM interface on the Signal 1 input (S1IN)
        
        All the configs related to the PWM interface for CANdi on S1,
        including absolute sensor offset, absolute sensor discontinuity point
        and sensor direction.
        """
        
        
        self.pwm2: PWM2Configs = PWM2Configs()
        """
        Configs related to CANdi's PWM interface on the Signal 2 input (S2IN)
        
        All the configs related to the PWM interface for CANdi on S1,
        including absolute sensor offset, absolute sensor discontinuity point
        and sensor direction.
        """
        
    
    def with_custom_params(self, new_custom_params: CustomParamsConfigs) -> 'CANdiConfiguration':
        """
        Modifies this configuration's custom_params parameter and returns itself for
        method-chaining and easier to use config API.
    
        Custom Params.
        
        Custom paramaters that have no real impact on controller.
    
        :param new_custom_params: Parameter to modify
        :type new_custom_params: CustomParamsConfigs
        :returns: Itself
        :rtype: CANdiConfiguration
        """
        self.custom_params = new_custom_params
        return self
    
    def with_digital_inputs(self, new_digital_inputs: DigitalInputsConfigs) -> 'CANdiConfiguration':
        """
        Modifies this configuration's digital_inputs parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs related to CANdi digital I/O settings
        
        Contains float-state settings and when to assert the S1/S2 inputs.
    
        :param new_digital_inputs: Parameter to modify
        :type new_digital_inputs: DigitalInputsConfigs
        :returns: Itself
        :rtype: CANdiConfiguration
        """
        self.digital_inputs = new_digital_inputs
        return self
    
    def with_quadrature(self, new_quadrature: QuadratureConfigs) -> 'CANdiConfiguration':
        """
        Modifies this configuration's quadrature parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs related to CANdi's quadrature interface using both the S1IN
        and S2IN inputs
        
        All the configs related to the quadrature interface for CANdi,
        including encoder edges per revolution and sensor direction.
    
        :param new_quadrature: Parameter to modify
        :type new_quadrature: QuadratureConfigs
        :returns: Itself
        :rtype: CANdiConfiguration
        """
        self.quadrature = new_quadrature
        return self
    
    def with_pwm1(self, new_pwm1: PWM1Configs) -> 'CANdiConfiguration':
        """
        Modifies this configuration's pwm1 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs related to CANdi's PWM interface on the Signal 1 input (S1IN)
        
        All the configs related to the PWM interface for CANdi on S1,
        including absolute sensor offset, absolute sensor discontinuity point
        and sensor direction.
    
        :param new_pwm1: Parameter to modify
        :type new_pwm1: PWM1Configs
        :returns: Itself
        :rtype: CANdiConfiguration
        """
        self.pwm1 = new_pwm1
        return self
    
    def with_pwm2(self, new_pwm2: PWM2Configs) -> 'CANdiConfiguration':
        """
        Modifies this configuration's pwm2 parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs related to CANdi's PWM interface on the Signal 2 input (S2IN)
        
        All the configs related to the PWM interface for CANdi on S1,
        including absolute sensor offset, absolute sensor discontinuity point
        and sensor direction.
    
        :param new_pwm2: Parameter to modify
        :type new_pwm2: PWM2Configs
        :returns: Itself
        :rtype: CANdiConfiguration
        """
        self.pwm2 = new_pwm2
        return self

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :returns: String representation of this object
        :rtype: str
        """
        ss = []
        ss.append("CANdiConfiguration")
        ss.append(str(self.custom_params))
        ss.append(str(self.digital_inputs))
        ss.append(str(self.quadrature))
        ss.append(str(self.pwm1))
        ss.append(str(self.pwm2))
        return "\n".join(ss)


    def serialize(self) -> str:
        """
        Get the serialized form of this configuration

        :returns: Serialized form of this config group
        :rtype: str
        """
        ss = []
        ss.append(self.custom_params.serialize())
        ss.append(self.digital_inputs.serialize())
        ss.append(self.quadrature.serialize())
        ss.append(self.pwm1.serialize())
        ss.append(self.pwm2.serialize())
        return "".join(ss)

    def deserialize(self, to_deserialize: str) -> StatusCode:
        """
        Take a string and deserialize it to this configuration

        :returns: Return code of the deserialize method
        :rtype: str
        """
        err: StatusCode = StatusCode.OK
        err = self.custom_params.deserialize(to_deserialize)
        err = self.digital_inputs.deserialize(to_deserialize)
        err = self.quadrature.deserialize(to_deserialize)
        err = self.pwm1.deserialize(to_deserialize)
        err = self.pwm2.deserialize(to_deserialize)
        return err



class CANdiConfigurator(ParentConfigurator):
    """
 * Class for CANdi, a CAN digital input device that detects when a digital
 * signal is asserted or deasserted.

    This handles the configurations for CANdi
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

    
    def set_quadrature_position(self, new_value: rotation, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Sets the position of the quadrature input.
        
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
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CANDI_SET_QUAD_POSITION.value, new_value, ctypes.byref(value))
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
    
    
    def clear_sticky_fault_5_v(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: CANdi has detected a 5V fault. This may be due to
        overcurrent or a short-circuit.
        
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
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_CANDI_5V.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    

