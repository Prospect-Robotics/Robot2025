"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

try:
    import math
    from typing import TypeVar
    from wpimath.kinematics import (
        SwerveDrive2Kinematics,
        SwerveDrive3Kinematics,
        SwerveDrive4Kinematics,
        SwerveDrive6Kinematics,
    )
    from wpilib.simulation import DCMotorSim
    from wpimath.system.plant import DCMotor, LinearSystemId

    from phoenix6.hardware.parent_device import ParentDevice
    from phoenix6.hardware.traits.common_talon import CommonTalon
    from phoenix6.sim.chassis_reference import ChassisReference
    from phoenix6.sim.cancoder_sim_state import CANcoderSimState
    from phoenix6.sim.candi_sim_state import CANdiSimState
    from phoenix6.sim.pigeon2_sim_state import Pigeon2SimState
    from phoenix6.sim.talon_fxs_sim_state import TalonFXSSimState
    from phoenix6.swerve.swerve_module_constants import (
        DriveMotorArrangement,
        SteerMotorArrangement,
        SwerveModuleConstants
    )
    from phoenix6.swerve.swerve_module import SwerveModule
    from phoenix6.swerve.utility.geometry import Rotation2d, Translation2d
    from phoenix6.units import kilogram_square_meter, radians_per_second, second, volt

    DriveMotorT = TypeVar("DriveMotorT", bound="CommonTalon")
    SteerMotorT = TypeVar("SteerMotorT", bound="CommonTalon")
    EncoderT = TypeVar("EncoderT", bound="ParentDevice")

    class SimSwerveDrivetrain:
        """
        Simplified swerve drive simulation class.

        This class assumes that the swerve drive is perfect, meaning
        that there is no scrub and the wheels do not slip.

        In addition, it assumes the inertia of the robot is governed only
        by the inertia of the steer module and the individual drive wheels.
        Robot-wide inertia is not accounted for, and neither is translational
        vs rotational inertia of the robot.

        These assumptions provide a simplified example that can demonstrate the
        behavior of a swerve drive in simulation. Users are encouraged to
        expand this model for their own use.
        """

        class SimSwerveModule:
            def __init__(
                self,
                drive_gearing: float, drive_inertia: kilogram_square_meter,
                drive_friction_voltage: volt, drive_motor_inverted: bool,
                drive_motor_type: DriveMotorArrangement,
                steer_gearing: float, steer_inertia: kilogram_square_meter,
                steer_friction_voltage: volt, steer_motor_inverted: bool,
                steer_motor_type: SteerMotorArrangement,
                encoder_inverted: bool,
            ):
                if drive_motor_type == DriveMotorArrangement.TALON_FXS_NEO_JST:
                    drive_gearbox = DCMotor.NEO(1)
                elif drive_motor_type == DriveMotorArrangement.TALON_FXS_VORTEX_JST:
                    drive_gearbox = DCMotor.neoVortex(1)
                else:
                    drive_gearbox = DCMotor.krakenX60FOC(1)

                if steer_motor_type == SteerMotorArrangement.TALON_FXS_MINION_JST:
                    steer_gearbox = DCMotor(12, 3.1, 202, 4, 774, 1)
                elif steer_motor_type == SteerMotorArrangement.TALON_FXS_NEO_JST:
                    steer_gearbox = DCMotor.NEO(1)
                elif steer_motor_type == SteerMotorArrangement.TALON_FXS_VORTEX_JST:
                    steer_gearbox = DCMotor.neoVortex(1)
                elif (
                    steer_motor_type == SteerMotorArrangement.TALON_FXS_BRUSHED_AB or
                    steer_motor_type == SteerMotorArrangement.TALON_FXS_BRUSHED_AC or
                    steer_motor_type == SteerMotorArrangement.TALON_FXS_BRUSHED_BC
                ):
                    steer_gearbox = DCMotor.CIM(1)
                else:
                    steer_gearbox = DCMotor.krakenX60FOC(1)

                self.drive_motor = DCMotorSim(LinearSystemId.DCMotorSystem(drive_gearbox, drive_inertia, drive_gearing), drive_gearbox)
                """Reference to motor simulation for drive motor"""
                self.steer_motor = DCMotorSim(LinearSystemId.DCMotorSystem(steer_gearbox, steer_inertia, steer_gearing), steer_gearbox)
                """Reference to motor simulation for the steer motor"""
                self.drive_gearing = drive_gearing
                """Reference to steer gearing for updating encoder"""
                self.steer_gearing = steer_gearing
                """Reference to steer gearing for updating encoder"""
                self.drive_friction_voltage = drive_friction_voltage
                """Voltage necessary for the drive motor to overcome friction"""
                self.steer_friction_voltage = steer_friction_voltage
                """Voltage necessary for the steer motor to overcome friction"""
                self.drive_motor_inverted = drive_motor_inverted
                """Whether the drive motor is inverted"""
                self.steer_motor_inverted = steer_motor_inverted
                """Whether the steer motor is inverted"""
                self.encoder_inverted = encoder_inverted
                """Whether the azimuth encoder is inverted"""

        def __init__(
            self,
            wheel_locations: list[Translation2d],
            pigeon_sim: Pigeon2SimState,
            module_constants: list[SwerveModuleConstants],
        ):
            self._pigeon_sim = pigeon_sim
            self._modules: list[SimSwerveDrivetrain.SimSwerveModule] = []
            for module in module_constants:
                self._modules.append(
                    self.SimSwerveModule(
                        module.drive_motor_gear_ratio, module.drive_inertia,
                        module.drive_friction_voltage, module.drive_motor_inverted,
                        module.drive_motor_type,
                        module.steer_motor_gear_ratio, module.steer_inertia,
                        module.steer_friction_voltage, module.steer_motor_inverted,
                        module.steer_motor_type,
                        module.encoder_inverted,
                    )
                )

            if len(wheel_locations) == 2:
                self._kinem = SwerveDrive2Kinematics(wheel_locations[0], wheel_locations[1])
            elif len(wheel_locations) == 3:
                self._kinem = SwerveDrive3Kinematics(wheel_locations[0], wheel_locations[1], wheel_locations[2])
            elif len(wheel_locations) == 4:
                self._kinem = SwerveDrive4Kinematics(wheel_locations[0], wheel_locations[1], wheel_locations[2], wheel_locations[3])
            elif len(wheel_locations) == 6:
                self._kinem = SwerveDrive6Kinematics(wheel_locations[0], wheel_locations[1], wheel_locations[2], wheel_locations[3], wheel_locations[4], wheel_locations[5])
            else:
                self._kinem = None

            self._last_angle = Rotation2d()

        def update(
            self,
            dt: second,
            supply_voltage: volt,
            modules_to_apply: list[SwerveModule[DriveMotorT, SteerMotorT, EncoderT]]
        ):
            """
            Update this simulation for the time duration.

            This performs a simulation update on all the simulated devices

            :param dt: The time delta between this update and the previous update
            :type dt: second
            :param supply_voltage: The voltage as seen at the motor controllers
            :type supply_voltage: volt
            :param modules_to_apply: What modules to apply the update to
            :type modules_to_apply: list[SwerveModule[DriveMotorT, SteerMotorT, EncoderT]]
            """
            if self._kinem is None:
                return
            elif len(modules_to_apply) != len(self._modules):
                return

            for sim_module, module_to_apply in zip(self._modules, modules_to_apply):
                drive_motor = module_to_apply.drive_motor.sim_state
                steer_motor = module_to_apply.steer_motor.sim_state
                encoder = module_to_apply.encoder.sim_state

                if isinstance(drive_motor, TalonFXSSimState):
                    drive_motor.motor_orientation = (
                        ChassisReference.Clockwise_Positive
                        if sim_module.drive_motor_inverted
                        else ChassisReference.CounterClockwise_Positive
                    )
                else:
                    drive_motor.orientation = (
                        ChassisReference.Clockwise_Positive
                        if sim_module.drive_motor_inverted
                        else ChassisReference.CounterClockwise_Positive
                    )

                if isinstance(steer_motor, TalonFXSSimState):
                    steer_motor.motor_orientation = (
                        ChassisReference.Clockwise_Positive
                        if sim_module.steer_motor_inverted
                        else ChassisReference.CounterClockwise_Positive
                    )
                    steer_motor.ext_sensor_orientation = (
                        ChassisReference.Clockwise_Positive
                        if sim_module.steer_motor_inverted != sim_module.encoder_inverted
                        else ChassisReference.CounterClockwise_Positive
                    )
                else:
                    steer_motor.orientation = (
                        ChassisReference.Clockwise_Positive
                        if sim_module.steer_motor_inverted
                        else ChassisReference.CounterClockwise_Positive
                    )

                if isinstance(encoder, CANcoderSimState):
                    encoder.orientation = (
                        ChassisReference.Clockwise_Positive
                        if sim_module.encoder_inverted
                        else ChassisReference.CounterClockwise_Positive
                    )
                elif isinstance(encoder, CANdiSimState):
                    # encoder.orientation = (
                    #     ChassisReference.Clockwise_Positive
                    #     if sim_module.encoder_inverted
                    #     else ChassisReference.CounterClockwise_Positive
                    # )
                    pass

                drive_motor.set_supply_voltage(supply_voltage)
                steer_motor.set_supply_voltage(supply_voltage)
                encoder.set_supply_voltage(supply_voltage)

                sim_module.drive_motor.setInputVoltage(
                    self.add_friction(drive_motor.motor_voltage, sim_module.drive_friction_voltage)
                )
                sim_module.steer_motor.setInputVoltage(
                    self.add_friction(steer_motor.motor_voltage, sim_module.steer_friction_voltage)
                )

                sim_module.drive_motor.update(dt)
                sim_module.steer_motor.update(dt)

                drive_motor.set_raw_rotor_position(sim_module.drive_motor.getAngularPosition() / (2 * math.pi) * sim_module.drive_gearing)
                drive_motor.set_rotor_velocity(sim_module.drive_motor.getAngularVelocity() / (2 * math.pi) * sim_module.drive_gearing)

                steer_motor.set_raw_rotor_position(sim_module.steer_motor.getAngularPosition() / (2 * math.pi) * sim_module.steer_gearing)
                steer_motor.set_rotor_velocity(sim_module.steer_motor.getAngularVelocity() / (2 * math.pi) * sim_module.steer_gearing)
                if isinstance(steer_motor, TalonFXSSimState):
                    # azimuth encoders see the mechanism, so don't account for the steer gearing
                    steer_motor.set_pulse_width_position(sim_module.steer_motor.getAngularPosition() / (2 * math.pi))
                    steer_motor.set_pulse_width_velocity(sim_module.steer_motor.getAngularVelocity() / (2 * math.pi))

                if isinstance(encoder, CANcoderSimState):
                    # azimuth encoders see the mechanism, so don't account for the steer gearing
                    encoder.set_raw_position(sim_module.steer_motor.getAngularPosition() / (2 * math.pi))
                    encoder.set_velocity(sim_module.steer_motor.getAngularVelocity() / (2 * math.pi))
                elif isinstance(encoder, CANdiSimState):
                    # azimuth encoders see the mechanism, so don't account for the steer gearing
                    # encoder.set_raw_position(sim_module.steer_motor.getAngularPosition() / (2 * math.pi))
                    # encoder.set_velocity(sim_module.steer_motor.getAngularVelocity() / (2 * math.pi))
                    pass

            states = [module.get_current_state() for module in modules_to_apply]

            angular_vel: radians_per_second = self._kinem.toChassisSpeeds(tuple(states)).omega
            self._last_angle = self._last_angle + Rotation2d(angular_vel * dt)
            self._pigeon_sim.set_raw_yaw(self._last_angle.degrees())
            self._pigeon_sim.set_angular_velocity_z(math.degrees(angular_vel))

        @staticmethod
        def add_friction(motor_voltage: volt, friction_voltage: volt) -> volt:
            """
            Applies the effects of friction to dampen the motor voltage.

            :param motor_voltage: Voltage output by the motor
            :type motor_voltage: volt
            :param friction_voltage: Voltage required to overcome friction
            :type friction_voltage: volt
            :returns: Friction-dampened motor voltage
            :rtype: volt
            """
            if math.fabs(motor_voltage) < friction_voltage:
                motor_voltage = 0.0
            elif motor_voltage > 0.0:
                motor_voltage -= friction_voltage
            else:
                motor_voltage += friction_voltage
            return motor_voltage

except ImportError:
    pass
