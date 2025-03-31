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
import com.team2813.commands.LockFunctionCommand;
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
    Subsystems subsystems = Subsystems.create(networkTableInstance);
    drive = subsystems.drive();
    elevator = subsystems.elevator();
    intakePivot = subsystems.intakePivot();
    climb = subsystems.climb();
    intake = subsystems.intake();
    groundIntakePivot = new GroundIntakePivot(networkTableInstance);
    autoChooser =
        configureAuto(drive, elevator, intakePivot, intake, groundIntake, groundIntakePivot);
    SmartDashboard.putData("Auto Routine", autoChooser);
    sysIdRoutineSelector =
        new SysIdRoutineSelector(
            subsystems.registry(), RobotContainer::getSysIdRoutines, shuffleboard);
    configureBindings();
  }

  /**
   * Configure PathPlanner named commands
   *
   * @see <a href="https://pathplanner.dev/pplib-named-commands.html">PathPlanner docs</a>
   */
  private static void configureAutoCommands( // TODO: extract class
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
            intake.slowOutakeCoralCommand(),
            new WaitCommand(DROP_CORAL),
            new ParallelCommandGroup(
                intake.stopIntakeMotorCommand(),
                elevator.disableCommand(),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "ScoreL1",
        new ParallelCommandGroup(
            new InstantCommand(groundIntake::outtakeCoral, groundIntake),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                groundIntakePivot)));

    NamedCommands.registerCommand(
        "ScoreL3",
        new SequentialCommandGroup(
            elevator.moveToPositionCommand(Elevator.Position.TOP),
            intakePivot.moveToPositionCommand(IntakePivot.Rotations.OUTTAKE),
            intake.slowOutakeCoralCommand(),
            new WaitCommand(DROP_CORAL),
            new ParallelCommandGroup(
                intake.stopIntakeMotorCommand(),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "BumpAlgaeLow",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.ALGAE_BUMP)),
            intake.outakeCoralCommand(),
            new WaitCommand(SECONDS_1), // TODO: Wait until we bump low algae
            new ParallelCommandGroup(
                intake.stopIntakeMotorCommand(),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "BumpAlgaeHigh",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.TOP),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.ALGAE_BUMP)),
            intake.bumpAlgaeCommand(),
            new WaitCommand(SECONDS_1), // TODO: Wait until we bump high algae
            new ParallelCommandGroup(
                intake.stopIntakeMotorCommand(),
                elevator.setSetpointCommand(Elevator.Position.BOTTOM),
                intakePivot.setSetpointCommand(IntakePivot.Rotations.INTAKE))));

    NamedCommands.registerCommand(
        "IntakeCoral",
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.INTAKE)),
            intake.intakeCoralCommand(),
            new WaitUntilCommand(intake::hasCoral).withTimeout(INTAKE_TIME),
            new ParallelCommandGroup(
                intake.stopIntakeMotorCommand(),
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
        drive.asSubsystem() // Reference to this subsystem to set requirements
        );
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
            new WaitCommand(0.02),
            new DeferredCommand(drive::leftAutoAlignCommand, Set.of(drive.asSubsystem()))));

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
            new WaitCommand(0.02),
            new DeferredCommand(drive::rightAutoAlignCommand, Set.of(drive.asSubsystem()))));

    SYSID_RUN.whileTrue(
        new DeferredCommand(
            sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
    INTAKE_BUTTON.whileTrue(
        new SequentialCommandGroup(
            new ParallelCommandGroup(
                elevator.moveToPositionCommand(Elevator.Position.BOTTOM),
                intakePivot.moveToPositionCommand(IntakePivot.Rotations.INTAKE),
                intake.intakeCoralCommand())));
    INTAKE_BUTTON.onFalse(intake.stopIntakeMotorCommand());

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
            intake.outakeCoralCommand(),
            new InstantCommand(groundIntake::outtakeCoral, groundIntake),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.TOP),
                groundIntakePivot)));
    OUTTAKE_BUTTON.onFalse(
        new ParallelCommandGroup(
            intake.stopIntakeMotorCommand(),
            new InstantCommand(groundIntake::stopGroundIntakeMotor, groundIntake),
            new InstantCommand(
                () -> groundIntakePivot.setSetpoint(GroundIntakePivot.Positions.HARD_STOP),
                groundIntakePivot)));

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
            intake.stopIntakeMotorCommand()));

    SLOW_OUTTAKE.onTrue(intake.slowOutakeCoralCommand());
    SLOW_OUTTAKE.onFalse(intake.stopIntakeMotorCommand());
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
