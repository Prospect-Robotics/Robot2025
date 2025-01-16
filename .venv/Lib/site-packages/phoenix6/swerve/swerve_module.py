"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from enum import Enum
from typing import final, overload, Generic, TypeVar
from threading import RLock
from phoenix6.units import newton
from phoenix6.configs.cancoder_configs import CANcoderConfiguration
from phoenix6.configs.candi_configs import CANdiConfiguration
from phoenix6.configs.talon_fx_configs import TalonFXConfiguration
from phoenix6.configs.talon_fxs_configs import TalonFXSConfiguration
from phoenix6.hardware.cancoder import CANcoder
from phoenix6.hardware.candi import CANdi
from phoenix6.hardware.talon_fx import TalonFX
from phoenix6.hardware.traits.common_talon import CommonTalon
from phoenix6.hardware.parent_device import ParentDevice, SupportsSendRequest
from phoenix6.signals.spn_enums import (
    BrushedMotorWiringValue,
    ExternalFeedbackSensorSourceValue,
    FeedbackSensorSourceValue,
    InvertedValue,
    MotorArrangementValue,
    NeutralModeValue,
    SensorDirectionValue,
    SensorPhaseValue
)
from phoenix6.swerve.utility.geometry import *
from phoenix6.swerve.utility.kinematics import *
from phoenix6.swerve.swerve_module_constants import (
    ClosedLoopOutputType,
    DriveMotorArrangement,
    SteerMotorArrangement,
    SteerFeedbackType,
    SwerveModuleConstants
)
from phoenix6.phoenix_native import Native, SwerveModuleRequest_t, SwerveModuleState_t

DriveMotorT = TypeVar("DriveMotorT", bound="CommonTalon")
SteerMotorT = TypeVar("SteerMotorT", bound="CommonTalon")
EncoderT = TypeVar("EncoderT", bound="ParentDevice")

_NUM_CONFIG_ATTEMPTS = 2
"""Number of times to attempt config applies."""

class SwerveModule(Generic[DriveMotorT, SteerMotorT, EncoderT]):
    """
    Swerve Module class that encapsulates a swerve module powered by CTR
    Electronics devices.

    This class handles the hardware devices and configures them for
    swerve module operation using the Phoenix 6 API.

    This class constructs hardware devices internally, so the user
    only specifies the constants (IDs, PID gains, gear ratios, etc).
    Getters for these hardware devices are available.

    :param drive_motor_type: Type of the drive motor
    :type drive_motor_type:  type[DriveMotorT]
    :param steer_motor_type: Type of the steer motor
    :type steer_motor_type:  type[SteerMotorT]
    :param encoder_type:     Type of the azimuth encoder
    :type encoder_type:      type[EncoderT]
    :param constants:        Constants used to construct the module
    :type constants:         SwerveModuleConstants
    :param canbus_name:      The name of the CAN bus this module is on
    :type canbus_name:       str
    :param drivetrain_id:    ID of the swerve drivetrain
    :type drivetrain_id:     int
    :param index:            Index of this swerve module
    :type index:             int
    """

    class SteerRequestType(Enum):
        """
        All possible control requests for the module steer motor.
        """

        MOTION_MAGIC_EXPO = 0
        """
        Control the drive motor using a Motion Magic® Expo request.
        The control output type is determined by SwerveModuleConstants.SteerMotorClosedLoopOutput
        """
        POSITION = 1
        """
        Control the drive motor using an unprofiled position request.
        The control output type is determined by SwerveModuleConstants.SteerMotorClosedLoopOutput
        """

    class DriveRequestType(Enum):
        OPEN_LOOP_VOLTAGE = 0
        """
        Control the drive motor using an open-loop voltage request.
        """
        VELOCITY = 1
        """
        Control the drive motor using a velocity closed-loop request.
        The control output type is determined by SwerveModuleConstants.DriveMotorClosedLoopOutput
        """

    class ModuleRequest:
        """
        Contains everything the swerve module needs to apply a request.
        """

        def __init__(self):
            self.state = SwerveModuleState()
            """
            Unoptimized speed and direction the module should target.
            """

            self.wheel_force_feedforward_x: newton = 0.0
            """
            Robot-centric wheel force feedforward to apply in the
            X direction. X is defined as forward according to WPILib
            convention, so this determines the forward force to apply.

            This force should include friction applied to the ground.
            """
            self.wheel_force_feedforward_y: newton = 0.0
            """
            Robot-centric wheel force feedforward to apply in the
            Y direction. Y is defined as to the left according to WPILib
            convention, so this determines the force to apply to the left.

            This force should include friction applied to the ground.
            """

            self.drive_request = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            """
            The type of control request to use for the drive motor.
            """
            self.steer_request = SwerveModule.SteerRequestType.POSITION
            """
            The type of control request to use for the steer motor.
            """

            self.update_period: second = 0.0
            """
            The update period of the module request. Setting this to a
            non-zero value adds a velocity feedforward to the steer motor.
            """

            self.enable_foc = True
            """
            When using Voltage-based control, set to true (default) to use FOC commutation
            (requires Phoenix Pro), which increases peak power by ~15%. Set to false to
            use trapezoidal commutation. This is ignored when using Torque-based control,
            which always uses FOC.

            FOC improves motor performance by leveraging torque (current) control. 
            However, this may be inconvenient for applications that require specifying
            duty cycle or voltage.  CTR-Electronics has developed a hybrid method that
            combines the performances gains of FOC while still allowing applications to
            provide duty cycle or voltage demand.  This not to be confused with simple
            sinusoidal control or phase voltage control which lacks the performance
            gains.
            """

        def with_state(self, new_state: SwerveModuleState) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the state parameter and returns itself.

            Unoptimized speed and direction the module should target.

            :param new_state: Parameter to modify
            :type new_state: SwerveModuleState
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.state = new_state
            return self

        def with_wheel_force_feedforward_x(self, new_wheel_force_feedforward_x: newton) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the wheel_force_feedforward_x parameter and returns itself.

            Robot-centric wheel force feedforward to apply in the
            X direction. X is defined as forward according to WPILib
            convention, so this determines the forward force to apply.

            This force should include friction applied to the ground.

            :param wheel_force_feedforward_x: Parameter to modify
            :type wheel_force_feedforward_x: newton
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.wheel_force_feedforward_x = new_wheel_force_feedforward_x
            return self

        def with_wheel_force_feedforward_y(self, new_wheel_force_feedforward_y: newton) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the wheel_force_feedforward_y parameter and returns itself.

            Robot-centric wheel force feedforward to apply in the
            Y direction. Y is defined as to the left according to WPILib
            convention, so this determines the force to apply to the left.

            This force should include friction applied to the ground.

            :param wheel_force_feedforward_y: Parameter to modify
            :type wheel_force_feedforward_y: newton
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.wheel_force_feedforward_y = new_wheel_force_feedforward_y
            return self

        def with_drive_request(self, new_drive_request: 'SwerveModule.DriveRequestType') -> 'SwerveModule.ModuleRequest':
            """
            Modifies the drive_request parameter and returns itself.

            The type of control request to use for the drive motor.

            :param new_drive_request: Parameter to modify
            :type new_drive_request: SwerveModule.DriveRequestType
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.drive_request = new_drive_request
            return self

        def with_steer_request(self, new_steer_request: 'SwerveModule.SteerRequestType') -> 'SwerveModule.ModuleRequest':
            """
            Modifies the steer_request parameter and returns itself.

            The type of control request to use for the steer motor.

            :param new_steer_request: Parameter to modify
            :type new_steer_request: SwerveModule.SteerRequestType
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.steer_request = new_steer_request
            return self

        def with_update_period(self, new_update_period: second) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the update_period parameter and returns itself.

            The update period of the module request. Setting this to a
            non-zero value adds a velocity feedforward to the steer motor.

            :param new_update_period: Parameter to modify
            :type new_update_period: second
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.update_period = new_update_period
            return self

        def with_enable_foc(self, new_enable_foc: bool) -> 'SwerveModule.ModuleRequest':
            """
            Modifies the enable_foc parameter and returns itself.

            When using Voltage-based control, set to true (default) to use FOC commutation
            (requires Phoenix Pro), which increases peak power by ~15%. Set to false to
            use trapezoidal commutation. This is ignored when using Torque-based control,
            which always uses FOC.

            FOC improves motor performance by leveraging torque (current) control. 
            However, this may be inconvenient for applications that require specifying
            duty cycle or voltage.  CTR-Electronics has developed a hybrid method that
            combines the performances gains of FOC while still allowing applications to
            provide duty cycle or voltage demand.  This not to be confused with simple
            sinusoidal control or phase voltage control which lacks the performance
            gains.

            :param new_enable_foc: Parameter to modify
            :type new_enable_foc: bool
            :returns: Itself
            :rtype: SwerveModule.ModuleRequest
            """
            self.enable_foc = new_enable_foc
            return self

    def __init__(
        self,
        drive_motor_type: type[DriveMotorT],
        steer_motor_type: type[SteerMotorT],
        encoder_type: type[EncoderT],
        constants: SwerveModuleConstants,
        canbus_name: str,
        drivetrain_id: int,
        index: int
    ):
        self._drivetrain_id = drivetrain_id
        """ID of the native drivetrain instance, used for native calls."""
        self._module_idx = index
        """Index of this module in the native drivetrain, used for native calls."""

        self.__current_position = SwerveModulePosition()
        self.__current_state = SwerveModuleState()
        self.__target_state = SwerveModuleState()
        self.__state_lock = RLock()

        self.__drive_motor = drive_motor_type(constants.drive_motor_id, canbus_name)
        self.__steer_motor = steer_motor_type(constants.steer_motor_id, canbus_name)
        self.__encoder = encoder_type(constants.encoder_id, canbus_name)

        self.__drive_closed_loop_output = constants.drive_motor_closed_loop_output
        self.__steer_closed_loop_output = constants.steer_motor_closed_loop_output

        drive_configs = constants.drive_motor_initial_configs
        drive_configs.motor_output.neutral_mode = NeutralModeValue.BRAKE

        drive_configs.slot0 = constants.drive_motor_gains
        if isinstance(drive_configs, TalonFXConfiguration):
            drive_configs.torque_current.peak_forward_torque_current = constants.slip_current
            drive_configs.torque_current.peak_reverse_torque_current = -constants.slip_current
        drive_configs.current_limits.stator_current_limit = constants.slip_current
        drive_configs.current_limits.stator_current_limit_enable = True

        if isinstance(drive_configs, TalonFXSConfiguration):
            if constants.drive_motor_type == DriveMotorArrangement.TALON_FX_INTEGRATED:
                print(f"Cannot use TalonFX_Integrated drive motor type on Talon FXS ID {self.drive_motor.device_id}. TalonFX_Integrated is only supported on Talon FX.")
            elif constants.drive_motor_type == DriveMotorArrangement.TALON_FXS_NEO_JST:
                drive_configs.commutation.motor_arrangement = MotorArrangementValue.NEO_JST
            elif constants.drive_motor_type == DriveMotorArrangement.TALON_FXS_VORTEX_JST:
                drive_configs.commutation.motor_arrangement = MotorArrangementValue.VORTEX_JST
        else:
            if constants.drive_motor_type != DriveMotorArrangement.TALON_FX_INTEGRATED:
                print(f"Drive motor Talon FX ID {self.drive_motor.device_id} only supports TalonFX_Integrated.")

        drive_configs.motor_output.inverted = (
            InvertedValue.CLOCKWISE_POSITIVE
            if constants.drive_motor_inverted
            else InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        )
        for _ in range(_NUM_CONFIG_ATTEMPTS):
            response = self.drive_motor.configurator.apply(drive_configs)
            if response.is_ok():
                break
        if not response.is_ok():
            print(f"Talon ID {self.drive_motor.device_id} failed config with error {response.name}")

        steer_configs = constants.steer_motor_initial_configs
        steer_configs.motor_output.neutral_mode = NeutralModeValue.BRAKE

        steer_configs.slot0 = constants.steer_motor_gains
        if isinstance(steer_configs, TalonFXSConfiguration):
            if constants.steer_motor_type == SteerMotorArrangement.TALON_FX_INTEGRATED:
                print(f"Cannot use TalonFX_Integrated steer motor type on Talon FXS ID {self.steer_motor.device_id}. TalonFX_Integrated is only supported on Talon FX.")
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_MINION_JST:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.MINION_JST
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_NEO_JST:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.NEO_JST
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_VORTEX_JST:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.VORTEX_JST
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_NEO550_JST:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.NEO550_JST
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_BRUSHED_AB:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.BRUSHED_DC
                steer_configs.commutation.brushed_motor_wiring = BrushedMotorWiringValue.LEADS_A_AND_B
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_BRUSHED_AC:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.BRUSHED_DC
                steer_configs.commutation.brushed_motor_wiring = BrushedMotorWiringValue.LEADS_A_AND_C
            elif constants.steer_motor_type == SteerMotorArrangement.TALON_FXS_BRUSHED_BC:
                steer_configs.commutation.motor_arrangement = MotorArrangementValue.BRUSHED_DC
                steer_configs.commutation.brushed_motor_wiring = BrushedMotorWiringValue.LEADS_B_AND_C

            # Modify configuration to use remote encoder setting
            steer_configs.external_feedback.external_feedback_remote_sensor_id = constants.encoder_id
            if constants.feedback_source is SteerFeedbackType.FUSED_CANCODER:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.FUSED_CANCODER
            elif constants.feedback_source is SteerFeedbackType.SYNC_CANCODER:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.SYNC_CANCODER
            elif constants.feedback_source is SteerFeedbackType.REMOTE_CANCODER:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.REMOTE_CANCODER
            elif constants.feedback_source is SteerFeedbackType.FUSED_CANDI_PWM1:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.FUSED_CANDI_PWM1
            elif constants.feedback_source is SteerFeedbackType.FUSED_CANDI_PWM2:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.FUSED_CANDI_PWM2
            elif constants.feedback_source is SteerFeedbackType.SYNC_CANDI_PWM1:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.SYNC_CANDI_PWM1
            elif constants.feedback_source is SteerFeedbackType.SYNC_CANDI_PWM2:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.SYNC_CANDI_PWM2
            elif constants.feedback_source is SteerFeedbackType.REMOTE_CANDI_PWM1:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.REMOTE_CANDI_PWM1
            elif constants.feedback_source is SteerFeedbackType.REMOTE_CANDI_PWM2:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.REMOTE_CANDI_PWM2
            elif constants.feedback_source is SteerFeedbackType.TALON_FXS_PULSE_WIDTH:
                steer_configs.external_feedback.external_feedback_sensor_source = ExternalFeedbackSensorSourceValue.PULSE_WIDTH
                steer_configs.external_feedback.absolute_sensor_offset = constants.encoder_offset
                steer_configs.external_feedback.sensor_phase = (
                    SensorPhaseValue.OPPOSED
                    if constants.encoder_inverted
                    else SensorPhaseValue.ALIGNED
                )
            steer_configs.external_feedback.rotor_to_sensor_ratio = constants.steer_motor_gear_ratio
        else:
            if constants.steer_motor_type != SteerMotorArrangement.TALON_FX_INTEGRATED:
                print(f"Steer motor Talon FX ID {self.steer_motor.device_id} only supports TalonFX_Integrated.")

            # Modify configuration to use remote encoder setting
            steer_configs.feedback.feedback_remote_sensor_id = constants.encoder_id
            if constants.feedback_source is SteerFeedbackType.FUSED_CANCODER:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.FUSED_CANCODER
            elif constants.feedback_source is SteerFeedbackType.SYNC_CANCODER:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.SYNC_CANCODER
            elif constants.feedback_source is SteerFeedbackType.REMOTE_CANCODER:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANCODER
            elif constants.feedback_source is SteerFeedbackType.FUSED_CANDI_PWM1:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.FUSED_CANDI_PWM1
            elif constants.feedback_source is SteerFeedbackType.FUSED_CANDI_PWM2:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.FUSED_CANDI_PWM2
            elif constants.feedback_source is SteerFeedbackType.SYNC_CANDI_PWM1:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.SYNC_CANDI_PWM1
            elif constants.feedback_source is SteerFeedbackType.SYNC_CANDI_PWM2:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.SYNC_CANDI_PWM2
            elif constants.feedback_source is SteerFeedbackType.REMOTE_CANDI_PWM1:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANDI_PWM1
            elif constants.feedback_source is SteerFeedbackType.REMOTE_CANDI_PWM2:
                steer_configs.feedback.feedback_sensor_source = FeedbackSensorSourceValue.REMOTE_CANDI_PWM2
            elif constants.feedback_source is SteerFeedbackType.TALON_FXS_PULSE_WIDTH:
                print(f"Cannot use Pulse Width steer feedback type on Talon FX ID {self.steer_motor.device_id}. Pulse Width is only supported on Talon FXS.")
            steer_configs.feedback.rotor_to_sensor_ratio = constants.steer_motor_gear_ratio

        steer_configs.motion_magic.motion_magic_expo_k_v = 0.12 * constants.steer_motor_gear_ratio
        steer_configs.motion_magic.motion_magic_expo_k_a = 0.8 / constants.steer_motor_gear_ratio

        # Enable continuous wrap for swerve modules
        steer_configs.closed_loop_general.continuous_wrap = True

        steer_configs.motor_output.inverted = (
            InvertedValue.CLOCKWISE_POSITIVE
            if constants.steer_motor_inverted
            else InvertedValue.COUNTER_CLOCKWISE_POSITIVE
        )
        for _ in range(_NUM_CONFIG_ATTEMPTS):
            response = self.steer_motor.configurator.apply(steer_configs)
            if response.is_ok():
                break
        if not response.is_ok():
            print(f"Talon ID {self.steer_motor.device_id} failed config with error {response.name}")

        encoder_configs = constants.encoder_initial_configs
        if isinstance(encoder_configs, CANcoderConfiguration):
            encoder_configs.magnet_sensor.magnet_offset = constants.encoder_offset
            encoder_configs.magnet_sensor.sensor_direction = (
                SensorDirectionValue.CLOCKWISE_POSITIVE
                if constants.encoder_inverted
                else SensorDirectionValue.COUNTER_CLOCKWISE_POSITIVE
            )
            for _ in range(_NUM_CONFIG_ATTEMPTS):
                response = self.encoder.configurator.apply(encoder_configs)
                if response.is_ok():
                    break
            if not response.is_ok():
                print(f"Encoder ID {self.encoder.device_id} failed config with error {response.name}")
        elif isinstance(encoder_configs, CANdiConfiguration):
            for _ in range(_NUM_CONFIG_ATTEMPTS):
                response = self.encoder.configurator.apply(encoder_configs.digital_inputs)
                if response.is_ok():
                    break
            if not response.is_ok():
                print(f"Encoder ID {self.encoder.device_id} failed config with error {response.name}")

            for _ in range(_NUM_CONFIG_ATTEMPTS):
                response = self.encoder.configurator.apply(encoder_configs.custom_params)
                if response.is_ok():
                    break
            if not response.is_ok():
                print(f"Encoder ID {self.encoder.device_id} failed config with error {response.name}")

            if constants.feedback_source in [
                SteerFeedbackType.FUSED_CANDI_PWM1,
                SteerFeedbackType.SYNC_CANDI_PWM1,
                SteerFeedbackType.REMOTE_CANDI_PWM1
            ]:
                encoder_configs.pwm1.absolute_sensor_offset = constants.encoder_offset
                encoder_configs.pwm1.sensor_direction = constants.encoder_inverted
                for _ in range(_NUM_CONFIG_ATTEMPTS):
                    response = self.encoder.configurator.apply(encoder_configs.pwm1)
                    if response.is_ok():
                        break
                if not response.is_ok():
                    print(f"Encoder ID {self.encoder.device_id} failed config with error {response.name}")
            elif constants.feedback_source in [
                SteerFeedbackType.FUSED_CANDI_PWM2,
                SteerFeedbackType.SYNC_CANDI_PWM2,
                SteerFeedbackType.REMOTE_CANDI_PWM2
            ]:
                encoder_configs.pwm2.absolute_sensor_offset = constants.encoder_offset
                encoder_configs.pwm2.sensor_direction = constants.encoder_inverted
                for _ in range(_NUM_CONFIG_ATTEMPTS):
                    response = self.encoder.configurator.apply(encoder_configs.pwm2)
                    if response.is_ok():
                        break
                if not response.is_ok():
                    print(f"Encoder ID {self.encoder.device_id} failed config with error {response.name}")

    @overload
    def apply(self, module_request: ModuleRequest):
        """
        Applies the desired ModuleRequest to this module.

        :param module_request: The request to apply to this module
        :type module_request:  ModuleRequest
        """
        ...

    @overload
    def apply(self, drive_request: SupportsSendRequest, steer_request: SupportsSendRequest):
        """
        Controls this module using the specified drive and steer control requests.

        This is intended only to be used for characterization of the robot; do not use this for normal use.

        :param drive_request: The control request to apply to the drive motor
        :type drive_request: SupportsSendRequest
        :param steer_request: The control request to apply to the steer motor
        :type steer_request: SupportsSendRequest
        """
        ...

    def apply(self, arg1 = None, arg2 = None):
        if isinstance(arg1, self.ModuleRequest) and arg2 is None:
            # self.apply(module_request)
            module_request = arg1

            c_state = SwerveModuleState_t()
            c_state.speed = module_request.state.speed
            c_state.angle = module_request.state.angle.radians()

            c_module_request = SwerveModuleRequest_t()
            c_module_request.state = c_state
            c_module_request.wheelForceFeedforwardX = module_request.wheel_force_feedforward_x
            c_module_request.wheelForceFeedforwardY = module_request.wheel_force_feedforward_y
            c_module_request.driveRequest = module_request.drive_request.value
            c_module_request.steerRequest = module_request.steer_request.value
            c_module_request.updatePeriod = module_request.update_period
            c_module_request.enableFOC = module_request.enable_foc

            Native.api_instance().c_ctre_phoenix6_swerve_module_apply(
                self._drivetrain_id,
                self._module_idx,
                ctypes.byref(c_module_request),
            )
        elif arg1 is not None and arg2 is not None:
            # self.apply(drive_request, steer_request)
            drive_request: SupportsSendRequest = arg1
            steer_request: SupportsSendRequest = arg2

            self.drive_motor.set_control(drive_request.with_update_freq_hz(0))
            self.steer_motor.set_control(steer_request.with_update_freq_hz(0))
        else:
            raise TypeError('Invalid arguments for SwerveModule.apply')

    @final
    def get_position(self, refresh: bool) -> SwerveModulePosition:
        """
        Gets the state of this module and passes it back as a
        SwerveModulePosition object with latency compensated values.

        This function is blocking when it performs a refresh.

        :param refresh: True if the signals should be refreshed
        :type refresh: bool
        :returns: SwerveModulePosition containing this module's state
        :rtype: SwerveModulePosition
        """
        with self.__state_lock:
            c_position = Native.api_instance().c_ctre_phoenix6_swerve_module_get_position(self._drivetrain_id, self._module_idx, refresh)
            self.__current_position.distance = c_position.distance
            self.__current_position.angle = Rotation2d(c_position.angle)
            return self.__current_position

    @final
    def get_cached_position(self) -> SwerveModulePosition:
        """
        Gets the last cached swerve module position.
        This differs from get_position in that it will not
        perform any latency compensation or refresh the signals.

        :returns: Last cached SwerveModulePosition
        :rtype: SwerveModulePosition
        """
        with self.__state_lock:
            c_position = Native.api_instance().c_ctre_phoenix6_swerve_module_get_cached_position(self._drivetrain_id, self._module_idx)
            self.__current_position.distance = c_position.distance
            self.__current_position.angle = Rotation2d(c_position.angle)
            return self.__current_position

    @final
    def get_current_state(self) -> SwerveModuleState:
        """
        Get the current state of the module.

        This is typically used for telemetry, as the
        SwerveModulePosition is used for odometry.

        :returns: Current state of the module
        :rtype: SwerveModuleState
        """
        with self.__state_lock:
            c_state = Native.api_instance().c_ctre_phoenix6_swerve_module_get_current_state(self._drivetrain_id, self._module_idx)
            self.__current_state.speed = c_state.speed
            self.__current_state.angle = Rotation2d(c_state.angle)
            return self.__current_state

    @final
    def get_target_state(self) -> SwerveModuleState:
        """
        Get the target state of the module.

        This is typically used for telemetry.

        :returns: Target state of the module
        :rtype: SwerveModuleState
        """
        with self.__state_lock:
            c_state = Native.api_instance().c_ctre_phoenix6_swerve_module_get_target_state(self._drivetrain_id, self._module_idx)
            self.__target_state.speed = c_state.speed
            self.__target_state.angle = Rotation2d(c_state.angle)
            return self.__target_state

    def reset_position(self):
        """
        Resets this module's drive motor position to 0 rotations.
        """
        Native.api_instance().c_ctre_phoenix6_swerve_module_reset_position(self._drivetrain_id, self._module_idx)

    @final
    @property
    def drive_closed_loop_output_type(self) -> ClosedLoopOutputType:
        """
        Gets the closed-loop output type to use for the drive motor.

        :returns: Drive motor closed-loop output type
        :rtype: ClosedLoopOutputType
        """
        return self.__drive_closed_loop_output

    @final
    @property
    def steer_closed_loop_output_type(self) -> ClosedLoopOutputType:
        """
        Gets the closed-loop output type to use for the steer motor.

        :returns: Steer motor closed-loop output type
        :rtype: ClosedLoopOutputType
        """
        return self.__steer_closed_loop_output

    @final
    @property
    def drive_motor(self) -> DriveMotorT:
        """
        Gets this module's Drive Motor reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This module's Drive Motor reference
        :rtype: DriveMotorT
        """
        return self.__drive_motor

    @final
    @property
    def steer_motor(self) -> SteerMotorT:
        """
        Gets this module's Steer Motor reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This module's Steer Motor reference
        :rtype: SteerMotorT
        """
        return self.__steer_motor

    @final
    @property
    def encoder(self) -> EncoderT:
        """
        Gets this module's azimuth encoder reference.

        This should be used only to access signals and change configurations that the
        swerve drivetrain does not configure itself.

        :returns: This module's azimuth encoder reference
        :rtype: EncoderT
        """
        return self.__encoder
