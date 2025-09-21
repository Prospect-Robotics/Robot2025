// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import static com.team2813.Constants.DriverConstants.*;
import static com.team2813.Constants.OperatorConstants.*;

import com.ctre.phoenix6.SignalLogger;
import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.auto.NamedCommands;
import com.pathplanner.lib.events.EventTrigger;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.commands.OuttakeCommand;
import com.team2813.lib2813.limelight.BotPoseEstimate;
import com.team2813.lib2813.limelight.Limelight;
import com.team2813.subsystems.*;
import com.team2813.subsystems.climb.Climb;
import com.team2813.subsystems.drive.Drive;
import com.team2813.subsystems.drive.DriveSubsystem;
import com.team2813.subsystems.elevator.Elevator;
import com.team2813.subsystems.intake.Intake;
import com.team2813.subsystems.intake.IntakePivot;
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
import java.util.ArrayList;
import java.util.List;

public class RobotContainer implements AutoCloseable {
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
    var registry = new SubsystemRegistry();
    this.drive = Drive.create(networkTableInstance, registry);
    this.elevator = Elevator.create(networkTableInstance, () -> -OPERATOR_CONTROLLER.getRightY());
    this.intakePivot = IntakePivot.create(networkTableInstance);
    this.climb = Climb.create(networkTableInstance);
    this.intake = Intake.create(networkTableInstance);
    this.groundIntakePivot = new GroundIntakePivot(networkTableInstance);
    autoChooser =
        configureAuto(drive, elevator, intakePivot, intake, groundIntake, groundIntakePivot);
    SmartDashboard.putData("Auto Routine", autoChooser);
    sysIdRoutineSelector =
        new SysIdRoutineSelector(registry, RobotContainer::getSysIdRoutines, shuffleboard);
    configureBindings();
  }

  /**
   * Configure PathPlanner named commands
   *
   * @see <a href="https://pathplanner.dev/pplib-named-commands.html">PathPlanner docs</a>
   */
  private static void configureAutoCommands(
      Elevator elevator,
      IntakePivot intakePivot,
      Intake intake,
      GroundIntake groundIntake,
      GroundIntakePivot groundIntakePivot) {
    Time SECONDS_1 = Units.Seconds.of(1);
    Time SECONDS_HALF = Units.Seconds.of(0.5);
    Time SECONDS_2 = Units.Seconds.of(2);
    Time DROP_CORAL = Units.Seconds.of(0.4);
    Time INTAKE_TIME = Units.Seconds.of(3);

    NamedCommands.registerCommand(
        "PrepareL2",
        new ParallelCommandGroup(
            intakePivot.setSetpointCommand(IntakePivot.Rotations.OUTTAKE),
            elevator.setSetpointCommand(Elevator.Position.BOTTOM)));

    NamedCommands.registerCommand(
        "PrepareL3",
        new ParallelCommandGroup(
            intakePivot.setSetpointCommand(IntakePivot.Rotations.OUTTAKE),
            elevator.setSetpointCommand(Elevator.Position.TOP)));

    NamedCommands.registerCommand(
        "PrepareScore", intakePivot.setSetpointCommand(IntakePivot.Rotations.OUTTAKE));

    NamedCommands.registerCommand(
        "ScoreL2",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.OUTTAKE)),
            intake.slowOuttakeItemCommand(),
            new WaitCommand(DROP_CORAL),
            new ParallelCommandGroup(
                intake.stopMotorCommand(),
                elevator.disableCommand(),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "ScoreL1",
        new ParallelCommandGroup(
            groundIntake.outtakeItemCommand(),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                groundIntakePivot)));

    NamedCommands.registerCommand(
        "ScoreL3",
        new SequentialCommandGroup(
            elevator.moveToPositionCommand(Elevator.Position.TOP),
            intakePivot.moveToPositionCommand(IntakePivot.Rotations.OUTTAKE),
            intake.slowOuttakeItemCommand(),
            new WaitCommand(DROP_CORAL),
            new ParallelCommandGroup(
                intake.stopMotorCommand(),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "BumpAlgaeLow",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.ALGAE_BUMP)),
            intake.outtakeItemCommand(),
            new WaitCommand(SECONDS_1), // TODO: Wait until we bump low algae
            new ParallelCommandGroup(
                intake.stopMotorCommand(),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "BumpAlgaeHigh",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                new SequentialCommandGroup(
                    new WaitCommand(0.05), elevator.setSetpointCommand(Elevator.Position.TOP)),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.ALGAE_BUMP)),
            intake.bumpAlgaeCommand(),
            new WaitCommand(SECONDS_1), // TODO: Wait until we bump high algae
            new ParallelCommandGroup(
                intake.stopMotorCommand(),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "IntakeCoral",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.INTAKE)),
            intake.intakeItemCommand(),
            new WaitUntilCommand(intake::hasCoral).withTimeout(INTAKE_TIME),
            new ParallelCommandGroup(
                intake.intakeItemCommand(),
                elevator.disableCommand(),
                intakePivot.disableCommand())));

    new EventTrigger("PrepareL2")
        .onTrue(
            new ParallelCommandGroup(
                intakePivot.setSetpointCommand(IntakePivot.Rotations.OUTTAKE),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM)));
    new EventTrigger("PrepareL3")
        .onTrue(
            new ParallelCommandGroup(
                intakePivot.setSetpointCommand(IntakePivot.Rotations.OUTTAKE),
                elevator.setSetpointCommand(Elevator.Position.TOP)));
  }

  private static SendableChooser<Command> configureAuto(
      Drive drive,
      Elevator elevator,
      IntakePivot intakePivot,
      Intake intake,
      GroundIntake groundIntake,
      GroundIntakePivot groundIntakePivot) {
    drive.configurePathPlanner();
    configureAutoCommands(elevator, intakePivot, intake, groundIntake, groundIntakePivot);
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
                            .getSubsystem(DriveSubsystem.class)
                            .runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(DriveSubsystem.class)))));
    routines.add(
        new DropdownEntry(
            "Drive-Steer Motor",
            new SysIdRoutine(
                new SysIdRoutine.Config(
                    null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
                new SysIdRoutine.Mechanism(
                    (v) ->
                        registry
                            .getSubsystem(DriveSubsystem.class)
                            .runSysIdRequest(STEER_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(DriveSubsystem.class)))));
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
                            .getSubsystem(DriveSubsystem.class)
                            .runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(DriveSubsystem.class)))));
    return routines;
  }

  private void configureBindings() {
    // Driver
    SLOWMODE_BUTTON.whileTrue(drive.enableSlowModeCommand(true));
    SLOWMODE_BUTTON.onFalse(drive.enableSlowModeCommand(false));
    SLOWMODE_BUTTON.onTrue(drive.enableSlowModeCommand(true));
    SETPOSE.onTrue(
        new InstantCommand(
            () ->
                Limelight.getDefaultLimelight()
                    .getLocationalData()
                    .getBotpose()
                    .map(Pose3d::toPose2d)
                    .map(RobotContainer::toBotposeBlue)
                    .ifPresent(drive::setPose)));
    RESET_POSE.onTrue(drive.resetPoseCommand());

    // Every subsystem should be in the set; we don't know what subsystem will be controlled, so
    // assume we control all of them
    // TODO: Reimplement with photonvision.
    AUTO_ALIGN_LEFT.onTrue(
        new InstantCommand(
            () ->
                DriverStation.reportWarning(
                    "Attempted to auto align left, but there is no limelight implementation.",
                    false)));
    // TODO: Reimplement with photonvision.
    AUTO_ALIGN_RIGHT.onTrue(
        new InstantCommand(
            () ->
                DriverStation.reportWarning(
                    "Attempted to auto align right, but there is no limelight implementation.",
                    false)));

    SYSID_RUN.whileTrue(
        new DeferredCommand(
            sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
    INTAKE_BUTTON.whileTrue(
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.INTAKE),
                intake.intakeItemCommand())));
    INTAKE_BUTTON.onFalse(intake.stopMotorCommand());

    GROUND_CORAL_INTAKE.whileTrue(
        new SequentialCommandGroup(
            new LockFunctionCommand(
                groundIntakePivot::atPosition,
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.BOTTOM),
                groundIntakePivot),
            groundIntake.intakeItemCommand()));
    GROUND_CORAL_INTAKE.onFalse(
        new ParallelCommandGroup(
            groundIntake.stopMotorCommand(),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
                groundIntakePivot)));

    OUTTAKE_BUTTON.onTrue(OuttakeCommand.create(intake, groundIntake, groundIntakePivot));
    CATCH_CORAL.onTrue(
        new ParallelCommandGroup(
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                groundIntakePivot),
            groundIntake.intakeItemCommand()));
    CATCH_CORAL.onFalse(
        new ParallelCommandGroup(
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
                groundIntakePivot),
            groundIntake.stopMotorCommand()));

    PREP_L2_CORAL.onTrue(
        new ParallelCommandGroup(
            elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
            intakePivot.moveToPositionCommand(IntakePivot.Rotations.OUTTAKE)));
    PREP_L3_CORAL.onTrue(
        new ParallelCommandGroup(
            elevator.moveToPositionCommand(Elevator.Position.TOP),
            intakePivot.moveToPositionCommand(IntakePivot.Rotations.OUTTAKE)));
    /* Is there code for algea intake?
    R2.whileTrue(
      new InstantCommand()
      );*/

    CLIMB_DOWN.onTrue(
        new SequentialCommandGroup(
            intakePivot.moveToPositionCommand(IntakePivot.Rotations.ALGAE_BUMP),
            climb.lowerCommand()));
    CLIMB_DOWN.onFalse(climb.stopCommand());

    CLIMB_UP.whileTrue(climb.raiseCommand());
    CLIMB_UP.onFalse(climb.stopCommand());

    ALGAE_BUMP.whileTrue(
        new SequentialCommandGroup(
            intakePivot.moveToPositionCommand(IntakePivot.Rotations.ALGAE_BUMP),
            intake.bumpAlgaeCommand()));
    ALGAE_BUMP.onFalse(
        new ParallelCommandGroup(
            intakePivot.setSetpointCommand(IntakePivot.Rotations.OUTTAKE),
            intake.stopMotorCommand()));

    SLOW_OUTTAKE.onTrue(intake.slowOuttakeItemCommand());
    SLOW_OUTTAKE.onFalse(intake.stopMotorCommand());

    MANUAL_GROUND_OUTTAKE.onTrue(groundIntake.outtakeItemCommand());
    MANUAL_GROUND_OUTTAKE.onFalse(groundIntake.stopMotorCommand());
    MANUAL_GROUND_INTAKE.onTrue(groundIntake.intakeItemCommand());
    MANUAL_GROUND_INTAKE.onFalse(groundIntake.stopMotorCommand());
    MANUAL_GROUND_UP.onTrue(
        new InstantCommand(
            () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
            groundIntakePivot));
    MANUAL_GROUND_DOWN.onTrue(
        new InstantCommand(
            () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.BOTTOM),
            groundIntakePivot));
    MANUAL_GROUND_STOW.onTrue(
        new InstantCommand(
            () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
            groundIntakePivot));
    MANUAL_FAST_GROUND_OUTTAKE.onTrue(groundIntake.fastOuttakeItemCommand());
    MANUAL_FAST_GROUND_OUTTAKE.onFalse(groundIntake.stopMotorCommand());
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
