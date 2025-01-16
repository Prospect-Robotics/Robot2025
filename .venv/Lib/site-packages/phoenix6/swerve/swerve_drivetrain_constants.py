"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from phoenix6.configs import Pigeon2Configuration
from phoenix6.phoenix_native import Native

class SwerveDrivetrainConstants:
    """
    Common constants for a swerve drivetrain.
    """

    def __init__(self):
        self.can_bus_name: str = "rio"
        """
        Name of the CAN bus the swerve drive is on. Possible CAN bus strings are:
        
            - empty string or "rio" for the native roboRIO CAN bus
            - CANivore name or serial number
            - "*" for any CANivore seen by the program
        
        Note that all devices must be on the same CAN bus.
        """
        self.pigeon2_id: int = 0
        """
        CAN ID of the Pigeon2 on the drivetrain.
        """
        self.pigeon2_configs: None | Pigeon2Configuration = None
        """
        The configuration object to apply to the Pigeon2. This defaults to null. If this
        remains null, then the Pigeon2 will not be configured (and whatever configs are
        on it remain on it). If this is not null, the Pigeon2 will be overwritten with
        these configs.
        """
    
    def with_can_bus_name(self, new_can_bus_name: str) -> 'SwerveDrivetrainConstants':
        """
        Modifies the can_bus_name parameter and returns itself.
    
        Name of the CAN bus the swerve drive is on. Possible CAN bus strings are:
        
            - empty string or "rio" for the native roboRIO CAN bus
            - CANivore name or serial number
            - "*" for any CANivore seen by the program
        
        Note that all devices must be on the same CAN bus.
    
        :param new_can_bus_name: Parameter to modify
        :type new_can_bus_name: str
        :returns: this object
        :rtype: SwerveDrivetrainConstants
        """
    
        self.can_bus_name = new_can_bus_name
        return self
    
    def with_pigeon2_id(self, new_pigeon2_id: int) -> 'SwerveDrivetrainConstants':
        """
        Modifies the pigeon2_id parameter and returns itself.
    
        CAN ID of the Pigeon2 on the drivetrain.
    
        :param new_pigeon2_id: Parameter to modify
        :type new_pigeon2_id: int
        :returns: this object
        :rtype: SwerveDrivetrainConstants
        """
    
        self.pigeon2_id = new_pigeon2_id
        return self
    
    def with_pigeon2_configs(self, new_pigeon2_configs: None | Pigeon2Configuration) -> 'SwerveDrivetrainConstants':
        """
        Modifies the pigeon2_configs parameter and returns itself.
    
        The configuration object to apply to the Pigeon2. This defaults to null. If this
        remains null, then the Pigeon2 will not be configured (and whatever configs are
        on it remain on it). If this is not null, the Pigeon2 will be overwritten with
        these configs.
    
        :param new_pigeon2_configs: Parameter to modify
        :type new_pigeon2_configs: None | Pigeon2Configuration
        :returns: this object
        :rtype: SwerveDrivetrainConstants
        """
    
        self.pigeon2_configs = new_pigeon2_configs
        return self
    
    def _create_native_instance(self) -> ctypes.c_void_p:
        self._c_can_bus_name = ctypes.c_char_p(bytes(self.can_bus_name, 'utf-8'))
        return Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain_constants(
            self._c_can_bus_name,
            self.pigeon2_id
        )
    
