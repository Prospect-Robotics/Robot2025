"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
import math
from enum import Enum
from typing import Protocol, runtime_checkable, TYPE_CHECKING
from phoenix6.status_code import StatusCode
from phoenix6.swerve.utility.geometry import *
from phoenix6.swerve.utility.kinematics import *
from phoenix6.swerve.utility.phoenix_pid_controller import PhoenixPIDController
from phoenix6.swerve.swerve_module import SwerveModule
from phoenix6.swerve.swerve_module_constants import ClosedLoopOutputType
from phoenix6.controls.coast_out import CoastOut
from phoenix6.controls.position_torque_current_foc import PositionTorqueCurrentFOC
from phoenix6.controls.position_voltage import PositionVoltage
from phoenix6.controls.voltage_out import VoltageOut
from phoenix6.units import *
from phoenix6.phoenix_native import Native

if TYPE_CHECKING:
    from phoenix6.swerve.swerve_drivetrain import SwerveControlParameters

try:
    import wpimath.kinematics # pylint: disable=unused-import
    USE_WPILIB = True
except ImportError:
    USE_WPILIB = False

class ForwardPerspectiveValue(Enum):
    """
    In field-centric control, the direction of "forward" is sometimes different
    depending on perspective. This addresses which forward to use.
    """

    OPERATOR_PERSPECTIVE = 0
    """
    "Forward" (positive X) is determined from the operator's perspective. This
    is important for most teleop driven field-centric requests, where positive
    X means to drive away from the operator.

    Important: Users must specify the operator_perspective in the SwerveDrivetrain object
    """
    BLUE_ALLIANCE = 1
    """
    "Forward" (positive X) is always from the perspective of the blue alliance (i.e. towards
    the red alliance). This is important in situations such as path following where positive
    X is always from the blue alliance perspective, regardless of where the operator is
    physically located.
    """

class SwerveRequest(Protocol):
    """
    Container for all the Swerve Requests. Use this to find all applicable swerve
    drive requests.

    This is also an interface common to all swerve drive control requests that
    allow the request to calculate the state to apply to the modules.
    """

    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        """
        Applies this swerve request to the given modules. This is
        typically called by the SwerveDrivetrain odometry thread.

        For native swerve requests, this API can be called from a
        non-native request's apply to compose the two together.

        :param parameters: Parameters the control request needs to calculate the module state
        :type parameters: SwerveControlParameters
        :param modules_to_apply: Modules to which the control request is applied
        :type modules_to_apply: list[SwerveModule]
        :returns: Status code of sending the request
        :rtype: StatusCode
        """
        pass

@runtime_checkable
class NativeSwerveRequest(SwerveRequest, Protocol):
    """
    Swerve requests implemented in native code.
    """

    def _apply_native(self, id: int):
        """
        Applies a native swerve request to the native drivetrain with the provided ID.

        When this is implemented, the regular apply() function should do nothing
        (return OK). Additionally, this cannot be called from another swerve request's
        apply method, as this overrides the native swerve request of the drivetrain.

        Unlike apply(), this function is called every time SwerveDrivetrain.set_control()
        is run, not every loop of the odometry thread. Instead, the underlying native
        request is run at the full update frequency of the odometry thread.

        :param id: ID of the native swerve drivetrain
        :type id: int
        """
        pass


class Idle(NativeSwerveRequest):
    """
    Does nothing to the swerve module state. This is the default state of a newly
    created swerve drive mechanism.
    """

    def __init__(self):
    
        return
    
    
    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_idle(parameters.drivetrain_id))
    
    def _apply_native(self, id: int):
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_idle(id)
    

class SwerveDriveBrake(NativeSwerveRequest):
    """
    Sets the swerve drive module states to point inward on the robot in an "X"
    fashion, creating a natural brake which will oppose any motion.
    """

    def __init__(self):
        self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
        """
        The type of control request to use for the drive motor.
        """
        self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
        """
        The type of control request to use for the drive motor.
        """
        return
    
    def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'SwerveDriveBrake':
        """
        Modifies the drive_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_drive_request_type: Parameter to modify
        :type new_drive_request_type: SwerveModule.DriveRequestType
        :returns: this object
        :rtype: SwerveDriveBrake
        """
    
        self.drive_request_type = new_drive_request_type
        return self
    
    def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'SwerveDriveBrake':
        """
        Modifies the steer_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_steer_request_type: Parameter to modify
        :type new_steer_request_type: SwerveModule.SteerRequestType
        :returns: this object
        :rtype: SwerveDriveBrake
        """
    
        self.steer_request_type = new_steer_request_type
        return self
    
    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_swerve_drive_brake(parameters.drivetrain_id,
            self.drive_request_type.value,
            self.steer_request_type.value))
    
    def _apply_native(self, id: int):
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_swerve_drive_brake(id,
            self.drive_request_type.value,
            self.steer_request_type.value)
    

class FieldCentric(NativeSwerveRequest):
    """
    Drives the swerve drivetrain in a field-centric manner.
    
    When users use this request, they specify the direction the robot should travel
    oriented against the field, and the rate at which their robot should rotate
    about the center of the robot.
    
    An example scenario is that the robot is oriented to the east, the VelocityX is
    +5 m/s, VelocityY is 0 m/s, and RotationRate is 0.5 rad/s. In this scenario, the
    robot would drive northward at 5 m/s and turn counterclockwise at 0.5 rad/s.
    """

    def __init__(self):
        self.velocity_x: meters_per_second = 0
        """
        The velocity in the X direction, in m/s. X is defined as forward according to
        WPILib convention, so this determines how fast to travel forward.
        """
        self.velocity_y: meters_per_second = 0
        """
        The velocity in the Y direction, in m/s. Y is defined as to the left according
        to WPILib convention, so this determines how fast to travel to the left.
        """
        self.rotational_rate: radians_per_second = 0
        """
        The angular rate to rotate at, in radians per second. Angular rate is defined as
        counterclockwise positive, so this determines how fast to turn counterclockwise.
        """
        self.deadband: meters_per_second = 0
        """
        The allowable deadband of the request, in m/s.
        """
        self.rotational_deadband: radians_per_second = 0
        """
        The rotational deadband of the request, in radians per second.
        """
        self.center_of_rotation: Translation2d = Translation2d()
        """
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
        """
        self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
        """
        The type of control request to use for the drive motor.
        """
        self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
        """
        The type of control request to use for the drive motor.
        """
        self.desaturate_wheel_speeds: bool = True
        """
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
        """
        self.forward_perspective: ForwardPerspectiveValue = ForwardPerspectiveValue.OPERATOR_PERSPECTIVE
        """
        The perspective to use when determining which direction is forward.
        """
        return
    
    def with_velocity_x(self, new_velocity_x: meters_per_second) -> 'FieldCentric':
        """
        Modifies the velocity_x parameter and returns itself.
    
        The velocity in the X direction, in m/s. X is defined as forward according to
        WPILib convention, so this determines how fast to travel forward.
    
        :param new_velocity_x: Parameter to modify
        :type new_velocity_x: meters_per_second
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.velocity_x = new_velocity_x
        return self
    
    def with_velocity_y(self, new_velocity_y: meters_per_second) -> 'FieldCentric':
        """
        Modifies the velocity_y parameter and returns itself.
    
        The velocity in the Y direction, in m/s. Y is defined as to the left according
        to WPILib convention, so this determines how fast to travel to the left.
    
        :param new_velocity_y: Parameter to modify
        :type new_velocity_y: meters_per_second
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.velocity_y = new_velocity_y
        return self
    
    def with_rotational_rate(self, new_rotational_rate: radians_per_second) -> 'FieldCentric':
        """
        Modifies the rotational_rate parameter and returns itself.
    
        The angular rate to rotate at, in radians per second. Angular rate is defined as
        counterclockwise positive, so this determines how fast to turn counterclockwise.
    
        :param new_rotational_rate: Parameter to modify
        :type new_rotational_rate: radians_per_second
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.rotational_rate = new_rotational_rate
        return self
    
    def with_deadband(self, new_deadband: meters_per_second) -> 'FieldCentric':
        """
        Modifies the deadband parameter and returns itself.
    
        The allowable deadband of the request, in m/s.
    
        :param new_deadband: Parameter to modify
        :type new_deadband: meters_per_second
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.deadband = new_deadband
        return self
    
    def with_rotational_deadband(self, new_rotational_deadband: radians_per_second) -> 'FieldCentric':
        """
        Modifies the rotational_deadband parameter and returns itself.
    
        The rotational deadband of the request, in radians per second.
    
        :param new_rotational_deadband: Parameter to modify
        :type new_rotational_deadband: radians_per_second
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.rotational_deadband = new_rotational_deadband
        return self
    
    def with_center_of_rotation(self, new_center_of_rotation: Translation2d) -> 'FieldCentric':
        """
        Modifies the center_of_rotation parameter and returns itself.
    
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
    
        :param new_center_of_rotation: Parameter to modify
        :type new_center_of_rotation: Translation2d
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.center_of_rotation = new_center_of_rotation
        return self
    
    def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'FieldCentric':
        """
        Modifies the drive_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_drive_request_type: Parameter to modify
        :type new_drive_request_type: SwerveModule.DriveRequestType
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.drive_request_type = new_drive_request_type
        return self
    
    def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'FieldCentric':
        """
        Modifies the steer_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_steer_request_type: Parameter to modify
        :type new_steer_request_type: SwerveModule.SteerRequestType
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.steer_request_type = new_steer_request_type
        return self
    
    def with_desaturate_wheel_speeds(self, new_desaturate_wheel_speeds: bool) -> 'FieldCentric':
        """
        Modifies the desaturate_wheel_speeds parameter and returns itself.
    
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
    
        :param new_desaturate_wheel_speeds: Parameter to modify
        :type new_desaturate_wheel_speeds: bool
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.desaturate_wheel_speeds = new_desaturate_wheel_speeds
        return self
    
    def with_forward_perspective(self, new_forward_perspective: ForwardPerspectiveValue) -> 'FieldCentric':
        """
        Modifies the forward_perspective parameter and returns itself.
    
        The perspective to use when determining which direction is forward.
    
        :param new_forward_perspective: Parameter to modify
        :type new_forward_perspective: ForwardPerspectiveValue
        :returns: this object
        :rtype: FieldCentric
        """
    
        self.forward_perspective = new_forward_perspective
        return self
    
    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_field_centric(parameters.drivetrain_id,
            self.velocity_x,
            self.velocity_y,
            self.rotational_rate,
            self.deadband,
            self.rotational_deadband,
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds,
            self.forward_perspective.value))
    
    def _apply_native(self, id: int):
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_field_centric(id,
            self.velocity_x,
            self.velocity_y,
            self.rotational_rate,
            self.deadband,
            self.rotational_deadband,
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds,
            self.forward_perspective.value)
    

class RobotCentric(NativeSwerveRequest):
    """
    Drives the swerve drivetrain in a robot-centric manner.
    
    When users use this request, they specify the direction the robot should travel
    oriented against the robot itself, and the rate at which their robot should
    rotate about the center of the robot.
    
    An example scenario is that the robot is oriented to the east, the VelocityX is
    +5 m/s, VelocityY is 0 m/s, and RotationRate is 0.5 rad/s. In this scenario, the
    robot would drive eastward at 5 m/s and turn counterclockwise at 0.5 rad/s.
    """

    def __init__(self):
        self.velocity_x: meters_per_second = 0
        """
        The velocity in the X direction, in m/s. X is defined as forward according to
        WPILib convention, so this determines how fast to travel forward.
        """
        self.velocity_y: meters_per_second = 0
        """
        The velocity in the Y direction, in m/s. Y is defined as to the left according
        to WPILib convention, so this determines how fast to travel to the left.
        """
        self.rotational_rate: radians_per_second = 0
        """
        The angular rate to rotate at, in radians per second. Angular rate is defined as
        counterclockwise positive, so this determines how fast to turn counterclockwise.
        """
        self.deadband: meters_per_second = 0
        """
        The allowable deadband of the request, in m/s.
        """
        self.rotational_deadband: radians_per_second = 0
        """
        The rotational deadband of the request, in radians per second.
        """
        self.center_of_rotation: Translation2d = Translation2d()
        """
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
        """
        self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
        """
        The type of control request to use for the drive motor.
        """
        self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
        """
        The type of control request to use for the drive motor.
        """
        self.desaturate_wheel_speeds: bool = True
        """
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
        """
        return
    
    def with_velocity_x(self, new_velocity_x: meters_per_second) -> 'RobotCentric':
        """
        Modifies the velocity_x parameter and returns itself.
    
        The velocity in the X direction, in m/s. X is defined as forward according to
        WPILib convention, so this determines how fast to travel forward.
    
        :param new_velocity_x: Parameter to modify
        :type new_velocity_x: meters_per_second
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.velocity_x = new_velocity_x
        return self
    
    def with_velocity_y(self, new_velocity_y: meters_per_second) -> 'RobotCentric':
        """
        Modifies the velocity_y parameter and returns itself.
    
        The velocity in the Y direction, in m/s. Y is defined as to the left according
        to WPILib convention, so this determines how fast to travel to the left.
    
        :param new_velocity_y: Parameter to modify
        :type new_velocity_y: meters_per_second
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.velocity_y = new_velocity_y
        return self
    
    def with_rotational_rate(self, new_rotational_rate: radians_per_second) -> 'RobotCentric':
        """
        Modifies the rotational_rate parameter and returns itself.
    
        The angular rate to rotate at, in radians per second. Angular rate is defined as
        counterclockwise positive, so this determines how fast to turn counterclockwise.
    
        :param new_rotational_rate: Parameter to modify
        :type new_rotational_rate: radians_per_second
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.rotational_rate = new_rotational_rate
        return self
    
    def with_deadband(self, new_deadband: meters_per_second) -> 'RobotCentric':
        """
        Modifies the deadband parameter and returns itself.
    
        The allowable deadband of the request, in m/s.
    
        :param new_deadband: Parameter to modify
        :type new_deadband: meters_per_second
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.deadband = new_deadband
        return self
    
    def with_rotational_deadband(self, new_rotational_deadband: radians_per_second) -> 'RobotCentric':
        """
        Modifies the rotational_deadband parameter and returns itself.
    
        The rotational deadband of the request, in radians per second.
    
        :param new_rotational_deadband: Parameter to modify
        :type new_rotational_deadband: radians_per_second
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.rotational_deadband = new_rotational_deadband
        return self
    
    def with_center_of_rotation(self, new_center_of_rotation: Translation2d) -> 'RobotCentric':
        """
        Modifies the center_of_rotation parameter and returns itself.
    
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
    
        :param new_center_of_rotation: Parameter to modify
        :type new_center_of_rotation: Translation2d
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.center_of_rotation = new_center_of_rotation
        return self
    
    def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'RobotCentric':
        """
        Modifies the drive_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_drive_request_type: Parameter to modify
        :type new_drive_request_type: SwerveModule.DriveRequestType
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.drive_request_type = new_drive_request_type
        return self
    
    def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'RobotCentric':
        """
        Modifies the steer_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_steer_request_type: Parameter to modify
        :type new_steer_request_type: SwerveModule.SteerRequestType
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.steer_request_type = new_steer_request_type
        return self
    
    def with_desaturate_wheel_speeds(self, new_desaturate_wheel_speeds: bool) -> 'RobotCentric':
        """
        Modifies the desaturate_wheel_speeds parameter and returns itself.
    
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
    
        :param new_desaturate_wheel_speeds: Parameter to modify
        :type new_desaturate_wheel_speeds: bool
        :returns: this object
        :rtype: RobotCentric
        """
    
        self.desaturate_wheel_speeds = new_desaturate_wheel_speeds
        return self
    
    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_robot_centric(parameters.drivetrain_id,
            self.velocity_x,
            self.velocity_y,
            self.rotational_rate,
            self.deadband,
            self.rotational_deadband,
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds))
    
    def _apply_native(self, id: int):
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_robot_centric(id,
            self.velocity_x,
            self.velocity_y,
            self.rotational_rate,
            self.deadband,
            self.rotational_deadband,
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds)
    

class PointWheelsAt(NativeSwerveRequest):
    """
    Sets the swerve drive modules to point to a specified direction.
    """

    def __init__(self):
        self.module_direction: Rotation2d = Rotation2d()
        """
        The direction to point the modules toward. This direction is still optimized to
        what the module was previously at.
        """
        self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
        """
        The type of control request to use for the drive motor.
        """
        self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
        """
        The type of control request to use for the drive motor.
        """
        return
    
    def with_module_direction(self, new_module_direction: Rotation2d) -> 'PointWheelsAt':
        """
        Modifies the module_direction parameter and returns itself.
    
        The direction to point the modules toward. This direction is still optimized to
        what the module was previously at.
    
        :param new_module_direction: Parameter to modify
        :type new_module_direction: Rotation2d
        :returns: this object
        :rtype: PointWheelsAt
        """
    
        self.module_direction = new_module_direction
        return self
    
    def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'PointWheelsAt':
        """
        Modifies the drive_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_drive_request_type: Parameter to modify
        :type new_drive_request_type: SwerveModule.DriveRequestType
        :returns: this object
        :rtype: PointWheelsAt
        """
    
        self.drive_request_type = new_drive_request_type
        return self
    
    def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'PointWheelsAt':
        """
        Modifies the steer_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_steer_request_type: Parameter to modify
        :type new_steer_request_type: SwerveModule.SteerRequestType
        :returns: this object
        :rtype: PointWheelsAt
        """
    
        self.steer_request_type = new_steer_request_type
        return self
    
    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_point_wheels_at(parameters.drivetrain_id,
            self.module_direction.radians(),
            self.drive_request_type.value,
            self.steer_request_type.value))
    
    def _apply_native(self, id: int):
        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_point_wheels_at(id,
            self.module_direction.radians(),
            self.drive_request_type.value,
            self.steer_request_type.value)
    

class ApplyRobotSpeeds(NativeSwerveRequest):
    """
    Accepts a generic robot-centric ChassisSpeeds to apply to the drivetrain.
    """

    def __init__(self):
        self.speeds: ChassisSpeeds = ChassisSpeeds()
        """
        The robot-centric chassis speeds to apply to the drivetrain.
        """
        self.wheel_force_feedforwards_x: list[newton] = []
        """
        Robot-centric wheel force feedforwards to apply in the X direction, in newtons.
        X is defined as forward according to WPILib convention, so this determines the
        forward forces to apply.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
        """
        self.wheel_force_feedforwards_y: list[newton] = []
        """
        Robot-centric wheel force feedforwards to apply in the Y direction, in newtons.
        Y is defined as to the left according to WPILib convention, so this determines
        the forces to apply to the left.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
        """
        self.center_of_rotation: Translation2d = Translation2d()
        """
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
        """
        self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
        """
        The type of control request to use for the drive motor.
        """
        self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
        """
        The type of control request to use for the drive motor.
        """
        self.desaturate_wheel_speeds: bool = True
        """
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
        """
        return

    def with_speeds(self, new_speeds: ChassisSpeeds) -> 'ApplyRobotSpeeds':
        """
        Modifies the speeds parameter and returns itself.
    
        The robot-centric chassis speeds to apply to the drivetrain.
    
        :param new_speeds: Parameter to modify
        :type new_speeds: ChassisSpeeds
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.speeds = new_speeds
        return self
    
    def with_wheel_force_feedforwards_x(self, new_wheel_force_feedforwards_x: list[newton]) -> 'ApplyRobotSpeeds':
        """
        Modifies the wheel_force_feedforwards_x parameter and returns itself.
    
        Robot-centric wheel force feedforwards to apply in the X direction, in newtons.
        X is defined as forward according to WPILib convention, so this determines the
        forward forces to apply.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
    
        :param new_wheel_force_feedforwards_x: Parameter to modify
        :type new_wheel_force_feedforwards_x: list[newton]
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.wheel_force_feedforwards_x = new_wheel_force_feedforwards_x
        return self
    
    def with_wheel_force_feedforwards_y(self, new_wheel_force_feedforwards_y: list[newton]) -> 'ApplyRobotSpeeds':
        """
        Modifies the wheel_force_feedforwards_y parameter and returns itself.
    
        Robot-centric wheel force feedforwards to apply in the Y direction, in newtons.
        Y is defined as to the left according to WPILib convention, so this determines
        the forces to apply to the left.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
    
        :param new_wheel_force_feedforwards_y: Parameter to modify
        :type new_wheel_force_feedforwards_y: list[newton]
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.wheel_force_feedforwards_y = new_wheel_force_feedforwards_y
        return self
    
    def with_center_of_rotation(self, new_center_of_rotation: Translation2d) -> 'ApplyRobotSpeeds':
        """
        Modifies the center_of_rotation parameter and returns itself.
    
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
    
        :param new_center_of_rotation: Parameter to modify
        :type new_center_of_rotation: Translation2d
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.center_of_rotation = new_center_of_rotation
        return self
    
    def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'ApplyRobotSpeeds':
        """
        Modifies the drive_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_drive_request_type: Parameter to modify
        :type new_drive_request_type: SwerveModule.DriveRequestType
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.drive_request_type = new_drive_request_type
        return self
    
    def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'ApplyRobotSpeeds':
        """
        Modifies the steer_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_steer_request_type: Parameter to modify
        :type new_steer_request_type: SwerveModule.SteerRequestType
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.steer_request_type = new_steer_request_type
        return self
    
    def with_desaturate_wheel_speeds(self, new_desaturate_wheel_speeds: bool) -> 'ApplyRobotSpeeds':
        """
        Modifies the desaturate_wheel_speeds parameter and returns itself.
    
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
    
        :param new_desaturate_wheel_speeds: Parameter to modify
        :type new_desaturate_wheel_speeds: bool
        :returns: this object
        :rtype: ApplyRobotSpeeds
        """
    
        self.desaturate_wheel_speeds = new_desaturate_wheel_speeds
        return self

    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        c_wheel_force_feedforwards_x = (ctypes.c_double * len(self.wheel_force_feedforwards_x))()
        for (i, wheel_force_feedforward_x) in enumerate(self.wheel_force_feedforwards_x):
            c_wheel_force_feedforwards_x[i] = wheel_force_feedforward_x

        c_wheel_force_feedforwards_y = (ctypes.c_double * len(self.wheel_force_feedforwards_y))()
        for (i, wheel_force_feedforward_y) in enumerate(self.wheel_force_feedforwards_y):
            c_wheel_force_feedforwards_y[i] = wheel_force_feedforward_y

        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_apply_robot_speeds(parameters.drivetrain_id,
            self.speeds.vx,
            self.speeds.vy,
            self.speeds.omega,
            c_wheel_force_feedforwards_x,
            len(self.wheel_force_feedforwards_x),
            c_wheel_force_feedforwards_y,
            len(self.wheel_force_feedforwards_y),
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds))
    
    def _apply_native(self, id: int):
        c_wheel_force_feedforwards_x = (ctypes.c_double * len(self.wheel_force_feedforwards_x))()
        for (i, wheel_force_feedforward_x) in enumerate(self.wheel_force_feedforwards_x):
            c_wheel_force_feedforwards_x[i] = wheel_force_feedforward_x

        c_wheel_force_feedforwards_y = (ctypes.c_double * len(self.wheel_force_feedforwards_y))()
        for (i, wheel_force_feedforward_y) in enumerate(self.wheel_force_feedforwards_y):
            c_wheel_force_feedforwards_y[i] = wheel_force_feedforward_y

        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_apply_robot_speeds(id,
            self.speeds.vx,
            self.speeds.vy,
            self.speeds.omega,
            c_wheel_force_feedforwards_x,
            len(self.wheel_force_feedforwards_x),
            c_wheel_force_feedforwards_y,
            len(self.wheel_force_feedforwards_y),
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds)


class ApplyFieldSpeeds(NativeSwerveRequest):
    """
    Accepts a generic field-centric ChassisSpeeds to apply to the drivetrain.
    """

    def __init__(self):
        self.speeds: ChassisSpeeds = ChassisSpeeds()
        """
        The field-centric chassis speeds to apply to the drivetrain.
        """
        self.wheel_force_feedforwards_x: list[newton] = []
        """
        Field-centric wheel force feedforwards to apply in the X direction, in newtons.
        X is defined as forward according to WPILib convention, so this determines the
        forward forces to apply.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
        """
        self.wheel_force_feedforwards_y: list[newton] = []
        """
        Field-centric wheel force feedforwards to apply in the Y direction, in newtons.
        Y is defined as to the left according to WPILib convention, so this determines
        the forces to apply to the left.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
        """
        self.center_of_rotation: Translation2d = Translation2d()
        """
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
        """
        self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
        """
        The type of control request to use for the drive motor.
        """
        self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
        """
        The type of control request to use for the drive motor.
        """
        self.desaturate_wheel_speeds: bool = True
        """
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
        """
        self.forward_perspective: ForwardPerspectiveValue = ForwardPerspectiveValue.BLUE_ALLIANCE
        """
        The perspective to use when determining which direction is forward.
        """
        return

    def with_speeds(self, new_speeds: ChassisSpeeds) -> 'ApplyFieldSpeeds':
        """
        Modifies the speeds parameter and returns itself.
    
        The field-centric chassis speeds to apply to the drivetrain.
    
        :param new_speeds: Parameter to modify
        :type new_speeds: ChassisSpeeds
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.speeds = new_speeds
        return self
    
    def with_wheel_force_feedforwards_x(self, new_wheel_force_feedforwards_x: list[newton]) -> 'ApplyFieldSpeeds':
        """
        Modifies the wheel_force_feedforwards_x parameter and returns itself.
    
        Field-centric wheel force feedforwards to apply in the X direction, in newtons.
        X is defined as forward according to WPILib convention, so this determines the
        forward forces to apply.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
    
        :param new_wheel_force_feedforwards_x: Parameter to modify
        :type new_wheel_force_feedforwards_x: list[newton]
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.wheel_force_feedforwards_x = new_wheel_force_feedforwards_x
        return self
    
    def with_wheel_force_feedforwards_y(self, new_wheel_force_feedforwards_y: list[newton]) -> 'ApplyFieldSpeeds':
        """
        Modifies the wheel_force_feedforwards_y parameter and returns itself.
    
        Field-centric wheel force feedforwards to apply in the Y direction, in newtons.
        Y is defined as to the left according to WPILib convention, so this determines
        the forces to apply to the left.
        
        These forces should include friction applied to the ground.
        
        The order of the forces should match the order of the modules returned from
        SwerveDrivetrain.
    
        :param new_wheel_force_feedforwards_y: Parameter to modify
        :type new_wheel_force_feedforwards_y: list[newton]
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.wheel_force_feedforwards_y = new_wheel_force_feedforwards_y
        return self
    
    def with_center_of_rotation(self, new_center_of_rotation: Translation2d) -> 'ApplyFieldSpeeds':
        """
        Modifies the center_of_rotation parameter and returns itself.
    
        The center of rotation the robot should rotate around. This is (0,0) by default,
        which will rotate around the center of the robot.
    
        :param new_center_of_rotation: Parameter to modify
        :type new_center_of_rotation: Translation2d
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.center_of_rotation = new_center_of_rotation
        return self
    
    def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'ApplyFieldSpeeds':
        """
        Modifies the drive_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_drive_request_type: Parameter to modify
        :type new_drive_request_type: SwerveModule.DriveRequestType
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.drive_request_type = new_drive_request_type
        return self
    
    def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'ApplyFieldSpeeds':
        """
        Modifies the steer_request_type parameter and returns itself.
    
        The type of control request to use for the drive motor.
    
        :param new_steer_request_type: Parameter to modify
        :type new_steer_request_type: SwerveModule.SteerRequestType
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.steer_request_type = new_steer_request_type
        return self
    
    def with_desaturate_wheel_speeds(self, new_desaturate_wheel_speeds: bool) -> 'ApplyFieldSpeeds':
        """
        Modifies the desaturate_wheel_speeds parameter and returns itself.
    
        Whether to desaturate wheel speeds before applying. For more information, see
        the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
    
        :param new_desaturate_wheel_speeds: Parameter to modify
        :type new_desaturate_wheel_speeds: bool
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.desaturate_wheel_speeds = new_desaturate_wheel_speeds
        return self
    
    def with_forward_perspective(self, new_forward_perspective: ForwardPerspectiveValue) -> 'ApplyFieldSpeeds':
        """
        Modifies the forward_perspective parameter and returns itself.
    
        The perspective to use when determining which direction is forward.
    
        :param new_forward_perspective: Parameter to modify
        :type new_forward_perspective: ForwardPerspectiveValue
        :returns: this object
        :rtype: ApplyFieldSpeeds
        """
    
        self.forward_perspective = new_forward_perspective
        return self

    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        c_wheel_force_feedforwards_x = (ctypes.c_double * len(self.wheel_force_feedforwards_x))()
        for (i, wheel_force_feedforward_x) in enumerate(self.wheel_force_feedforwards_x):
            c_wheel_force_feedforwards_x[i] = wheel_force_feedforward_x

        c_wheel_force_feedforwards_y = (ctypes.c_double * len(self.wheel_force_feedforwards_y))()
        for (i, wheel_force_feedforward_y) in enumerate(self.wheel_force_feedforwards_y):
            c_wheel_force_feedforwards_y[i] = wheel_force_feedforward_y

        return StatusCode(Native.api_instance().c_ctre_phoenix6_swerve_request_apply_apply_field_speeds(parameters.drivetrain_id,
            self.speeds.vx,
            self.speeds.vy,
            self.speeds.omega,
            c_wheel_force_feedforwards_x,
            len(self.wheel_force_feedforwards_x),
            c_wheel_force_feedforwards_y,
            len(self.wheel_force_feedforwards_y),
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds,
            self.forward_perspective.value))
    
    def _apply_native(self, id: int):
        c_wheel_force_feedforwards_x = (ctypes.c_double * len(self.wheel_force_feedforwards_x))()
        for (i, wheel_force_feedforward_x) in enumerate(self.wheel_force_feedforwards_x):
            c_wheel_force_feedforwards_x[i] = wheel_force_feedforward_x

        c_wheel_force_feedforwards_y = (ctypes.c_double * len(self.wheel_force_feedforwards_y))()
        for (i, wheel_force_feedforward_y) in enumerate(self.wheel_force_feedforwards_y):
            c_wheel_force_feedforwards_y[i] = wheel_force_feedforward_y

        Native.api_instance().c_ctre_phoenix6_swerve_drivetrain_set_control_apply_field_speeds(id,
            self.speeds.vx,
            self.speeds.vy,
            self.speeds.omega,
            c_wheel_force_feedforwards_x,
            len(self.wheel_force_feedforwards_x),
            c_wheel_force_feedforwards_y,
            len(self.wheel_force_feedforwards_y),
            self.center_of_rotation.X(),
            self.center_of_rotation.Y(),
            self.drive_request_type.value,
            self.steer_request_type.value,
            self.desaturate_wheel_speeds,
            self.forward_perspective.value)


if USE_WPILIB:
    class FieldCentricFacingAngle(SwerveRequest):
        """
        Drives the swerve drivetrain in a field-centric manner, maintaining a
        specified heading angle to ensure the robot is facing the desired direction

        When users use this request, they specify the direction the robot should
        travel oriented against the field, and the direction the robot should be facing.

        An example scenario is that the robot is oriented to the east, the VelocityX
        is +5 m/s, VelocityY is 0 m/s, and TargetDirection is 180 degrees.
        In this scenario, the robot would drive northward at 5 m/s and turn clockwise
        to a target of 180 degrees.

        This control request is especially useful for autonomous control, where the
        robot should be facing a changing direction throughout the motion.
        """

        def __init__(self):
            self.velocity_x: meters_per_second = 0
            """
            The velocity in the X direction, in m/s. X is defined as forward according to
            WPILib convention, so this determines how fast to travel forward.
            """
            self.velocity_y: meters_per_second = 0
            """
            The velocity in the Y direction, in m/s. Y is defined as to the left according
            to WPILib convention, so this determines how fast to travel to the left.
            """
            self.target_direction: Rotation2d = Rotation2d()
            """
            The desired direction to face.
            0 Degrees is defined as in the direction of the X axis.
            As a result, a TargetDirection of 90 degrees will point along
            the Y axis, or to the left.
            """
            self.target_rate_feedforward: radians_per_second = 0
            """
            The rotational rate feedforward to add to the output of the heading
            controller, in radians per second. When using a motion profile for the
            target direction, this can be set to the current velocity reference of
            the profile.
            """
            self.deadband: meters_per_second = 0
            """
            The allowable deadband of the request, in m/s.
            """
            self.rotational_deadband: radians_per_second = 0
            """
            The rotational deadband of the request, in radians per second.
            """
            self.center_of_rotation: Translation2d = Translation2d()
            """
            The center of rotation the robot should rotate around. This is (0,0) by default,
            which will rotate around the center of the robot.
            """
            self.drive_request_type: SwerveModule.DriveRequestType = SwerveModule.DriveRequestType.OPEN_LOOP_VOLTAGE
            """
            The type of control request to use for the drive motor.
            """
            self.steer_request_type: SwerveModule.SteerRequestType = SwerveModule.SteerRequestType.POSITION
            """
            The type of control request to use for the drive motor.
            """
            self.desaturate_wheel_speeds: bool = True
            """
            Whether to desaturate wheel speeds before applying. For more information, see
            the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.
            """
            self.forward_perspective: ForwardPerspectiveValue = ForwardPerspectiveValue.OPERATOR_PERSPECTIVE
            """
            The perspective to use when determining which direction is forward.
            """
            self.heading_controller: PhoenixPIDController = PhoenixPIDController(0.0, 0.0, 0.0)
            """
            The PID controller used to maintain the desired heading.
            Users can specify the PID gains to change how aggressively to maintain
            heading.

            This PID controller operates on heading radians and outputs a target
            rotational rate in radians per second. Note that continuous input should
            be enabled on the range [-pi, pi].
            """

            self.__field_centric = FieldCentric()

            self.heading_controller.enableContinuousInput(-math.pi, math.pi)

        def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
            angle_to_face = self.target_direction
            if self.forward_perspective is ForwardPerspectiveValue.OPERATOR_PERSPECTIVE:
                # If we're operator perspective, rotate the direction we want to face by the angle
                angle_to_face = angle_to_face.rotateBy(parameters.operator_forward_direction)

            to_apply_omega = self.target_rate_feedforward + self.heading_controller.calculate(
                parameters.current_pose.rotation().radians(),
                angle_to_face.radians(),
                parameters.timestamp
            )

            return (
                self.__field_centric
                .with_velocity_x(self.velocity_x)
                .with_velocity_y(self.velocity_y)
                .with_rotational_rate(to_apply_omega)
                .with_deadband(self.deadband)
                .with_rotational_deadband(self.rotational_deadband)
                .with_center_of_rotation(self.center_of_rotation)
                .with_drive_request_type(self.drive_request_type)
                .with_steer_request_type(self.steer_request_type)
                .with_desaturate_wheel_speeds(self.desaturate_wheel_speeds)
                .with_forward_perspective(self.forward_perspective)
                .apply(parameters, modules_to_apply)
            )

        def with_velocity_x(self, new_velocity_x: meters_per_second) -> 'FieldCentricFacingAngle':
            """
            Modifies the velocity_x parameter and returns itself.

            The velocity in the X direction, in m/s. X is defined as forward according to
            WPILib convention, so this determines how fast to travel forward.

            :param new_velocity_x: Parameter to modify
            :type new_velocity_x: meters_per_second
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.velocity_x = new_velocity_x
            return self

        def with_velocity_y(self, new_velocity_y: meters_per_second) -> 'FieldCentricFacingAngle':
            """
            Modifies the velocity_y parameter and returns itself.

            The velocity in the Y direction, in m/s. Y is defined as to the left according
            to WPILib convention, so this determines how fast to travel to the left.

            :param new_velocity_y: Parameter to modify
            :type new_velocity_y: meters_per_second
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.velocity_y = new_velocity_y
            return self

        def with_target_direction(self, new_target_direction: Rotation2d) -> 'FieldCentricFacingAngle':
            """
            Modifies the target_direction parameter and returns itself.

            The desired direction to face.
            0 Degrees is defined as in the direction of the X axis.
            As a result, a TargetDirection of 90 degrees will point along
            the Y axis, or to the left.

            :param new_target_direction: Parameter to modify
            :type new_target_direction: Rotation2d
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.target_direction = new_target_direction
            return self

        def with_target_rate_feedforward(self, new_target_rate_feedforward: radians_per_second) -> 'FieldCentricFacingAngle':
            """
            Modifies the target_rate_feedforward parameter and returns itself.

            The rotational rate feedforward to add to the output of the heading
            controller, in radians per second. When using a motion profile for the
            target direction, this can be set to the current velocity reference of
            the profile.

            :param new_target_rate_feedforward: Parameter to modify
            :type new_target_rate_feedforward: radians_per_second
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.target_rate_feedforward = new_target_rate_feedforward
            return self

        def with_deadband(self, new_deadband: meters_per_second) -> 'FieldCentricFacingAngle':
            """
            Modifies the deadband parameter and returns itself.

            The allowable deadband of the request, in m/s.

            :param new_deadband: Parameter to modify
            :type new_deadband: meters_per_second
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.deadband = new_deadband
            return self

        def with_rotational_deadband(self, new_rotational_deadband: radians_per_second) -> 'FieldCentricFacingAngle':
            """
            Modifies the rotational_deadband parameter and returns itself.

            The rotational deadband of the request, in radians per second.

            :param new_rotational_deadband: Parameter to modify
            :type new_rotational_deadband: radians_per_second
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.rotational_deadband = new_rotational_deadband
            return self

        def with_center_of_rotation(self, new_center_of_rotation: Translation2d) -> 'FieldCentricFacingAngle':
            """
            Modifies the center_of_rotation parameter and returns itself.

            The center of rotation the robot should rotate around. This is (0,0) by default,
            which will rotate around the center of the robot.

            :param new_center_of_rotation: Parameter to modify
            :type new_center_of_rotation: Translation2d
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.center_of_rotation = new_center_of_rotation
            return self

        def with_drive_request_type(self, new_drive_request_type: SwerveModule.DriveRequestType) -> 'FieldCentricFacingAngle':
            """
            Modifies the drive_request_type parameter and returns itself.

            The type of control request to use for the drive motor.

            :param new_drive_request_type: Parameter to modify
            :type new_drive_request_type: SwerveModule.DriveRequestType
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.drive_request_type = new_drive_request_type
            return self

        def with_steer_request_type(self, new_steer_request_type: SwerveModule.SteerRequestType) -> 'FieldCentricFacingAngle':
            """
            Modifies the steer_request_type parameter and returns itself.

            The type of control request to use for the drive motor.

            :param new_steer_request_type: Parameter to modify
            :type new_steer_request_type: SwerveModule.SteerRequestType
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.steer_request_type = new_steer_request_type
            return self

        def with_desaturate_wheel_speeds(self, new_desaturate_wheel_speeds: bool) -> 'FieldCentricFacingAngle':
            """
            Modifies the desaturate_wheel_speeds parameter and returns itself.

            Whether to desaturate wheel speeds before applying. For more information, see
            the documentation of SwerveDriveKinematics.desaturateWheelSpeeds.

            :param new_desaturate_wheel_speeds: Parameter to modify
            :type new_desaturate_wheel_speeds: bool
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.desaturate_wheel_speeds = new_desaturate_wheel_speeds
            return self

        def with_forward_perspective(self, new_forward_perspective: ForwardPerspectiveValue) -> 'FieldCentricFacingAngle':
            """
            Modifies the forward_perspective parameter and returns itself.

            The perspective to use when determining which direction is forward.

            :param new_forward_perspective: Parameter to modify
            :type new_forward_perspective: ForwardPerspectiveValue
            :returns: this object
            :rtype: FieldCentricFacingAngle
            """

            self.forward_perspective = new_forward_perspective
            return self

class SysIdSwerveTranslation(SwerveRequest):
    """
    SysId-specific SwerveRequest to characterize the translational
    characteristics of a swerve drivetrain.
    """

    def __init__(self):
        self.volts_to_apply: volt = 0.0
        """
        Voltage to apply to drive wheels.
        """

        self.__drive_request = VoltageOut(0)
        """Local reference to a voltage request for the drive motors"""
        self.__steer_request_voltage = PositionVoltage(0)
        """Local reference to a position voltage request for the steer motors"""
        self.__steer_request_torque_current = PositionTorqueCurrentFOC(0)
        """Local reference to a position torque current request for the steer motors"""

    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        for module in modules_to_apply:
            if module.steer_closed_loop_output_type == ClosedLoopOutputType.TORQUE_CURRENT_FOC:
                module.apply(
                    self.__drive_request.with_output(self.volts_to_apply),
                    self.__steer_request_torque_current.with_position(0)
                )
            else:
                module.apply(
                    self.__drive_request.with_output(self.volts_to_apply),
                    self.__steer_request_voltage.with_position(0)
                )
        return StatusCode.OK

    def with_volts(self, volts: volt) -> 'SysIdSwerveTranslation':
        """
        Sets the voltage to apply to the drive wheels.

        :param volts: Voltage to apply
        :type volts: volt
        :returns: this request
        :rtype: SysIdSwerveTranslation
        """
        self.volts_to_apply = volts
        return self

class SysIdSwerveRotation(SwerveRequest):
    """
    SysId-specific SwerveRequest to characterize the rotational
    characteristics of a swerve drivetrain. This is useful to
    characterize the heading controller for FieldCentricFacingAngle.

    The RotationalRate of this swerve request should be logged.
    When importing the log to SysId, set the "voltage" to
    RotationalRate, "position" to the Pigeon 2 Yaw, and "velocity"
    to the Pigeon 2 AngularVelocityZWorld. Note that the position
    and velocity will both need to be scaled by pi/180.

    Alternatively, the MotorVoltage of one of the drive motors can
    be loaded into the SysId "voltage" field, which can be useful
    when determining the MOI of the robot.
    """

    def __init__(self):
        self.rotational_rate: radians_per_second = 0.0
        """
        The angular rate to rotate at, in radians per second.
        """

        self.__drive_request = VoltageOut(0)
        """Local reference to a voltage request for the drive motors"""
        self.__steer_request_voltage = PositionVoltage(0)
        """Local reference to a position voltage request for the steer motors"""
        self.__steer_request_torque_current = PositionTorqueCurrentFOC(0)
        """Local reference to a position torque current request for the steer motors"""

    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        for i, module in enumerate(modules_to_apply):
            speed = self.rotational_rate * parameters.module_locations[i].norm()
            drive_voltage = speed / parameters.max_speed * 12.0

            angle = parameters.module_locations[i].angle() + Rotation2d.fromDegrees(90)

            if module.steer_closed_loop_output_type == ClosedLoopOutputType.TORQUE_CURRENT_FOC:
                module.apply(
                    self.__drive_request.with_output(drive_voltage),
                    self.__steer_request_torque_current.with_position(angle.radians() / (2 * math.pi))
                )
            else:
                module.apply(
                    self.__drive_request.with_output(drive_voltage),
                    self.__steer_request_voltage.with_position(angle.radians() / (2 * math.pi))
                )
        return StatusCode.OK

    def with_rotational_rate(self, rotational_rate: radians_per_second) -> 'SysIdSwerveRotation':
        """
        Sets the angular rate to rotate at, in radians per second.

        :param rotational_rate: Angular rate to rotate at
        :type rotational_rate: radians_per_second
        :returns: this request
        :rtype: SysIdSwerveRotation
        """

        self.rotational_rate = rotational_rate
        return self

class SysIdSwerveSteerGains(SwerveRequest):
    """
    SysId-specific SwerveRequest to characterize the steer module
    characteristics of a swerve drivetrain.
    """

    def __init__(self):
        self.volts_to_apply: volt = 0.0
        """
        Voltage to apply to steer wheels.
        """

        self.__drive_request = CoastOut()
        """Local reference to a coast request for the drive motors"""
        self.__steer_request = VoltageOut(0)
        """Local reference to a voltage request for the steer motors"""

    def apply(self, parameters: 'SwerveControlParameters', modules_to_apply: list[SwerveModule]) -> StatusCode:
        for module in modules_to_apply:
            module.apply(
                self.__drive_request,
                self.__steer_request.with_output(self.volts_to_apply)
            )
        return StatusCode.OK

    def with_volts(self, volts: volt) -> 'SysIdSwerveSteerGains':
        """
        Sets the voltage to apply to the steer wheels.

        :param volts: Voltage to apply
        :type volts: volt
        :returns: this request
        :rtype: SysIdSwerveSteerGains
        """
        self.volts_to_apply = volts
        return self
