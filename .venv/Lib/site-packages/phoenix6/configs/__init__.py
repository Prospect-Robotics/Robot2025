"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from .config_groups import SupportsSerialization
from .config_groups import MagnetSensorConfigs
from .config_groups import MountPoseConfigs
from .config_groups import GyroTrimConfigs
from .config_groups import Pigeon2FeaturesConfigs
from .config_groups import MotorOutputConfigs
from .config_groups import CurrentLimitsConfigs
from .config_groups import VoltageConfigs
from .config_groups import TorqueCurrentConfigs
from .config_groups import FeedbackConfigs
from .config_groups import ExternalFeedbackConfigs
from .config_groups import DifferentialSensorsConfigs
from .config_groups import DifferentialConstantsConfigs
from .config_groups import OpenLoopRampsConfigs
from .config_groups import ClosedLoopRampsConfigs
from .config_groups import HardwareLimitSwitchConfigs
from .config_groups import AudioConfigs
from .config_groups import SoftwareLimitSwitchConfigs
from .config_groups import MotionMagicConfigs
from .config_groups import CustomParamsConfigs
from .config_groups import ClosedLoopGeneralConfigs
from .config_groups import ToFParamsConfigs
from .config_groups import ProximityParamsConfigs
from .config_groups import FovParamsConfigs
from .config_groups import CommutationConfigs
from .config_groups import DigitalInputsConfigs
from .config_groups import QuadratureConfigs
from .config_groups import PWM1Configs
from .config_groups import PWM2Configs
from .config_groups import Slot0Configs
from .config_groups import Slot1Configs
from .config_groups import Slot2Configs
from .config_groups import SlotConfigs
from .talon_fx_configs import TalonFXConfiguration, TalonFXConfigurator
from .cancoder_configs import CANcoderConfiguration, CANcoderConfigurator
from .pigeon2_configs import Pigeon2Configuration, Pigeon2Configurator
from .talon_fxs_configs import TalonFXSConfiguration, TalonFXSConfigurator
from .canrange_configs import CANrangeConfiguration, CANrangeConfigurator
from .candi_configs import CANdiConfiguration, CANdiConfigurator


__all__ = [
    "SupportsSerialization",
    "MagnetSensorConfigs",
    "MountPoseConfigs",
    "GyroTrimConfigs",
    "Pigeon2FeaturesConfigs",
    "MotorOutputConfigs",
    "CurrentLimitsConfigs",
    "VoltageConfigs",
    "TorqueCurrentConfigs",
    "FeedbackConfigs",
    "ExternalFeedbackConfigs",
    "DifferentialSensorsConfigs",
    "DifferentialConstantsConfigs",
    "OpenLoopRampsConfigs",
    "ClosedLoopRampsConfigs",
    "HardwareLimitSwitchConfigs",
    "AudioConfigs",
    "SoftwareLimitSwitchConfigs",
    "MotionMagicConfigs",
    "CustomParamsConfigs",
    "ClosedLoopGeneralConfigs",
    "ToFParamsConfigs",
    "ProximityParamsConfigs",
    "FovParamsConfigs",
    "CommutationConfigs",
    "DigitalInputsConfigs",
    "QuadratureConfigs",
    "PWM1Configs",
    "PWM2Configs",
    "Slot0Configs",
    "Slot1Configs",
    "Slot2Configs",
    "SlotConfigs",
    "TalonFXConfiguration",
    "TalonFXConfigurator",
    "CANcoderConfiguration",
    "CANcoderConfigurator",
    "Pigeon2Configuration",
    "Pigeon2Configurator",
    "TalonFXSConfiguration",
    "TalonFXSConfigurator",
    "CANrangeConfiguration",
    "CANrangeConfigurator",
    "CANdiConfiguration",
    "CANdiConfigurator",
]
