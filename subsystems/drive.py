from phoenix6.configs import pigeon2_configs, talon_fx_configs, Slot0Configs
from phoenix6.hardware import talon_fx
import phoenix6.hardware.core.core_pigeon2 as core_pigeon2
from phoenix6.swerve import swerve_drivetrain, swerve_drivetrain_constants, swerve_module_constants, SwerveModuleConstantsFactory
from phoenix6.swerve.swerve_module_constants import ClosedLoopOutputType, SteerFeedbackType
from phoenix6.swerve.requests import ApplyFieldSpeeds, FieldCentricFacingAngle
from wpimath.kinematics import ChassisSpeeds
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from constants import *

class Drive():

    frontDist = 0
    leftDist = 0
    FLSteerOffset = 0.0
    FRSteerOffset = 0.0
    BLSteerOffset = 0.0
    BRSteerOffset = 0.0
        
    steerGains = Slot0Configs().with_k_p(50).with_k_i(0).with_k_d(0.2).with_k_s(0).with_k_v(0).with_k_a(0) #TODO: tune this

    driveGains = Slot0Configs().with_k_p(2.5).with_k_i(0).with_k_d(0).with_k_s(0).with_k_v(0).with_k_a(0) #TODO: also tune this
    drivetrainconstants = swerve_drivetrain_constants.SwerveDrivetrainConstants().with_pigeon2_id(PIGEON_ID).with_can_bus_name("rio")
    constantCreator = SwerveModuleConstantsFactory().with_drive_motor_gear_ratio(6.75).with_steer_motor_gear_ratio(150.0/7).with_wheel_radius(1.75).with_slip_current(90).with_steer_motor_gains(steerGains).with_drive_motor_gains(driveGains).with_drive_motor_closed_loop_output(ClosedLoopOutputType.TORQUE_CURRENT_FOC).with_steer_motor_closed_loop_output(ClosedLoopOutputType.VOLTAGE).with_speed_at12_volts(5).with_feedback_source(SteerFeedbackType.FUSED_CANCODER).with_coupling_gear_ratio(3.5)
    frontLeft = constantCreator.create_module_constants(
        FRONT_LEFT_STEER_ID, 
        FRONT_LEFT_DRIVE_ID, 
        FRONT_LEFT_ENCODER_ID, 
        FLSteerOffset, 
        frontDist, 
        leftDist, 
        True, 
        True, 
        False)
    frontRight = constantCreator.create_module_constants(
        FRONT_RIGHT_STEER_ID, 
        FRONT_RIGHT_DRIVE_ID, 
        FRONT_RIGHT_ENCODER_ID, 
        FRSteerOffset, 
        frontDist, 
        -leftDist, 
        True, 
        True, 
        False)
    backLeft = constantCreator.create_module_constants(
        BACK_LEFT_STEER_ID, 
        BACK_LEFT_DRIVE_ID, 
        BACK_LEFT_ENCODER_ID, 
        BLSteerOffset, 
        -frontDist, 
        leftDist, 
        True, 
        True, 
        False)
    backRight = constantCreator.create_module_constants(
        BACK_RIGHT_STEER_ID, 
        BACK_RIGHT_DRIVE_ID, 
        BACK_RIGHT_ENCODER_ID, 
        BRSteerOffset, 
        -frontDist, 
        -leftDist, 
        True, 
        True, 
        False)
    drivetrain = swerve_drivetrain.SwerveDrivetrain(talon_fx.TalonFX, talon_fx.TalonFX, core_pigeon2.CorePigeon2, drivetrainconstants, [frontLeft, frontRight, backLeft, backRight])
    applyFieldSpeedsApplier = ApplyFieldSpeeds()
    fieldCentricFacingAngleApplier = FieldCentricFacingAngle()
    def drive(demand: ChassisSpeeds):
        self.drivetrain.set_control(self.applyFieldSpeedsApplier.with_speeds(demand))