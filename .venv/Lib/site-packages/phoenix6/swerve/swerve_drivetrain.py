"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import copy
import ctypes
from typing import final, overload, Callable, Generic, TypeVar
from threading import RLock
from phoenix6.status_code import StatusCode
from phoenix6.hardware.pigeon2 import Pigeon2
from phoenix6.hardware.traits.common_talon import CommonTalon
from phoenix6.hardware.parent_device import ParentDevice
from phoenix6.signals.spn_enums import NeutralModeValue
from phoenix6.swerve.swerve_drivetrain_constants import SwerveDrivetrainConstants
from phoenix6.swerve.swerve_module_constants import SwerveModuleConstants
from phoenix6.swerve.swerve_module import SwerveModule
from phoenix6.swerve.utility.geometry import *
from phoenix6.swerve.utility.kinematics import *
from phoenix6.swerve import requests
from phoenix6.units import *
from phoenix6.phoenix_native import (
    Native,
    Pose_t,
    SwerveControlParams_t,
    SwerveDriveState_t,
    SwerveModulePosition_t,
    SwerveModuleState_t,
)

try:
    from wpimath.kinematics import (
        SwerveDrive2Kinematics,
        SwerveDrive3Kinematics,
        SwerveDrive4Kinematics,
        SwerveDrive6Kinematics,
    )
    from wpimath.geometry import Rotation3d

    from phoenix6.swerve.sim_swerve_drivetrain import SimSwerveDrivetrain

    USE_WPILIB = True
except ImportError:
    USE_WPILIB = False

class SwerveControlParameters:
    """
    Contains everything the control requests need to calculate the module state.
    """

    def __init__(self):
        self.drivetrain_id = 0
        """ID of the native drivetrain instance, used for native calls"""

        if USE_WPILIB:
            self.kinematics: SwerveDrive2Kinematics | SwerveDrive3Kinematics | SwerveDrive4Kinematics | SwerveDrive6Kinematics = None
            """The kinematics object used for control"""
        self.module_locations: list[Translation2d] = None
        """The locations of the swerve modules"""
        self.max_speed: meters_per_second = 0.0
        """The max speed of the robot at 12 V output, in m/s"""

        self.operator_forward_direction = Rotation2d()
        """The forward direction from the operator perspective"""
        self.current_chassis_speed = ChassisSpeeds()
        """The current chassis speeds of the robot"""
        self.current_pose = Pose2d()
        """The current pose of the robot"""
        self.timestamp: second = 0.0
        """The timestamp of the current control apply, in the timebase of utils.get_current_time_seconds()"""
        self.update_period: second = 0.0
        """The update period of control apply"""

    def _update_from_native(self, control_params: SwerveControlParams_t):
        self.max_speed = control_params.kMaxSpeedMps
        self.operator_forward_direction = Rotation2d(control_params.operatorForwardDirection)
        self.current_chassis_speed.vx = control_params.currentChassisSpeed.vx
        self.current_chassis_speed.vy = control_params.currentChassisSpeed.vy
        self.current_chassis_speed.omega = control_params.currentChassisSpeed.omega
        self.current_pose = Pose2d(
            control_params.currentPose.x,
            control_params.currentPose.y,
            Rotation2d(control_params.currentPose.theta),
        )
        self.timestamp = control_params.timestamp
        self.update_period = control_params.updatePeriod


DriveMotorT = TypeVar("DriveMotorT", bound="CommonTalon")
SteerMotorT = TypeVar("SteerMotorT", bound="CommonTalon")
EncoderT = TypeVar("EncoderT", bound="ParentDevice")

_NUM_CONFIG_ATTEMPTS = 2
"""Number of times to attempt config applies."""

class SwerveDrivetrain(Generic[DriveMotorT, SteerMotorT, EncoderT]):
    """
    Swerve Drive class utilizing CTR Electronics' Phoenix 6 API.

    This class handles the kinematics, configuration, and odometry of a
    swerve drive utilizing CTR Electronics devices. We recommend using
    the Swerve Project Generator in Tuner X to create a template project
    that demonstrates how to use this class.

    This class performs pose estimation internally using a separate odometry
    thread. Vision measurements can be added using add_vision_measurement.
    Other odometry APIs such as reset_pose are also available. The resulting
    pose estimate can be retrieved along with module states and other
    information using get_state. Additionally, the odometry thread synchronously
    provides all new state updates to a telemetry function registered with
    register_telemetry.

    This class will construct the hardware devices internally, so the user
    only specifies the constants (IDs, PID gains, gear ratios, etc).
    Getters for these hardware devices are available.

    If using the generator, the order in which modules are constructed is
    Front Left, Front Right, Back Left, Back Right. This means if you need
    the Back Left module, call get_module(2) to get the third (0-indexed)
    module.
    """

    class SwerveDriveState:
        """
        Plain-Old-Data class holding the state of the swerve drivetrain.
        This encapsulates most data that is relevant for telemetry or
        decision-making from the Swerve Drive.
        """

        def __init__(self):
            self.pose = Pose2d()
            """The current pose of the robot"""
            self.speeds = ChassisSpeeds()
            """The current velocity of the robot"""
            self.module_states: list[SwerveModuleState] = None
            """The current module states"""
            self.module_targets: list[SwerveModuleState] = None
            """The target module states"""
            self.module_positions: list[SwerveModulePosition] = None
            """The current module positions"""
            self.raw_heading = Rotation2d()
            """The raw heading of the robot, unaffected by vision updates and odometry resets"""
            self.timestamp: second = 0.0
            """The timestamp of the state capture, in the timebase of utils.get_current_time_seconds()"""
            self.odometry_period: second = 0.0
            """The measured odometry update period, in seconds"""
            self.successful_daqs = 0
            """Number of successful data acquisitions"""
            self.failed_daqs = 0
            """Number of failed data acquisitions"""

        def __deepcopy__(self, memo) -> 'SwerveDrivetrain.SwerveDriveState':
            """
            Creates a deep copy of this state object.
            This API is not thread-safe.
            """
            to_return = SwerveDrivetrain.SwerveDriveState()
            to_return.pose = self.pose
            to_return.speeds = self.speeds
            to_return.module_states = self.module_states.copy()
            to_return.module_targets = self.module_targets.copy()
            to_return.module_positions = self.module_positions.copy()
            to_return.raw_heading = self.raw_heading
            to_return.timestamp = self.timestamp
            to_return.odometry_period = self.odometry_period
            to_return.successful_daqs = self.successful_daqs
            to_return.failed_daqs = self.failed_daqs
            return to_return

        def _update_from_native(self, state: SwerveDriveState_t):
            self.pose = Pose2d(state.pose.x, state.pose.y, Rotation2d(state.pose.theta))
            self.speeds = ChassisSpeeds(state.speeds.vx, state.speeds.vy, state.speeds.omega)
            for i, _ in enumerate(self.module_states):
                self.module_states[i] = SwerveModuleState(
                    state.moduleStates[i].speed,
                    Rotation2d(state.moduleStates[i].angle)
                )
            for i, _ in enumerate(self.module_targets):
                self.module_targets[i] = SwerveModuleState(
                    state.moduleTargets[i].speed,
                    Rotation2d(state.moduleTargets[i].angle)
                )
            for i, _ in enumerate(self.module_positions):
                self.module_positions[i] = SwerveModulePosition(
                    state.modulePositions[i].distance,
                    Rotation2d(state.modulePositions[i].angle)
                )
            self.raw_heading = Rotation2d(state.rawHeading)
            self.timestamp = state.timestamp
            self.odometry_period = state.odometryPeriod
            self.successful_daqs = state.successfulDaqs
            self.failed_daqs = state.failedDaqs

    class OdometryThread:
        """
        Performs swerve module updates in a separate thread to minimize latency.

        :param drivetrain: ID of the swerve drivetrain
        :type drivetrain: int
        """

        def __init__(self, drivetrain: int):
            self._drivetrain_id = drivetrain

        @final
        def start(self):
            """
            Starts the odometry thread.
            """
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_odom_start(self._drivetrain_id)

        @final
        def stop(self):
            """
            Stops the odometry thread.
            """
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_odom_stop(self._drivetrain_id)

        def is_odometry_valid(self) -> bool:
            """
            Check if the odometry is currently valid.

            :returns: True if odometry is valid
            :rtype: bool
            """
            return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_is_odometry_valid(self._drivetrain_id)

        @final
        def set_thread_priority(self, priority: int):
            """
            Sets the odometry thread priority to a real time priority under the specified priority level

            :param priority: Priority level to set the odometry thread to.
                             This is a value between 0 and 99, with 99 indicating higher
                             priority and 0 indicating lower priority.
            :type priority: int
            """
            Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_odom_set_thread_priority(self._drivetrain_id, priority)

    @overload
    def __init__(
        self,
        drive_motor_type: type[DriveMotorT],
        steer_motor_type: type[SteerMotorT],
        encoder_type: type[EncoderT],
        drivetrain_constants: SwerveDrivetrainConstants,
        modules: list[SwerveModuleConstants]
    ) -> None:
        """
        Constructs a CTRE SwerveDrivetrain using the specified constants.

        This constructs the underlying hardware devices, so users should not construct
        the devices themselves. If they need the devices, they can access them through
        getters in the classes.

        :param drive_motor_type:     Type of the drive motor
        :type drive_motor_type:      type[DriveMotorT]
        :param steer_motor_type:     Type of the steer motor
        :type steer_motor_type:      type[SteerMotorT]
        :param encoder_type:         Type of the azimuth encoder
        :type encoder_type:          type[EncoderT]
        :param drivetrain_constants: Drivetrain-wide constants for the swerve drive
        :type drivetrain_constants:  SwerveDrivetrainConstants
        :param modules:              Constants for each specific module
        :type modules:               list[SwerveModuleConstants]
        """
        ...

    @overload
    def __init__(
        self,
        drive_motor_type: type[DriveMotorT],
        steer_motor_type: type[SteerMotorT],
        encoder_type: type[EncoderT],
        drivetrain_constants: SwerveDrivetrainConstants,
        odometry_update_frequency: hertz,
        modules: list[SwerveModuleConstants]
    ) -> None:
        """
        Constructs a CTRE SwerveDrivetrain using the specified constants.

        This constructs the underlying hardware devices, so users should not construct
        the devices themselves. If they need the devices, they can access them through
        getters in the classes.

        :param drive_motor_type:            Type of the drive motor
        :type drive_motor_type:             type[DriveMotorT]
        :param steer_motor_type:            Type of the steer motor
        :type steer_motor_type:             type[SteerMotorT]
        :param encoder_type:                Type of the azimuth encoder
        :type encoder_type:                 type[EncoderT]
        :param drivetrain_constants:        Drivetrain-wide constants for the swerve drive
        :type drivetrain_constants:         SwerveDrivetrainConstants
        :param odometry_update_frequency:   The frequency to run the odometry loop. If
                                            unspecified or set to 0 Hz, this is 250 Hz on
                                            CAN FD, and 100 Hz on CAN 2.0.
        :type odometry_update_frequency:    hertz
        :param modules:                     Constants for each specific module
        :type modules:                      list[SwerveModuleConstants]
        """
        ...

    @overload
    def __init__(
        self,
        drive_motor_type: type[DriveMotorT],
        steer_motor_type: type[SteerMotorT],
        encoder_type: type[EncoderT],
        drivetrain_constants: SwerveDrivetrainConstants,
        odometry_update_frequency: hertz,
        odometry_standard_deviation: tuple[float, float, float],
        vision_standard_deviation: tuple[float, float, float],
        modules: list[SwerveModuleConstants]
    ) -> None:
        """
        Constructs a CTRE SwerveDrivetrain using the specified constants.

        This constructs the underlying hardware devices, so users should not construct
        the devices themselves. If they need the devices, they can access them through
        getters in the classes.
        
        :param drive_motor_type:            Type of the drive motor
        :type drive_motor_type:             type[DriveMotorT]
        :param steer_motor_type:            Type of the steer motor
        :type steer_motor_type:             type[SteerMotorT]
        :param encoder_type:                Type of the azimuth encoder
        :type encoder_type:                 type[EncoderT]
        :param drivetrain_constants:        Drivetrain-wide constants for the swerve drive
        :type drivetrain_constants:         SwerveDrivetrainConstants
        :param odometry_update_frequency:   The frequency to run the odometry loop. If
                                            unspecified or set to 0 Hz, this is 250 Hz on
                                            CAN FD, and 100 Hz on CAN 2.0.
        :type odometry_update_frequency:    hertz
        :param odometry_standard_deviation: The standard deviation for odometry calculation
                                            in the form [x, y, theta]ᵀ, with units in meters
                                            and radians
        :type odometry_standard_deviation:  tuple[float, float, float]
        :param vision_standard_deviation:   The standard deviation for vision calculation
                                            in the form [x, y, theta]ᵀ, with units in meters
                                            and radians
        :type vision_standard_deviation:    tuple[float, float, float]
        :param modules:                     Constants for each specific module
        :type modules:                      list[SwerveModuleConstants]
        """
        ...

    def __init__(
        self,
        drive_motor_type: type[DriveMotorT],
        steer_motor_type: type[SteerMotorT],
        encoder_type: type[EncoderT],
        drivetrain_constants: SwerveDrivetrainConstants,
        arg0 = None,
        arg1 = None,
        arg2 = None,
        arg3 = None,
    ):
        self._drivetrain_id = 0
        """ID of the native drivetrain instance, used for native calls."""

        if (
            isinstance(arg0, list) and isinstance(arg0[0], SwerveModuleConstants) and
            arg1 is None and
            arg2 is None and
            arg3 is None
        ):
            # Self(drivetrain_constants, modules)
            modules: list[SwerveModuleConstants] = arg0

            native_drive_constants = drivetrain_constants._create_native_instance()
            native_module_constants = SwerveModuleConstants._create_native_instance(modules)

            self._drivetrain_id = Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain(
                native_drive_constants,
                native_module_constants,
                len(modules),
            )

            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_drive_constants, ctypes.c_char_p)))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_module_constants, ctypes.c_char_p)))
        elif (
            isinstance(arg0, (hertz, float)) and
            isinstance(arg1, list) and isinstance(arg1[0], SwerveModuleConstants) and
            arg2 is None and
            arg3 is None
        ):
            # Self(drivetrain_constants, odometry_update_frequency, modules)
            modules: list[SwerveModuleConstants] = arg1

            native_drive_constants = drivetrain_constants._create_native_instance()
            native_module_constants = SwerveModuleConstants._create_native_instance(modules)

            self._drivetrain_id = Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain_with_freq(
                native_drive_constants,
                arg0,
                native_module_constants,
                len(modules),
            )

            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_drive_constants, ctypes.c_char_p)))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_module_constants, ctypes.c_char_p)))
        elif (
            isinstance(arg0, (hertz, float)) and
            isinstance(arg1, tuple[float, float, float]) and
            isinstance(arg2, tuple[float, float, float]) and
            isinstance(arg3, list) and isinstance(arg3[0], SwerveModuleConstants)
        ):
            # Self(drivetrain_constants, odometry_update_frequency, odometry_standard_deviation, vision_standard_deviation, modules)
            modules: list[SwerveModuleConstants] = arg3

            odometry_standard_deviation = (ctypes.c_double * 3)()
            odometry_standard_deviation[0] = arg1[0]
            odometry_standard_deviation[1] = arg1[1]
            odometry_standard_deviation[2] = arg1[2]

            vision_standard_deviation = (ctypes.c_double * 3)()
            vision_standard_deviation[0] = arg2[0]
            vision_standard_deviation[1] = arg2[1]
            vision_standard_deviation[2] = arg2[2]

            native_drive_constants = drivetrain_constants._create_native_instance()
            native_module_constants = SwerveModuleConstants._create_native_instance(modules)

            self._drivetrain_id = Native.api_instance().c_ctre_phoenix6_swerve_create_drivetrain_with_freq(
                native_drive_constants,
                arg0,
                odometry_standard_deviation,
                vision_standard_deviation,
                native_module_constants,
                len(modules),
            )

            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_drive_constants, ctypes.c_char_p)))
            Native.instance().c_ctre_phoenix6_free_memory(ctypes.byref(ctypes.cast(native_module_constants, ctypes.c_char_p)))
        else:
            raise TypeError('Invalid arguments for SwerveDrivetrain.__init__')

        self.__modules: list[SwerveModule[DriveMotorT, SteerMotorT, EncoderT]] = []
        self.__module_locations: list[Translation2d] = []
        for i, module in enumerate(modules):
            self.__modules.append(
                SwerveModule(
                    drive_motor_type,
                    steer_motor_type,
                    encoder_type,
                    module,
                    drivetrain_constants.can_bus_name,
                    self._drivetrain_id,
                    i
                )
            )
            self.__module_locations.append(Translation2d(module.location_x, module.location_y))

        if USE_WPILIB:
            if len(modules) == 2:
                self.__kinematics = SwerveDrive2Kinematics(self.__module_locations[0], self.__module_locations[1])
            elif len(modules) == 3:
                self.__kinematics = SwerveDrive3Kinematics(self.__module_locations[0], self.__module_locations[1], self.__module_locations[2])
            elif len(modules) == 4:
                self.__kinematics = SwerveDrive4Kinematics(self.__module_locations[0], self.__module_locations[1], self.__module_locations[2], self.__module_locations[3])
            elif len(modules) == 6:
                self.__kinematics = SwerveDrive6Kinematics(self.__module_locations[0], self.__module_locations[1], self.__module_locations[2], self.__module_locations[3], self.__module_locations[4], self.__module_locations[5])
            else:
                self.__kinematics = None

        self.__control_params = SwerveControlParameters()
        self.__control_params.drivetrain_id = self._drivetrain_id
        if USE_WPILIB:
            self.__control_params.kinematics = self.__kinematics
        self.__control_params.module_locations = self.__module_locations

        self.__swerve_request: requests.SwerveRequest = requests.Idle()
        self.__control_handle = None

        self.__telemetry_function: Callable[['SwerveDrivetrain.SwerveDriveState'], None] = None
        self.__telemetry_handle = None

        self.__state_lock = RLock()
        self.__cached_state = self.SwerveDriveState()
        self.__cached_state.module_states = [SwerveModuleState() for _ in modules]
        self.__cached_state.module_targets = [SwerveModuleState() for _ in modules]
        self.__cached_state.module_positions = [SwerveModulePosition() for _ in modules]

        self.__pigeon2 = Pigeon2(drivetrain_constants.pigeon2_id, drivetrain_constants.can_bus_name)
        if USE_WPILIB:
            self.__sim_drive = SimSwerveDrivetrain(self.__module_locations, self.__pigeon2.sim_state, modules)

        if drivetrain_constants.pigeon2_configs is not None:
            for _ in range(_NUM_CONFIG_ATTEMPTS):
                retval = self.pigeon2.configurator.apply(drivetrain_constants.pigeon2_configs)
                if retval.is_ok():
                    break
            if not retval.is_ok():
                print(f"Pigeon2 ID {self.pigeon2.device_id} failed to config with error: {retval.name}")

        # do not start thread until after applying Pigeon 2 configs
        self.__odometry_thread = self.OdometryThread(self._drivetrain_id)
        self.__odometry_thread.start()

    def __enter__(self) -> 'SwerveDrivetrain':
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        """
        Closes this SwerveDrivetrain instance.
        """
        Native.instance().c_ctre_phoenix6_swerve_destroy_drivetrain(self._drivetrain_id)
        self._drivetrain_id = 0

    if USE_WPILIB:
        def update_sim_state(self, dt: second, supply_voltage: volt):
            """
            Updates all the simulation state variables for this
            drivetrain class. User provides the update variables for the simulation.
            
            :param dt: time since last update call
            :type dt: second
            :param supply_voltage: voltage as seen at the motor controllers
            :type supply_voltage: volt
            """

            self.__sim_drive.update(dt, supply_voltage, self.__modules)

    @final
    def is_on_can_fd(self) -> bool:
        """
        Gets whether the drivetrain is on a CAN FD bus.

        :returns: True if on CAN FD
        :rtype: bool
        """
        return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_is_on_can_fd(self._drivetrain_id)

    @final
    def get_odometry_frequency(self) -> hertz:
        """
        Gets the target odometry update frequency.

        :returns: Target odometry update frequency
        :rtype: hertz
        """
        return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_get_odometry_frequency(self._drivetrain_id)

    @final
    @property
    def odometry_thread(self) -> OdometryThread:
        """
        Gets a reference to the odometry thread.

        :returns: Odometry thread
        :rtype: OdometryThread
        """
        return self.__odometry_thread

    def is_odometry_valid(self) -> bool:
        """
        Check if the odometry is currently valid.

        :returns: True if odometry is valid
        :rtype: bool
        """
        return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_is_odometry_valid(self._drivetrain_id)

    @final
    @property
    def kinematics(self) -> SwerveDrive2Kinematics | SwerveDrive3Kinematics | SwerveDrive4Kinematics | SwerveDrive6Kinematics:
        """
        Gets a reference to the kinematics used for the drivetrain.

        :returns: Swerve kinematics
        :rtype: SwerveDrive2Kinematics | SwerveDrive3Kinematics | SwerveDrive4Kinematics | SwerveDrive6Kinematics
        """
        return self.__kinematics

    def set_control(self, request: requests.SwerveRequest):
        """
        Applies the specified control request to this swerve drivetrain.

        :param request: Request to apply
        :type request: requests.SwerveRequest
        """
        if self.__swerve_request is not request:
            self.__swerve_request = request

            if request is None:
                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control(self._drivetrain_id, None, None)
                self.__control_handle = None
            elif isinstance(request, requests.NativeSwerveRequest):
                request._apply_native(self._drivetrain_id)
                self.__control_handle = None
            else:
                def control_callback(_, control_params_ptr: ctypes._Pointer):
                    control_params: SwerveControlParams_t = control_params_ptr.contents
                    self.__control_params._update_from_native(control_params)
                    if request:
                        return request.apply(self.__control_params, self.__modules).value
                    else:
                        return StatusCode.OK

                c_control_func_t = ctypes.CFUNCTYPE(ctypes.c_int32, ctypes.c_void_p, ctypes.POINTER(SwerveControlParams_t))
                c_control_func = c_control_func_t(control_callback)

                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control(self._drivetrain_id, None, c_control_func)
                self.__control_handle = c_control_func
        elif isinstance(request, requests.NativeSwerveRequest):
            request._apply_native(self._drivetrain_id)

    @final
    def get_state(self) -> SwerveDriveState:
        """    
        Gets the current state of the swerve drivetrain.
        This includes information such as the pose estimate,
        module states, and chassis speeds.

        :returns: Current state of the drivetrain
        :rtype: SwerveDriveState
        """
        c_module_states = (SwerveModuleState_t * len(self.__modules))()
        c_module_targets = (SwerveModuleState_t * len(self.__modules))()
        c_module_positions = (SwerveModulePosition_t * len(self.__modules))()

        c_state = SwerveDriveState_t()
        c_state.moduleStates = c_module_states
        c_state.moduleTargets = c_module_targets
        c_state.modulePositions = c_module_positions
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_get_state(self._drivetrain_id, ctypes.byref(c_state))

        with self.__state_lock:
            self.__cached_state._update_from_native(c_state)
            return self.__cached_state

    @final
    def get_state_copy(self) -> SwerveDriveState:
        """    
        Gets a copy of the current state of the swerve drivetrain.
        This includes information such as the pose estimate,
        module states, and chassis speeds.

        This can be used to get a thread-safe copy of the state object.

        :returns: Copy of the current state of the drivetrain
        :rtype: SwerveDriveState
        """
        c_module_states = (SwerveModuleState_t * len(self.__modules))()
        c_module_targets = (SwerveModuleState_t * len(self.__modules))()
        c_module_positions = (SwerveModulePosition_t * len(self.__modules))()

        c_state = SwerveDriveState_t()
        c_state.moduleStates = c_module_states
        c_state.moduleTargets = c_module_targets
        c_state.modulePositions = c_module_positions
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_get_state(self._drivetrain_id, ctypes.byref(c_state))

        with self.__state_lock:
            self.__cached_state._update_from_native(c_state)
            return copy.deepcopy(self.__cached_state)

    def register_telemetry(self, telemetry_function: Callable[[SwerveDriveState], None]):
        """
        Register the specified lambda to be executed whenever our SwerveDriveState function
        is updated in our odometry thread.

        It is imperative that this function is cheap, as it will be executed along with
        the odometry call, and if this takes a long time, it may negatively impact
        the odometry of this stack.

        This can also be used for logging data if the function performs logging instead of telemetry.
        Additionally, the SwerveDriveState object can be cloned and stored for later processing.
        
        :param telemetry_function: Function to call for telemetry or logging
        :type telemetry_function: Callable[[SwerveDriveState], None]
        """
        if self.__telemetry_function is not telemetry_function:
            self.__telemetry_function = telemetry_function

            if telemetry_function is None:
                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_register_telemetry(self._drivetrain_id, None)
                self.__telemetry_handle = None
            else:
                def telem_callback(_, state_ptr: ctypes._Pointer):
                    with self.__state_lock:
                        state: SwerveDriveState_t = state_ptr.contents
                        self.__cached_state._update_from_native(state)
                        if telemetry_function:
                            telemetry_function(self.__cached_state)

                c_telem_func_t = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.POINTER(SwerveDriveState_t))
                c_telem_func = c_telem_func_t(telem_callback)

                Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_register_telemetry(self._drivetrain_id, None, c_telem_func)
                self.__telemetry_handle = c_telem_func

    def config_neutral_mode(self, neutral_mode: NeutralModeValue) -> StatusCode:
        """
        Configures the neutral mode to use for all modules' drive motors.

        :param neutral_mode: The drive motor neutral mode
        :type neutral_mode: NeutralModeValue
        :returns: Status code of the first failed config call, or OK if all succeeded
        :rtype: StatusCode
        """
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_config_neutral_mode(self._drivetrain_id, neutral_mode.value))

    def tare_everything(self):
        """
        Zero's this swerve drive's odometry entirely.

        This will zero the entire odometry, and place the robot at 0,0
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_tare_everything(self._drivetrain_id)

    def seed_field_centric(self):
        """
        Resets the rotation of the robot pose to 0 from the
        ForwardPerspectiveValue.OPERATOR_PERSPECTIVE perspective.
        This makes the current orientation of the robot X forward for
        field-centric maneuvers.

        This is equivalent to calling reset_rotation with the operator
        perspective rotation.
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_seed_field_centric(self._drivetrain_id)

    def reset_pose(self, pose: Pose2d):
        """
        Resets the pose of the robot. The pose should be from the
        ForwardPerspectiveValue.BLUE_ALLIANCE perspective.

        :param pose: Pose to make the current pose
        :type pose: Pose2d
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_reset_pose(
            self._drivetrain_id,
            pose.x,
            pose.y,
            pose.rotation().radians(),
        )

    def reset_translation(self, translation: Translation2d):
        """
        Resets the translation of the robot pose without affecting rotation.
        The translation should be from the ForwardPerspectiveValue.BLUE_ALLIANCE
        perspective.

        :param translation: Translation to make the current translation
        :type translation: Translation2d
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_reset_translation(
            self._drivetrain_id,
            translation.x,
            translation.y,
        )

    def reset_rotation(self, rotation: Rotation2d):
        """
        Resets the rotation of the robot pose without affecting translation.
        The rotation should be from the ForwardPerspectiveValue.BLUE_ALLIANCE
        perspective.

        :param rotation: Rotation to make the current rotation
        :type rotation: Rotation2d
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_reset_rotation(self._drivetrain_id, rotation.radians())

    def set_operator_perspective_forward(self, field_direction: Rotation2d):
        """
        Takes the ForwardPerspectiveValue.BLUE_ALLIANCE perpective direction and treats
        it as the forward direction for ForwardPerspectiveValue.OPERATOR_PERSPECTIVE.

        If the operator is in the Blue Alliance Station, this should be 0 degrees.
        If the operator is in the Red Alliance Station, this should be 180 degrees.

        This does not change the robot pose, which is in the
        ForwardPerspectiveValue.BLUE_ALLIANCE perspective. As a result, the robot
        pose may need to be reset using reset_pose.

        :param field_direction: Heading indicating which direction is forward from
                                the ForwardPerspectiveValue.BLUE_ALLIANCE perspective
        :type field_direction: Rotation2d
        """
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_operator_perspective_forward(self._drivetrain_id, field_direction.radians())

    @final
    def get_operator_forward_direction(self) -> Rotation2d:
        """
        Returns the ForwardPerspectiveValue.BLUE_ALLIANCE perpective direction that is
        treated as the forward direction for ForwardPerspectiveValue.OPERATOR_PERSPECTIVE.

        If the operator is in the Blue Alliance Station, this should be 0 degrees.
        If the operator is in the Red Alliance Station, this should be 180 degrees.

        :returns: Heading indicating which direction is forward from
                  the ForwardPerspectiveValue.BLUE_ALLIANCE perspective
        :rtype: Rotation2d
        """
        return Rotation2d(Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_get_operator_forward_direction(self._drivetrain_id))

    def add_vision_measurement(self, vision_robot_pose: Pose2d, timestamp: second, vision_measurement_std_devs: tuple[float, float, float] | None = None):
        """
        Adds a vision measurement to the Kalman Filter. This will correct the
        odometry pose estimate while still accounting for measurement noise.

        This method can be called as infrequently as you want, as long as you are
        calling SwerveDrivePoseEstimator.update every loop.

        To promote stability of the pose estimate and make it robust to bad vision
        data, we recommend only adding vision measurements that are already within
        one meter or so of the current pose estimate.

        Note that the vision measurement standard deviations passed into this method
        will continue to apply to future measurements until a subsequent call to
        SwerveDrivePoseEstimator.setVisionMeasurementStdDevs or this method.

        :param vision_robot_pose:           The pose of the robot as measured by the vision
                                            camera.
        :type vision_robot_pose:            Pose2d
        :param timestamp:                   The timestamp of the vision measurement in
                                            seconds. Note that you must use a timestamp with
                                            an epoch since system startup (i.e., the epoch of
                                            this timestamp is the same epoch as
                                            utils.get_current_time_seconds).
                                            This means that you should use
                                            utils.get_current_time_seconds
                                            as your time source or sync the epochs.
                                            An FPGA timestamp can be converted to the correct
                                            timebase using utils.fpga_to_current_time.
        :type timestamp:                    second
        :param vision_measurement_std_devs: Standard deviations of the vision pose
                                            measurement (x position in meters, y
                                            position in meters, and heading in radians).
                                            Increase these numbers to trust the vision
                                            pose measurement less.
        :type vision_measurement_std_devs:  tuple[float, float, float] | None
        """
        if vision_measurement_std_devs is not None:
            c_vision_measurement_std_devs = (ctypes.c_double * 3)()
            c_vision_measurement_std_devs[0] = vision_measurement_std_devs[0]
            c_vision_measurement_std_devs[1] = vision_measurement_std_devs[1]
            c_vision_measurement_std_devs[2] = vision_measurement_std_devs[2]

            return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_add_vision_measurement_with_stddev(
                self._drivetrain_id,
                vision_robot_pose.x,
                vision_robot_pose.y,
                vision_robot_pose.rotation().radians(),
                timestamp,
                c_vision_measurement_std_devs,
            )
        else:
            return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_add_vision_measurement(
                self._drivetrain_id,
                vision_robot_pose.x,
                vision_robot_pose.y,
                vision_robot_pose.rotation().radians(),
                timestamp,
            )

    def set_vision_measurement_std_devs(self, vision_measurement_std_devs: tuple[float, float, float]):
        """
        Sets the pose estimator's trust of global measurements. This might be used to
        change trust in vision measurements after the autonomous period, or to change
        trust as distance to a vision target increases.

        :param vision_measurement_std_devs: Standard deviations of the vision
                                            measurements. Increase these numbers to
                                            trust global measurements from vision less.
                                            This matrix is in the form [x, y, theta]ᵀ,
                                            with units in meters and radians.
        :type vision_measurement_std_devs:  tuple[float, float, float]
        """
        c_vision_measurement_std_devs = (ctypes.c_double * 3)()
        c_vision_measurement_std_devs[0] = vision_measurement_std_devs[0]
        c_vision_measurement_std_devs[1] = vision_measurement_std_devs[1]
        c_vision_measurement_std_devs[2] = vision_measurement_std_devs[2]

        return Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_vision_measurement_stddevs(self._drivetrain_id, c_vision_measurement_std_devs)

    def sample_pose_at(self, timestamp: second) -> Pose2d | None:
        """
        Return the pose at a given timestamp, if the buffer is not empty.

        :param timestamp: The pose's timestamp. Note that you must use a timestamp
                          with an epoch since system startup (i.e., the epoch of
                          this timestamp is the same epoch as
                          utils.get_current_time_seconds). This means that you
                          should use utils.get_current_time_seconds as your
                          time source in this case.
                          An FPGA timestamp can be converted to the correct
                          timebase using utils.fpga_to_current_time.
        :type timestamp: second
        :returns: The pose at the given timestamp (or None if the buffer is empty).
        :rtype: Pose2d | None
        """
        c_pose = Pose_t()
        retval = Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_sample_pose_at(self._drivetrain_id, timestamp, ctypes.byref(c_pose))
        if not retval:
            return None
        return Pose2d(c_pose.x, c_pose.y, Rotation2d(c_pose.theta))

    @final
    def get_module(self, index: int) -> SwerveModule[DriveMotorT, SteerMotorT, EncoderT]:
        """
        Get a reference to the module at the specified index.
        The index corresponds to the module described in the constructor.

        :param index: Which module to get
        :type index: int
        :returns: Reference to SwerveModule
        :rtype: SwerveModule[DriveMotorT, SteerMotorT, EncoderT]
        """
        return self.__modules[index]

    @final
    @property
    def modules(self) -> list[SwerveModule[DriveMotorT, SteerMotorT, EncoderT]]:
        """
        Get a reference to the full array of modules.
        The indexes correspond to the module described in the constructor.

        :returns: Reference to the SwerveModule array
        :rtype: list[SwerveModule[DriveMotorT, SteerMotorT, EncoderT]]
        """
        return self.__modules

    @final
    @property
    def module_locations(self) -> list[Translation2d]:
        """
        Gets the locations of the swerve modules.

        :returns: Reference to the array of swerve module locations
        :rtype: list[Translation2d]
        """
        return self.__module_locations

    if USE_WPILIB:
        @final
        def get_rotation3d(self) -> Rotation3d:
            """
            Gets the current orientation of the robot as a Rotation3d from
            the Pigeon 2 quaternion values.

            :returns: The robot orientation as a Rotation3d
            :rtype: Rotation3d
            """
            return self.pigeon2.getRotation3d()

    @final
    @property
    def pigeon2(self) -> Pigeon2:
        """
        Gets this drivetrain's Pigeon 2 reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This drivetrain's Pigeon 2 reference
        :rtype: Pigeon2
        """
        return self.__pigeon2
