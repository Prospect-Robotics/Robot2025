// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import static com.team2813.Constants.DriverConstants.*;
import static com.team2813.Constants.OperatorConstants.*;

import com.ctre.phoenix6.SignalLogger;
import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.auto.NamedCommands;
import com.pathplanner.lib.config.PIDConstants;
import com.pathplanner.lib.config.RobotConfig;
import com.pathplanner.lib.controllers.PPHolonomicDriveController;
import com.pathplanner.lib.events.EventTrigger;
import com.team2813.commands.ElevatorDefaultCommand;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.commands.ManuelIntakePivot;
import com.team2813.commands.RobotCommands;
import com.team2813.commands.RobotLocalization;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.limelight.Limelight;
import com.team2813.subsystems.*;
import com.team2813.sysid.*;
import edu.wpi.first.math.geometry.Pose2d;
import edu.wpi.first.math.geometry.Pose3d;
import edu.wpi.first.math.geometry.Rotation2d;
import edu.wpi.first.networktables.NetworkTableInstance;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Time;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.*;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import org.json.simple.parser.ParseException;

public class RobotContainer implements AutoCloseable {
  private static final DriverStation.Alliance ALLIANCE_USED_IN_PATHS = DriverStation.Alliance.Blue;

  private final Climb climb;
  private final Intake intake;
  private final Elevator elevator;
  private final Drive drive;
  private final IntakePivot intakePivot;
  private final GroundIntake groundIntake = new GroundIntake();
  private final GroundIntakePivot groundIntakePivot;

  private final SendableChooser<Command> autoChooser;
  private final SysIdRoutineSelector sysIdRoutineSelector;

  public RobotContainer(ShuffleboardTabs shuffleboard, NetworkTableInstance networkTableInstance) {
    var localization = new RobotLocalization();
    this.drive = new Drive(networkTableInstance, localization);
    this.elevator = new Elevator(networkTableInstance);
    this.intakePivot = new IntakePivot(networkTableInstance);
    this.climb = new Climb(networkTableInstance);
    this.intake = new Intake(networkTableInstance);
    this.groundIntakePivot = new GroundIntakePivot(networkTableInstance);
    autoChooser = configureAuto(drive, elevator, intakePivot, intake);
    SmartDashboard.putData("Auto Routine", autoChooser);
    sysIdRoutineSelector =
        new SysIdRoutineSelector(
            new SubsystemRegistry(Set.of(drive)), RobotContainer::getSysIdRoutines, shuffleboard);
    RobotCommands autoCommands = new RobotCommands(intake, intakePivot, elevator);
    configureBindings(autoCommands, localization);
  }

  /**
   * Configure PathPlanner named commands
   *
   * @see <a href="https://pathplanner.dev/pplib-named-commands.html">PathPlanner docs</a>
   */
  private static void configureAutoCommands(
      Elevator elevator, IntakePivot intakePivot, Intake intake) {
    Time SECONDS_1 = Units.Seconds.of(1);
    Time SECONDS_HALF = Units.Seconds.of(0.5);
    Time SECONDS_2 = Units.Seconds.of(2);
    Time DROP_CORAL = Units.Seconds.of(0.25);
    Time INTAKE_TIME = Units.Seconds.of(3);

    NamedCommands.registerCommand(
        "PrepareL2",
        new ParallelCommandGroup(
            new InstantCommand(
                () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot),
            new InstantCommand(() -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator)));

    NamedCommands.registerCommand(
        "PrepareL3",
        new ParallelCommandGroup(
            new InstantCommand(
                () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot),
            new InstantCommand(() -> elevator.setSetpoint(Elevator.Position.TOP), elevator)));

    NamedCommands.registerCommand(
        "ScoreL2",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                new LockFunctionCommand(
                        elevator::atPosition,
                        () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                        elevator)
                    .withTimeout(SECONDS_2),
                new LockFunctionCommand(
                        intakePivot::atPosition,
                        () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE),
                        intakePivot)
                    .withTimeout(SECONDS_2)),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(DROP_CORAL),
            new ParallelCommandGroup(
                new InstantCommand(intake::stopIntakeMotor, intake),
                new InstantCommand(elevator::disable, elevator),
                new InstantCommand(
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE), intakePivot))));

    // TODO: Test L2 position works well for L1. If it doesn't make this not an alias (make an
    // actual command)
    // TODO: Since we are adding a dedicated L1 scorer, we should consider updating this to be an
    // actual command.
    NamedCommands.registerCommand("ScoreL1", NamedCommands.getCommand("ScoreL2"));

    NamedCommands.registerCommand(
        "ScoreL3",
        new SequentialCommandGroup(
            new LockFunctionCommand(
                    elevator::atPosition,
                    () -> elevator.setSetpoint(Elevator.Position.TOP),
                    elevator)
                .withTimeout(SECONDS_2),
            new LockFunctionCommand(
                    intakePivot::atPosition,
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE),
                    intakePivot)
                .withTimeout(SECONDS_2),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(DROP_CORAL),
            new ParallelCommandGroup(
                new InstantCommand(intake::stopIntakeMotor, intake),
                new InstantCommand(() -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator),
                new InstantCommand(
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE), intakePivot))));

    NamedCommands.registerCommand(
        "BumpAlgaeLow",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                new LockFunctionCommand(
                        elevator::atPosition,
                        () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                        elevator)
                    .withTimeout(SECONDS_2),
                new LockFunctionCommand(
                        intakePivot::atPosition,
                        () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP),
                        intakePivot)
                    .withTimeout(SECONDS_2)),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(SECONDS_1), // TODO: Wait until we bump low algae
            new ParallelCommandGroup(
                new InstantCommand(intake::stopIntakeMotor, intake),
                new InstantCommand(() -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator),
                new InstantCommand(
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE), intakePivot))));

    NamedCommands.registerCommand(
        "BumpAlgaeHigh",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                new LockFunctionCommand(
                        elevator::atPosition,
                        () -> elevator.setSetpoint(Elevator.Position.TOP),
                        elevator)
                    .withTimeout(SECONDS_2),
                new LockFunctionCommand(
                        intakePivot::atPosition,
                        () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP),
                        intakePivot)
                    .withTimeout(SECONDS_2)),
            new InstantCommand(intake::bumpAlgae, intake),
            new WaitCommand(SECONDS_1), // TODO: Wait until we bump high algae
            new ParallelCommandGroup(
                new InstantCommand(intake::stopIntakeMotor, intake),
                new InstantCommand(() -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator),
                new InstantCommand(
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE), intakePivot))));

    NamedCommands.registerCommand(
        "IntakeCoral",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                new LockFunctionCommand(
                        elevator::atPosition,
                        () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                        elevator)
                    .withTimeout(SECONDS_2),
                new LockFunctionCommand(
                        intakePivot::atPosition,
                        () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE),
                        intakePivot)
                    .withTimeout(SECONDS_2)),
            new InstantCommand(intake::intakeCoral),
            new WaitUntilCommand(intake::hasCoral).withTimeout(INTAKE_TIME),
            new ParallelCommandGroup(
                new InstantCommand(intake::stopIntakeMotor, intake),
                new InstantCommand(elevator::disable, elevator),
                new InstantCommand(intakePivot::disable, intakePivot))));

    new EventTrigger("PrepareL2")
        .onTrue(
            new ParallelCommandGroup(
                new InstantCommand(
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot),
                new InstantCommand(
                    () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator)));
    new EventTrigger("PrepareL3")
        .onTrue(
            new DeferredCommand(
                () -> NamedCommands.getCommand("PrepareL3"), Set.of(intakePivot, elevator)));
  }

  private static SendableChooser<Command> configureAuto(
      Drive drive, Elevator elevator, IntakePivot intakePivot, Intake intake) {
    RobotConfig config;
    try {
      config = RobotConfig.fromGUISettings();
    } catch (IOException | ParseException e) {
      // Or handle the error more gracefully
      throw new RuntimeException("Could not get config!", e);
    }
    AutoBuilder.configure(
        drive::getPose, // Robot pose supplier
        drive
            ::setPose, // Method to reset odometry (will be called if your auto has a starting pose)
        drive::getRobotRelativeSpeeds, // ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
        drive::drive, // Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also
        // optionally outputs individual module feedforwards
        new PPHolonomicDriveController( // PPHolonomicController is the built in path following
            // controller for holonomic drive trains
            new PIDConstants(15, 0.0, 0), // Translation PID constants
            new PIDConstants(
                6.85, 0.0, 1.3) // Rotation PID constants //make lower but 5 doesnt work
            ),
        config, // The robot configuration
        () -> {
          // Boolean supplier that controls when the path will be mirrored for the red alliance
          // This will flip the path being followed to the red side of the field.
          // THE ORIGIN WILL REMAIN ON THE BLUE SIDE
          return DriverStation.getAlliance()
              .map(alliance -> alliance != ALLIANCE_USED_IN_PATHS)
              .orElse(false);
        },
        drive // Reference to this subsystem to set requirements
        );
    configureAutoCommands(elevator, intakePivot, intake);
    return AutoBuilder.buildAutoChooser();
  }

  private static final SwerveSysidRequest DRIVE_SYSID =
      new SwerveSysidRequest(MotorType.Drive, RequestType.TorqueCurrentFOC);
  private static final SwerveSysidRequest STEER_SYSID =
      new SwerveSysidRequest(MotorType.Swerve, RequestType.VoltageOut);

  private static List<DropdownEntry> getSysIdRoutines(SubsystemRegistry registry) {
    List<DropdownEntry> routines = new ArrayList<>();
    routines.add(
        new DropdownEntry(
            "Drive-Drive Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) ->
                        registry
                            .getSubsystem(Drive.class)
                            .runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)))));
    routines.add(
        new DropdownEntry(
            "Drive-Steer Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) ->
                        registry
                            .getSubsystem(Drive.class)
                            .runSysIdRequest(STEER_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)))));
    routines.add(
        new DropdownEntry(
            "Drive-Slip Test (Forward Quasistatic only)",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    Units.Volts.of(0.25).per(Units.Second),
                    null,
                    null,
                    (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) ->
                        registry
                            .getSubsystem(Drive.class)
                            .runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)))));
    return routines;
  }

  private void configureBindings(RobotCommands autoCommands, RobotLocalization localization) {
    // Driver
    SLOWMODE_BUTTON.whileTrue(new InstantCommand(() -> drive.enableSlowMode(true), drive));
    SLOWMODE_BUTTON.onFalse(new InstantCommand(() -> drive.enableSlowMode(false), drive));
    SLOWMODE_BUTTON.onTrue(new InstantCommand(() -> drive.enableSlowMode(true), drive));
    SLOWMODE_BUTTON.onFalse(new InstantCommand(() -> drive.enableSlowMode(false), drive));
    SETPOSE.onTrue(
        new InstantCommand(
            () ->
                Limelight.getDefaultLimelight()
                    .getLocationalData()
                    .getBotpose()
                    .map(Pose3d::toPose2d)
                    .map(RobotContainer::toBotposeBlue)
                    .ifPresent(drive::setPose)));
    RESET_POSE.onTrue(new InstantCommand(drive::resetPose, drive));

    // Every subsystem should be in the set; we don't know what subsystem will be controlled, so
    // assume we control all of them
    AUTO_ALIGN_LEFT.onTrue(
        new SequentialCommandGroup(
            new InstantCommand(
                () ->
                    Limelight.getDefaultLimelight()
                        .getLocationalData()
                        .getBotpose()
                        .map(Pose3d::toPose2d)
                        .map(RobotContainer::toBotposeBlue)
                        .ifPresent(drive::setPose)),
            new WaitCommand(0.2),
            new DeferredCommand(
                () -> localization.getLeftAutoAlignCommand(drive::getPose), Set.of(drive)),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(0.375),
            new InstantCommand(intake::stopIntakeMotor, intake),
            new ParallelCommandGroup(
                new LockFunctionCommand(
                    elevator::atPosition,
                    () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                    elevator),
                new LockFunctionCommand(
                    intakePivot::atPosition,
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE),
                    intakePivot))));

    AUTO_ALIGN_RIGHT.onTrue(
        new SequentialCommandGroup(
            new InstantCommand(
                () ->
                    Limelight.getDefaultLimelight()
                        .getLocationalData()
                        .getBotpose()
                        .map(Pose3d::toPose2d)
                        .map(RobotContainer::toBotposeBlue)
                        .ifPresent(drive::setPose)),
            new WaitCommand(0.2),
            new DeferredCommand(
                () -> localization.getRightAutoAlignCommand(drive::getPose), Set.of(drive)),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(0.375),
            new InstantCommand(intake::stopIntakeMotor, intake),
            new ParallelCommandGroup(
                new LockFunctionCommand(
                    elevator::atPosition,
                    () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                    elevator),
                new LockFunctionCommand(
                    intakePivot::atPosition,
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE),
                    intakePivot))));

    SYSID_RUN.whileTrue(
        new DeferredCommand(
            sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
    INTAKE_BUTTON.whileTrue(
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                new LockFunctionCommand(
                        elevator::atPosition,
                        () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                        elevator)
                    .withTimeout(Units.Seconds.of(2)),
                new LockFunctionCommand(
                        intakePivot::atPosition,
                        () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE),
                        intakePivot)
                    .withTimeout(Units.Seconds.of(0.5))),
            new InstantCommand(intake::intakeCoral, intake)));
    INTAKE_BUTTON.onFalse(new InstantCommand(intake::stopIntakeMotor, intake));

    GROUND_CORAL_INTAKE.whileTrue(
        new SequentialCommandGroup(
            new LockFunctionCommand(
                groundIntakePivot::atPosition,
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.BOTTOM),
                groundIntakePivot),
            new InstantCommand(groundIntake::intakeCoral, groundIntake)));
    GROUND_CORAL_INTAKE.onFalse(
        new ParallelCommandGroup(
            new InstantCommand(groundIntake::stopGroundIntakeMotor, groundIntake),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
                groundIntakePivot)));

    OUTTAKE_BUTTON.onTrue(
        new ParallelCommandGroup(
            new InstantCommand(intake::outakeCoral, intake),
            new InstantCommand(groundIntake::outtakeCoral, groundIntake),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                groundIntakePivot)));
    OUTTAKE_BUTTON.onFalse(
        new ParallelCommandGroup(
            new InstantCommand(intake::stopIntakeMotor, intake),
            new InstantCommand(groundIntake::stopGroundIntakeMotor, groundIntake),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
                groundIntakePivot)));

    PREP_L2_CORAL.onTrue(
        new ParallelCommandGroup(
            new LockFunctionCommand(
                elevator::atPosition,
                () -> elevator.setSetpoint(Elevator.Position.BOTTOM),
                elevator),
            new LockFunctionCommand(
                intakePivot::atPosition,
                () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE),
                intakePivot)));
    PREP_L3_CORAL.onTrue(
        new ParallelCommandGroup(
            new LockFunctionCommand(
                elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.TOP), elevator),
            new LockFunctionCommand(
                intakePivot::atPosition,
                () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE),
                intakePivot)));
    /* Is there code for algea intake?
    R2.whileTrue(
      new InstantCommand()
      );*/
    elevator.setDefaultCommand(
        new ElevatorDefaultCommand(elevator, () -> -OPERATOR_CONTROLLER.getRightY()));
    intakePivot.setDefaultCommand(
        new ManuelIntakePivot(intakePivot, () -> -OPERATOR_CONTROLLER.getLeftY()));

    CLIMB_DOWN.onTrue(
        new SequentialCommandGroup(
            new LockFunctionCommand(
                intakePivot::atPosition,
                () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP),
                intakePivot),
            new InstantCommand(climb::lower, climb)));
    CLIMB_DOWN.onFalse(new InstantCommand(climb::stop, climb));

    CLIMB_UP.whileTrue(
        new SequentialCommandGroup(
            new LockFunctionCommand(climb::limitSwitchPressed, climb::raise, climb),
            new InstantCommand(climb::stop, climb)));
    CLIMB_UP.onFalse(new InstantCommand(climb::stop, climb));

    ALGAE_BUMP.whileTrue(
        new SequentialCommandGroup(
            new LockFunctionCommand(
                    intakePivot::atPosition,
                    () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP),
                    intakePivot)
                .withTimeout(Units.Seconds.of(2)),
            new InstantCommand(intake::bumpAlgae, intake)));
    ALGAE_BUMP.onFalse(
        new ParallelCommandGroup(
            new InstantCommand(
                () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot),
            new InstantCommand(intake::stopIntakeMotor, intake)));

    // SLOW_OUTTAKE.onTrue(new InstantCommand(intake::slowOuttakeCoral, intake));
    // SLOW_OUTTAKE.onFalse(new InstantCommand(intake::stopIntakeMotor, intake));
  }

  private static final Pose2d botposeBlueOrig =
      new Pose2d(Units.Meters.of(-8.7736), Units.Meters.of(-4.0257), new Rotation2d());

  public static Pose2d toBotposeBlue(Pose2d orig) {
    return orig.relativeTo(botposeBlueOrig);
  }

  public static BotPoseEstimate toBotposeBlue(BotPoseEstimate estimate) {
    return new BotPoseEstimate(toBotposeBlue(estimate.pose()), estimate.timestampSeconds());
  }

  public Command getAutonomousCommand() {
    return autoChooser.getSelected();
  }

  @Override
  public void close() {
    climb.close();
    drive.close();
    intake.close();
  }
}
