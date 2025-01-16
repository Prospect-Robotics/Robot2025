"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes as c
import os, pkg_resources

class ReturnValues(c.Structure):
    _fields_ = [
        ("outValue", c.c_double),
        ("unitsKey", c.c_uint32),
        ("units", c.c_char_p),
        ("hwtimestampseconds", c.c_double),
        ("swtimestampseconds", c.c_double),
        ("ecutimestampseconds", c.c_double),
        ("error", c.c_int),
    ]

class SignalValues(c.Structure):
    _fields_ = [
        ("devicehash", c.c_uint32),
        ("spn", c.c_uint32),
    ]

class NetworkSignals(c.Structure):
    _fields_ = [
        ("network", c.c_char_p),
        ("signal", SignalValues),
    ]

class Pose_t(c.Structure):
    _fields_ = [
        ("x", c.c_double),
        ("y", c.c_double),
        ("theta", c.c_double),
    ]

class ChassisSpeeds_t(c.Structure):
    _fields_ = [
        ("vx", c.c_double),
        ("vy", c.c_double),
        ("omega", c.c_double),
    ]

class SwerveModuleState_t(c.Structure):
    _fields_ = [
        ("speed", c.c_double),
        ("angle", c.c_double),
    ]

class SwerveModulePosition_t(c.Structure):
    _fields_ = [
        ("distance", c.c_double),
        ("angle", c.c_double),
    ]

class SwerveDriveState_t(c.Structure):
    _fields_ = [
        ("pose", Pose_t),
        ("speeds", ChassisSpeeds_t),
        ("moduleStates", c.POINTER(SwerveModuleState_t)),
        ("moduleTargets", c.POINTER(SwerveModuleState_t)),
        ("modulePositions", c.POINTER(SwerveModulePosition_t)),
        ("rawHeading", c.c_double),
        ("timestamp", c.c_double),
        ("odometryPeriod", c.c_double),
        ("successfulDaqs", c.c_int32),
        ("failedDaqs", c.c_int32),
    ]

class SwerveControlParams_t(c.Structure):
    _fields_ = [
        ("kMaxSpeedMps", c.c_double),
        ("operatorForwardDirection", c.c_double),
        ("currentChassisSpeed", ChassisSpeeds_t),
        ("currentPose", Pose_t),
        ("timestamp", c.c_double),
        ("updatePeriod", c.c_double),
    ]

class SwerveModuleRequest_t(c.Structure):
    _fields_ = [
        ("state", SwerveModuleState_t),
        ("wheelForceFeedforwardX", c.c_double),
        ("wheelForceFeedforwardY", c.c_double),
        ("driveRequest", c.c_int),
        ("steerRequest", c.c_int),
        ("updatePeriod", c.c_double),
        ("enableFOC", c.c_bool),
    ]

class Native:
    """
    Class to use for referencing c functions in the
    Phoenix6 C API
    """

    __instance = None
    __api_instance = None

    __all_c_libs = []

    __c_args = [
        ("c_ctre_phoenix6_get_current_time_seconds", c.c_double, []),
        ("c_ctre_phoenix6_get_system_time_seconds", c.c_double, []),
        ("c_ctre_phoenix6_is_simulation", c.c_bool, []),
        ("c_ctre_phoenix6_is_replay", c.c_bool, []),
        (
            "c_ctre_phoenix6_get_rets",
            c.c_int,
            [c.c_uint16, c.c_int, c.POINTER(ReturnValues)],
        ),
        (
            "c_ctre_phoenix6_encode_device",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_char_p, c.POINTER(c.c_uint32)],
        ),
        (
            "c_ctre_phoenix6_get_signal",
            c.c_int,
            [c.c_size_t, c.POINTER(SignalValues), c.POINTER(ReturnValues), c.c_char_p, c.c_bool, c.c_double]
        ),
        (
            "c_ctre_phoenix6_SetUpdateFrequency",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.c_uint16, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_SetUpdateFrequencyForAll",
            c.c_int,
            [c.c_int, c.POINTER(NetworkSignals), c.c_size_t, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_GetUpdateFrequency",
            c.c_double,
            [c.c_char_p, c.c_uint32, c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_OptimizeUpdateFrequencies",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_ResetUpdateFrequencies",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.c_double]
        ),
        (
            "c_ctre_phoenix6_unmanaged_feed_enable",
            c.c_int,
            [c.c_int32]
        ),
        (
            "c_ctre_phoenix6_unmanaged_get_api_compliancy",
            c.c_int,
            []
        ),
        (
            "c_ctre_phoenix6_unmanaged_get_phoenix_version",
            c.c_int,
            []
        ),
        (
            "c_ctre_phoenix6_unmanaged_get_enable_state",
            c.c_bool,
            []
        ),
        (
            "c_Phoenix_Diagnostics_SetSecondsToStart",
            None,
            [c.c_double]
        ),
        (
            "c_ctre_phoenix6_unmanaged_load_phoenix",
            None,
            []
        ),
        (
            "c_ctre_phoenix_report_error",
            None,
            [c.c_int, c.c_int32, c.c_int, c.c_char_p, c.c_char_p, c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_set_configs",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_int, c.c_double, c.c_char_p, c.c_uint32, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_get_configs",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_int, c.c_double, c.POINTER(c.c_char_p), c.c_bool]
        ),
        (
            "c_ctre_phoenix6_serialize_double",
            c.c_int,
            [c.c_int, c.c_double, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_serialize_int",
            c.c_int,
            [c.c_int, c.c_int, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_serialize_bool",
            c.c_int,
            [c.c_int, c.c_bool, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_serialize_pgn",
            c.c_int,
            [c.c_int, c.c_uint16, c.c_uint16, c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_deserialize_double",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_deserialize_int",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_int)]
        ),
        (
            "c_ctre_phoenix6_deserialize_bool",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_bool)]
        ),
        (
            "c_ctre_phoenix6_deserialize_pgn",
            c.c_int,
            [c.c_int, c.c_char_p, c.c_uint32, c.POINTER(c.c_uint16), c.POINTER(c.c_uint16)]
        ),
        (
            "c_ctre_phoenix6_free_memory",
            c.c_int,
            [c.POINTER(c.c_char_p)]
        ),
        (
            "c_ctre_phoenix6_platform_canbus_is_network_fd",
            c.c_bool,
            [c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_platform_canbus_get_status",
            c.c_int32,
            [c.POINTER(c.c_float), c.POINTER(c.c_uint32), c.POINTER(c.c_uint32), c.POINTER(c.c_uint32), c.POINTER(c.c_uint32), c.c_char_p, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_platform_sim_create",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_platform_sim_destroy",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_platform_sim_destroy_all",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_sim_set_physics_input",
            c.c_int32,
            [c.c_int, c.c_int, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_sim_get_physics_value",
            c.c_int32,
            [c.c_int, c.c_int, c.c_char_p, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_sim_get_last_error",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_platform_replay_load_file",
            c.c_int32,
            [c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_platform_replay_close_file",
            None,
            []
        ),
        (
            "c_ctre_phoenix6_platform_replay_is_file_loaded",
            c.c_bool,
            []
        ),
        (
            "c_ctre_phoenix6_platform_replay_play",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_replay_pause",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_replay_stop",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_replay_is_running",
            c.c_bool,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_platform_replay_set_speed",
            None,
            [c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_replay_step_timing",
            c.c_int32,
            [c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_raw",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_uint8), c.POINTER(c.c_uint8), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_boolean",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_bool), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_integer",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_int64), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_float",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_float), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_double",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_double), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_string",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.c_char_p, c.POINTER(c.c_uint8), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_boolean_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_bool), c.POINTER(c.c_uint8), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_integer_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_int64), c.POINTER(c.c_uint8), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_float_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_float), c.POINTER(c.c_uint8), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_replay_get_double_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_char_p), c.POINTER(c.c_double), c.POINTER(c.c_uint8), c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_platform_set_logger_path",
            c.c_int32,
            [c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_platform_start_logger",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_stop_logger",
            c.c_int32,
            []
        ),
        (
            "c_ctre_phoenix6_platform_enable_auto_logging",
            c.c_int32,
            [c.c_bool]
        ),
        (
            "c_ctre_phoenix6_platform_write_raw",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_uint8), c.c_uint8, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_boolean",
            c.c_int32,
            [c.c_char_p, c.c_bool, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_integer",
            c.c_int32,
            [c.c_char_p, c.c_int64, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_float",
            c.c_int32,
            [c.c_char_p, c.c_float, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_double",
            c.c_int32,
            [c.c_char_p, c.c_double, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_string",
            c.c_int32,
            [c.c_char_p, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_boolean_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_bool), c.c_uint8, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_integer_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_int64), c.c_uint8, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_float_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_float), c.c_uint8, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_platform_write_double_array",
            c.c_int32,
            [c.c_char_p, c.POINTER(c.c_double), c.c_uint8, c.c_char_p, c.c_double]
        ),
        (
            "c_ctre_phoenix6_orchestra_Create",
            c.c_int,
            [c.POINTER(c.c_uint16)]
        ),
        (
            "c_ctre_phoenix6_orchestra_Close",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_AddDevice",
            c.c_int,
            [c.c_uint16, c.c_char_p, c.c_uint32]
        ),
        (
            "c_ctre_phoenix6_orchestra_AddDeviceWithTrack",
            c.c_int,
            [c.c_uint16, c.c_char_p, c.c_uint32, c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_ClearDevices",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_LoadMusic",
            c.c_int,
            [c.c_uint16, c.c_char_p]
        ),
        (
            "c_ctre_phoenix6_orchestra_Play",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_Pause",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_Stop",
            c.c_int,
            [c.c_uint16]
        ),
        (
            "c_ctre_phoenix6_orchestra_IsPlaying",
            c.c_int,
            [c.c_uint16, c.POINTER(c.c_int)]
        ),
        (
            "c_ctre_phoenix6_orchestra_GetCurrentTime",
            c.c_int,
            [c.c_uint16, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_RequestControlDutyCycleOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVoltageOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlPositionDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlPositionVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlPositionTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVelocityDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVelocityVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlVelocityTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialPositionDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialPositionVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialVelocityDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialVelocityVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialMotionMagicDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialMotionMagicVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_int, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlStrictFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_int]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDifferentialStrictFollower",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_int]
        ),
        (
            "c_ctre_phoenix6_RequestControlNeutralOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlCoastOut",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlStaticBrake",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMusicTone",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVelocityDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVelocityTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicVelocityVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicExpoDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicExpoVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlMotionMagicExpoTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDynamicMotionMagicDutyCycle",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDynamicMotionMagicVoltage",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDynamicMotionMagicTorqueCurrentFOC",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_DutyCycleOut_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_PositionDutyCycle_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VelocityDutyCycle_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_MotionMagicDutyCycle_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_DutyCycleOut_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_PositionDutyCycle_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VelocityDutyCycle_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_MotionMagicDutyCycle_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VoltageOut_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_PositionVoltage_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VelocityVoltage_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_MotionMagicVoltage_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VoltageOut_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_PositionVoltage_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VelocityVoltage_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_MotionMagicVoltage_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_bool, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_TorqueCurrentFOC_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_PositionTorqueCurrentFOC_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VelocityTorqueCurrentFOC_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_MotionMagicTorqueCurrentFOC_Position",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_TorqueCurrentFOC_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_PositionTorqueCurrentFOC_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_VelocityTorqueCurrentFOC_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_RequestControlDiff_MotionMagicTorqueCurrentFOC_Velocity",
            c.c_int,
            [c.c_char_p, c.c_uint, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_int, c.c_bool, c.c_bool, c.c_bool, c.c_bool, c.c_bool]
        ),
    ]
    """
    Function prototypes for C methods in Phoenix Tools.

    Format is tuple[str, ctype, list[ctype]]

    First Parameter str is name of function
    Second Parameter ctype is return of function
    Third Parameter list[ctype] are the arguments of the function
    """

    __c_args_api = [
        (
            "c_ctre_phoenix6_swerve_create_drivetrain",
            c.c_int,
            [c.c_void_p, c.c_void_p, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_create_drivetrain_with_freq",
            c.c_int,
            [c.c_void_p, c.c_double, c.c_void_p, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_create_drivetrain_with_stddev",
            c.c_int,
            [c.c_void_p, c.c_double, c.POINTER(c.c_double), c.POINTER(c.c_double), c.c_void_p, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_destroy_drivetrain",
            None,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_is_on_can_fd",
            c.c_bool,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_get_odometry_frequency",
            c.c_double,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_is_odometry_valid",
            c.c_bool,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control",
            None,
            [c.c_int, c.c_void_p, c.CFUNCTYPE(c.c_int32, c.c_void_p, c.POINTER(SwerveControlParams_t))]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_get_state",
            None,
            [c.c_int, c.POINTER(SwerveDriveState_t)]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_register_telemetry",
            None,
            [c.c_int, c.c_void_p, c.CFUNCTYPE(None, c.c_void_p, c.POINTER(SwerveDriveState_t))]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_config_neutral_mode",
            c.c_int32,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_tare_everything",
            None,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_seed_field_centric",
            None,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_reset_pose",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_reset_translation",
            None,
            [c.c_int, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_reset_rotation",
            None,
            [c.c_int, c.c_double]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_operator_perspective_forward",
            None,
            [c.c_int, c.c_double]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_get_operator_forward_direction",
            c.c_double,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_add_vision_measurement",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_add_vision_measurement_with_stddev",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.c_double, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_vision_measurement_stddevs",
            None,
            [c.c_int, c.POINTER(c.c_double)]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_sample_pose_at",
            c.c_bool,
            [c.c_int, c.c_double, c.POINTER(Pose_t)]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_odom_start",
            None,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_odom_stop",
            None,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_odom_set_thread_priority",
            None,
            [c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_module_apply",
            None,
            [c.c_int, c.c_size_t, c.POINTER(SwerveModuleRequest_t)]
        ),
        (
            "c_ctre_phoenix6_swerve_module_get_position",
            SwerveModulePosition_t,
            [c.c_int, c.c_size_t, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_swerve_module_get_cached_position",
            SwerveModulePosition_t,
            [c.c_int, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_module_get_current_state",
            SwerveModuleState_t,
            [c.c_int, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_module_get_target_state",
            SwerveModuleState_t,
            [c.c_int, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_module_reset_position",
            None,
            [c.c_int, c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_create_drivetrain_constants",
            c.c_void_p,
            [c.c_char_p, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_create_module_constants_arr",
            c.c_void_p,
            [c.c_size_t]
        ),
        (
            "c_ctre_phoenix6_swerve_set_module_constants",
            None,
            [c.c_void_p, c.c_size_t, c.c_int, c.c_int, c.c_int, c.c_double, c.c_double, c.c_double, c.c_bool, c.c_bool, c.c_bool, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_int, c.c_double, c.c_double, c.c_int, c.c_int, c.c_int, c.c_double, c.c_double, c.c_double, c.c_double]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_idle",
            None,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_idle",
            c.c_int32,
            [c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_swerve_drive_brake",
            None,
            [c.c_int, c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_swerve_drive_brake",
            c.c_int32,
            [c.c_int, c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_field_centric",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_field_centric",
            c.c_int32,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_robot_centric",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_robot_centric",
            c.c_int32,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_point_wheels_at",
            None,
            [c.c_int, c.c_double, c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_point_wheels_at",
            c.c_int32,
            [c.c_int, c.c_double, c.c_int, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_apply_robot_speeds",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.POINTER(c.c_double), c.c_size_t, c.POINTER(c.c_double), c.c_size_t, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_apply_robot_speeds",
            c.c_int32,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.POINTER(c.c_double), c.c_size_t, c.POINTER(c.c_double), c.c_size_t, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool]
        ),
        (
            "c_ctre_phoenix6_swerve_drivetrain_set_control_apply_field_speeds",
            None,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.POINTER(c.c_double), c.c_size_t, c.POINTER(c.c_double), c.c_size_t, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool, c.c_int]
        ),
        (
            "c_ctre_phoenix6_swerve_request_apply_apply_field_speeds",
            c.c_int32,
            [c.c_int, c.c_double, c.c_double, c.c_double, c.POINTER(c.c_double), c.c_size_t, c.POINTER(c.c_double), c.c_size_t, c.c_double, c.c_double, c.c_int, c.c_int, c.c_bool, c.c_int]
        ),
    ]
    """
    Function prototypes for C methods in Phoenix 6 API.

    Format is tuple[str, ctype, list[ctype]]

    First Parameter str is name of function
    Second Parameter ctype is return of function
    Third Parameter list[ctype] are the arguments of the function
    """

    @classmethod
    def instance(clazz):
        """
        Get instance of the native class to
        reference Phoenix Tools C API calls.
        """
        if clazz.__instance is None:
            hardware_libs = ["CTRE_PhoenixTools"]
            sim_libs = [
                "CTRE_SimTalonSRX",
                "CTRE_SimVictorSPX",
                "CTRE_SimPigeonIMU",
                "CTRE_SimCANCoder",
                "CTRE_SimProTalonFX",
                "CTRE_SimProCANcoder",
                "CTRE_SimProPigeon2",
                "CTRE_SimProCANrange",
                "CTRE_PhoenixTools_Sim", # Make sure Tools_Sim is loaded last
            ]
            replay_libs = ["CTRE_PhoenixTools_Replay"]

            library_path = pkg_resources.resource_filename("phoenix6", "lib/")
            if os.name == "nt": # Windows will return nt
                extension = ".dll"
                prefix = ""
            elif os.uname().sysname == "Linux": # Perform uname to delineate between mac and linux
                extension = ".so"
                prefix = "lib"
            else:
                extension = ".dylib"
                prefix = "lib"

            # If we have an explicit target, use it; otherwise, use sim and fall back to hardware
            if "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Hardware":
                targets_to_attempt = [hardware_libs]
            elif "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Simulation":
                targets_to_attempt = [sim_libs]
            elif "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Replay":
                targets_to_attempt = [replay_libs]
            else:
                targets_to_attempt = [sim_libs, hardware_libs]

            for libs_to_load in targets_to_attempt:
                # Try to load the libs in this group
                try:
                    for lib in libs_to_load:
                        clazz.__instance = c.cdll.LoadLibrary(library_path + prefix + lib + extension)
                        clazz.__all_c_libs.append(clazz.__instance)
                    success = True
                    break
                except:
                    success = False
            if not success:
                if "CTR_TARGET" in os.environ:
                    raise FileNotFoundError(f"Could not find a CTRE_PhoenixTools {os.environ['CTR_TARGET']} library to load")
                else:
                    raise FileNotFoundError("Could not find an appropriate CTRE_PhoenixTools library to load")

            # And move on to declaring all the C functions we need access to
            for method, rtype, argtypes in clazz.__c_args:
                c_func = clazz.__instance.__getattr__(method)
                c_func.restype = rtype
                c_func.argtypes = argtypes

            # Also load Phoenix 6
            clazz.api_instance()
        return clazz.__instance

    @classmethod
    def api_instance(clazz):
        """
        Get instance of the native class to
        reference Phoenix 6 C API calls.
        """
        if clazz.__api_instance is None:
            # Make sure we load Phoenix Tools first
            clazz.instance()

            hardware_libs = ["CTRE_Phoenix6"]
            sim_libs = ["CTRE_Phoenix6_Sim"]
            replay_libs = ["CTRE_Phoenix6_Replay"]

            library_path = pkg_resources.resource_filename("phoenix6", "lib/")
            if os.name == "nt": # Windows will return nt
                extension = ".dll"
                prefix = ""
            elif os.uname().sysname == "Linux": # Perform uname to delineate between mac and linux
                extension = ".so"
                prefix = "lib"
            else:
                extension = ".dylib"
                prefix = "lib"

            # If we have an explicit target, use it; otherwise, use sim and fall back to hardware
            if "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Hardware":
                targets_to_attempt = [hardware_libs]
            elif "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Simulation":
                targets_to_attempt = [sim_libs]
            elif "CTR_TARGET" in os.environ and os.environ["CTR_TARGET"] == "Replay":
                targets_to_attempt = [replay_libs]
            else:
                targets_to_attempt = [sim_libs, hardware_libs]

            for libs_to_load in targets_to_attempt:
                # Try to load the libs in this group
                try:
                    for lib in libs_to_load:
                        clazz.__api_instance = c.cdll.LoadLibrary(library_path + prefix + lib + extension)
                        clazz.__all_c_libs.append(clazz.__api_instance)
                    success = True
                    break
                except:
                    success = False
            if not success:
                if "CTR_TARGET" in os.environ:
                    raise FileNotFoundError(f"Could not find a CTRE_Phoenix6 {os.environ['CTR_TARGET']} library to load")
                else:
                    raise FileNotFoundError("Could not find an appropriate CTRE_Phoenix6 library to load")

            # And move on to declaring all the C functions we need access to
            for method, rtype, argtypes in clazz.__c_args_api:
                c_func = clazz.__api_instance.__getattr__(method)
                c_func.restype = rtype
                c_func.argtypes = argtypes
        return clazz.__api_instance
