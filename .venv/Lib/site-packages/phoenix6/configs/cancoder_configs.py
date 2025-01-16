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


class CANcoderConfiguration:
    """
    Class for CANcoder, a CAN based magnetic encoder that provides absolute and
    relative position along with filtered velocity.

    This handles the configurations for CANcoder
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

        
        self.magnet_sensor: MagnetSensorConfigs = MagnetSensorConfigs()
        """
        Configs that affect the magnet sensor and how to interpret it.
        
        Includes sensor direction, the sensor discontinuity point, and the
        magnet offset.
        """
        
        
        self.custom_params: CustomParamsConfigs = CustomParamsConfigs()
        """
        Custom Params.
        
        Custom paramaters that have no real impact on controller.
        """
        
    
    def with_magnet_sensor(self, new_magnet_sensor: MagnetSensorConfigs) -> 'CANcoderConfiguration':
        """
        Modifies this configuration's magnet_sensor parameter and returns itself for
        method-chaining and easier to use config API.
    
        Configs that affect the magnet sensor and how to interpret it.
        
        Includes sensor direction, the sensor discontinuity point, and the
        magnet offset.
    
        :param new_magnet_sensor: Parameter to modify
        :type new_magnet_sensor: MagnetSensorConfigs
        :returns: Itself
        :rtype: CANcoderConfiguration
        """
        self.magnet_sensor = new_magnet_sensor
        return self
    
    def with_custom_params(self, new_custom_params: CustomParamsConfigs) -> 'CANcoderConfiguration':
        """
        Modifies this configuration's custom_params parameter and returns itself for
        method-chaining and easier to use config API.
    
        Custom Params.
        
        Custom paramaters that have no real impact on controller.
    
        :param new_custom_params: Parameter to modify
        :type new_custom_params: CustomParamsConfigs
        :returns: Itself
        :rtype: CANcoderConfiguration
        """
        self.custom_params = new_custom_params
        return self

    def __str__(self) -> str:
        """
        Provides the string representation
        of this object

        :returns: String representation of this object
        :rtype: str
        """
        ss = []
        ss.append("CANcoderConfiguration")
        ss.append(str(self.magnet_sensor))
        ss.append(str(self.custom_params))
        return "\n".join(ss)


    def serialize(self) -> str:
        """
        Get the serialized form of this configuration

        :returns: Serialized form of this config group
        :rtype: str
        """
        ss = []
        ss.append(self.magnet_sensor.serialize())
        ss.append(self.custom_params.serialize())
        return "".join(ss)

    def deserialize(self, to_deserialize: str) -> StatusCode:
        """
        Take a string and deserialize it to this configuration

        :returns: Return code of the deserialize method
        :rtype: str
        """
        err: StatusCode = StatusCode.OK
        err = self.magnet_sensor.deserialize(to_deserialize)
        err = self.custom_params.deserialize(to_deserialize)
        return err



class CANcoderConfigurator(ParentConfigurator):
    """
 * Class for CANcoder, a CAN based magnetic encoder that provides absolute and
 * relative position along with filtered velocity.

    This handles the configurations for CANcoder
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
        Sets the current position of the device.
        
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
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CANCODER_SET_SENSOR_POSITION.value, new_value, ctypes.byref(value))
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
    
    
    def clear_sticky_fault_bad_magnet(self, timeout_seconds: second = 0.100) -> StatusCode:
        """
        Clear sticky fault: The magnet distance is not correct or magnet is
        missing
        
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
        Native.instance().c_ctre_phoenix6_serialize_double(SpnValue.CLEAR_STICKY_FAULT_CANCODER_BAD_MAGNET.value, 0, ctypes.byref(value))
        if value.value is not None:
            serialized = str(value.value, encoding='utf-8')
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(value))
        else:
            serialized = ""
        return self._set_configs_private(serialized, timeout_seconds, False, True)
    

