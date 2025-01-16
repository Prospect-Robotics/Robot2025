"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from . import compound
from .duty_cycle_out import DutyCycleOut
from .torque_current_foc import TorqueCurrentFOC
from .voltage_out import VoltageOut
from .position_duty_cycle import PositionDutyCycle
from .position_voltage import PositionVoltage
from .position_torque_current_foc import PositionTorqueCurrentFOC
from .velocity_duty_cycle import VelocityDutyCycle
from .velocity_voltage import VelocityVoltage
from .velocity_torque_current_foc import VelocityTorqueCurrentFOC
from .motion_magic_duty_cycle import MotionMagicDutyCycle
from .motion_magic_voltage import MotionMagicVoltage
from .motion_magic_torque_current_foc import MotionMagicTorqueCurrentFOC
from .differential_duty_cycle import DifferentialDutyCycle
from .differential_voltage import DifferentialVoltage
from .differential_position_duty_cycle import DifferentialPositionDutyCycle
from .differential_position_voltage import DifferentialPositionVoltage
from .differential_velocity_duty_cycle import DifferentialVelocityDutyCycle
from .differential_velocity_voltage import DifferentialVelocityVoltage
from .differential_motion_magic_duty_cycle import DifferentialMotionMagicDutyCycle
from .differential_motion_magic_voltage import DifferentialMotionMagicVoltage
from .follower import Follower
from .strict_follower import StrictFollower
from .differential_follower import DifferentialFollower
from .differential_strict_follower import DifferentialStrictFollower
from .neutral_out import NeutralOut
from .coast_out import CoastOut
from .static_brake import StaticBrake
from .music_tone import MusicTone
from .motion_magic_velocity_duty_cycle import MotionMagicVelocityDutyCycle
from .motion_magic_velocity_torque_current_foc import MotionMagicVelocityTorqueCurrentFOC
from .motion_magic_velocity_voltage import MotionMagicVelocityVoltage
from .motion_magic_expo_duty_cycle import MotionMagicExpoDutyCycle
from .motion_magic_expo_voltage import MotionMagicExpoVoltage
from .motion_magic_expo_torque_current_foc import MotionMagicExpoTorqueCurrentFOC
from .dynamic_motion_magic_duty_cycle import DynamicMotionMagicDutyCycle
from .dynamic_motion_magic_voltage import DynamicMotionMagicVoltage
from .dynamic_motion_magic_torque_current_foc import DynamicMotionMagicTorqueCurrentFOC


__all__ = [
    "compound",
    "DutyCycleOut",
    "TorqueCurrentFOC",
    "VoltageOut",
    "PositionDutyCycle",
    "PositionVoltage",
    "PositionTorqueCurrentFOC",
    "VelocityDutyCycle",
    "VelocityVoltage",
    "VelocityTorqueCurrentFOC",
    "MotionMagicDutyCycle",
    "MotionMagicVoltage",
    "MotionMagicTorqueCurrentFOC",
    "DifferentialDutyCycle",
    "DifferentialVoltage",
    "DifferentialPositionDutyCycle",
    "DifferentialPositionVoltage",
    "DifferentialVelocityDutyCycle",
    "DifferentialVelocityVoltage",
    "DifferentialMotionMagicDutyCycle",
    "DifferentialMotionMagicVoltage",
    "Follower",
    "StrictFollower",
    "DifferentialFollower",
    "DifferentialStrictFollower",
    "NeutralOut",
    "CoastOut",
    "StaticBrake",
    "MusicTone",
    "MotionMagicVelocityDutyCycle",
    "MotionMagicVelocityTorqueCurrentFOC",
    "MotionMagicVelocityVoltage",
    "MotionMagicExpoDutyCycle",
    "MotionMagicExpoVoltage",
    "MotionMagicExpoTorqueCurrentFOC",
    "DynamicMotionMagicDutyCycle",
    "DynamicMotionMagicVoltage",
    "DynamicMotionMagicTorqueCurrentFOC",
]
