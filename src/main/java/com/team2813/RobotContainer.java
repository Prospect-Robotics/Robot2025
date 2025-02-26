// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.ctre.phoenix6.SignalLogger;
import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.auto.NamedCommands;
import com.pathplanner.lib.config.PIDConstants;
import com.pathplanner.lib.config.RobotConfig;
import com.pathplanner.lib.controllers.PPHolonomicDriveController;
import com.team2813.commands.DefaultDriveCommand;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.commands.ManuelIntakePivot;
import com.team2813.commands.RobotCommands;
import com.team2813.commands.ElevatorDefaultCommand;
import com.team2813.subsystems.*;
import com.team2813.sysid.*;
import edu.wpi.first.units.Units;
import edu.wpi.first.units.measure.Time;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;
import edu.wpi.first.wpilibj2.command.*;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;
import org.json.simple.parser.ParseException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import static com.team2813.Constants.DriverConstants.*;
import static com.team2813.Constants.OperatorConstants.*;
import static com.team2813.lib2813.util.ControlUtils.deadband;

public class RobotContainer implements AutoCloseable {
  private static final DriverStation.Alliance ALLIANCE_USED_IN_PATHS = DriverStation.Alliance.Blue;
  
  private final Climb climb = new Climb();
  private final Intake intake = new Intake();
  private final Elevator elevator;
  private final Drive drive;
  private final IntakePivot intakePivot;
  
  private final SendableChooser<Command> autoChooser;
  private final SysIdRoutineSelector sysIdRoutineSelector;
  
  public RobotContainer(ShuffleboardTabs shuffleboard) {
    this.drive = new Drive(shuffleboard);
    this.elevator = new Elevator(shuffleboard);
    this.intakePivot = new IntakePivot(shuffleboard);
    autoChooser = configureAuto(this.drive);

    SmartDashboard.putData("Auto Routine", autoChooser);
    drive.setDefaultCommand(
            new DefaultDriveCommand(
                    drive,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftY()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftX()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getRightX()) * Drive.MAX_ROTATION));
    sysIdRoutineSelector = new SysIdRoutineSelector(new SubsystemRegistry(Set.of(drive)), RobotContainer::getSysIdRoutines, shuffleboard);
    RobotCommands autoCommands = new RobotCommands(intake, intakePivot, elevator);
    configureBindings(autoCommands);
    configureAutoCommands(autoCommands);

  }
  
  /**
   * Configure PathPlanner named commands
   * @see <a href="https://pathplanner.dev/pplib-named-commands.html">PathPlanner docs</a>
   */
  private void configureAutoCommands(RobotCommands autoCommands) {
    Time SECONDS_1 = Units.Seconds.of(1);
    Time SECONDS_2 = Units.Seconds.of(2);
    NamedCommands.registerCommand("score-coral", autoCommands.placeCoral());
    NamedCommands.registerCommand("ScoreL2", new SequentialCommandGroup(
            new ParallelCommandGroup(
                    new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator).withTimeout(SECONDS_2),
                    new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot).withTimeout(SECONDS_2)
            ),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(SECONDS_1), //TODO: Wait until we don't have a note
            new ParallelCommandGroup(
                    new InstantCommand(intake::stopIntakeMotor, intake),
                    new InstantCommand(elevator::disable, elevator)
            )
    ));

    //TODO: Test L2 position works well for L1. If it doesn't make this not an alias (make an actual command)
    NamedCommands.registerCommand("ScoreL1", NamedCommands.getCommand("ScoreL2"));
    NamedCommands.registerCommand("ScoreL3", new SequentialCommandGroup(
            new ParallelCommandGroup(
                    new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.TOP), elevator).withTimeout(SECONDS_2),
                    new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot).withTimeout(SECONDS_2)
            ),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(SECONDS_1), //TODO: Wait until we don't have a note
            new ParallelCommandGroup(
                    new InstantCommand(intake::stopIntakeMotor, intake),
                    new InstantCommand(elevator::disable, elevator)
            )
    ));
    NamedCommands.registerCommand("BumpAlgaeLow", new SequentialCommandGroup(
            new ParallelCommandGroup(
                    new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator).withTimeout(SECONDS_2),
                    new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP), intakePivot).withTimeout(SECONDS_2)
            ),
            new InstantCommand(intake::outakeCoral, intake),
            new WaitCommand(SECONDS_1), //TODO: Wait until we bump low algae
            new ParallelCommandGroup(
                    new InstantCommand(intake::stopIntakeMotor, intake),
                    new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator),
                    new InstantCommand(intakePivot::disable, intakePivot)
            )
    ));
    NamedCommands.registerCommand("BumpAlgaeHigh", new SequentialCommandGroup(
            new ParallelCommandGroup(
                    new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.TOP), elevator).withTimeout(SECONDS_2),
                    new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP), intakePivot).withTimeout(SECONDS_2)
            ),
            new InstantCommand(intake::bumpAlgae, intake),
            new WaitCommand(SECONDS_1), //TODO: Wait until we bump high algae
            new ParallelCommandGroup(
                    new InstantCommand(intake::stopIntakeMotor, intake),
                    new InstantCommand(elevator::disable, elevator),
                    new InstantCommand(intakePivot::disable, intakePivot)
            )
    ));
    NamedCommands.registerCommand("IntakeCoral", new SequentialCommandGroup(
            new ParallelCommandGroup(
                    new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator).withTimeout(SECONDS_2),
                    new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE), intakePivot).withTimeout(SECONDS_2)
            ),
            new InstantCommand(intake::intakeCoral),
            new WaitCommand(SECONDS_1), //TODO: Wait until we have intaked a note.
            new ParallelCommandGroup(
                    new InstantCommand(intake::stopIntakeMotor, intake),
                    new InstantCommand(elevator::disable, elevator),
                    new InstantCommand(intakePivot::disable, intakePivot)
            )
    ));
  }

  private static SendableChooser<Command> configureAuto(Drive drive) {
    RobotConfig config;
    try {
      config = RobotConfig.fromGUISettings();
    } catch (IOException | ParseException e) {
      // Or handle the error more gracefully
      throw new RuntimeException("Could not get config!", e);
    }
    AutoBuilder.configure(
            drive::getPose, // Robot pose supplier
            drive::setPose, // Method to reset odometry (will be called if your auto has a starting pose)
            drive::getRobotRelativeSpeeds, // ChassisSpeeds supplier. MUST BE ROBOT RELATIVE
            drive::drive, // Method that will drive the robot given ROBOT RELATIVE ChassisSpeeds. Also optionally outputs individual module feedforwards
            new PPHolonomicDriveController( // PPHolonomicController is the built in path following controller for holonomic drive trains
                    new PIDConstants(15, 0.0, 0), // Translation PID constants
                    new PIDConstants(6.85, 0.0, 1.3) // Rotation PID constants //make lower but 5 doesnt work
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
    return AutoBuilder.buildAutoChooser();
  }

  private void configureBindings() {
    // Every subsystem should be in the set; we don't know what subsystem will be controlled, so assume we control all of them
    SYSID_RUN.whileTrue(new DeferredCommand(sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
  }
  
  private static double modifyAxis(double value) {
    value = deadband(value, 0.1);
    value = Math.copySign(value * value, value);
    return value;
  }
  
  private static final SwerveSysidRequest DRIVE_SYSID = new SwerveSysidRequest(MotorType.Drive, RequestType.TorqueCurrentFOC);
  private static final SwerveSysidRequest STEER_SYSID = new SwerveSysidRequest(MotorType.Swerve, RequestType.VoltageOut);
  
  private static List<DropdownEntry> getSysIdRoutines(SubsystemRegistry registry) {
    List<DropdownEntry> routines = new ArrayList<>();
    routines.add(new DropdownEntry("Drive-Drive Motor", new SysIdRoutine(
            new SysIdRoutine.Config(null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
            new SysIdRoutine.Mechanism(
                    (v) -> registry.getSubsystem(Drive.class).runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)
            )
    )));
    routines.add(new DropdownEntry("Drive-Steer Motor", new SysIdRoutine(
            new SysIdRoutine.Config(null, null, null, (s) -> SignalLogger.writeString("state", s.toString())),
            new SysIdRoutine.Mechanism(
                    (v) -> registry.getSubsystem(Drive.class).runSysIdRequest(STEER_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)
            )
    )));
    routines.add(new DropdownEntry("Drive-Slip Test (Forward Quasistatic only)", new SysIdRoutine(
            new SysIdRoutine.Config(Units.Volts.of(0.25).per(Units.Second), null, null, (s) -> SignalLogger.writeString("state", s.toString())),
            new SysIdRoutine.Mechanism(
                    (v) -> registry.getSubsystem(Drive.class).runSysIdRequest(DRIVE_SYSID.withVoltage(v)),
                    null,
                    registry.getSubsystem(Drive.class)
            )
    )));
    return routines;
  }
  
  private void configureBindings(RobotCommands autoCommands) {
    //Driver
    SLOWMODE_BUTTON.whileTrue(new InstantCommand(() -> drive.enableSlowMode(true), drive));
    SLOWMODE_BUTTON.onFalse(new InstantCommand(() -> drive.enableSlowMode(false), drive));
    PLACE_CORAL.onTrue(autoCommands.placeCoral());
    SLOWMODE_BUTTON.onTrue(new InstantCommand(() -> drive.enableSlowMode(true), drive));
    SLOWMODE_BUTTON.onFalse(new InstantCommand(() -> drive.enableSlowMode(false), drive));
    
    // Every subsystem should be in the set; we don't know what subsystem will be controlled, so assume we control all of them
    SYSID_RUN.whileTrue(new DeferredCommand(sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
    INTAKE_BUTTON.whileTrue(
            new SequentialCommandGroup(
                    new ParallelCommandGroup(
                            new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator).withTimeout(Units.Seconds.of(2)),
                            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.INTAKE), intakePivot).withTimeout(Units.Seconds.of(0.5))
                    ),
                    new InstantCommand(intake::intakeCoral, intake)
            )
    );
    INTAKE_BUTTON.onFalse(new InstantCommand(intake::stopIntakeMotor, intake));
    
    OUTTAKE_BUTTON.onTrue(new InstantCommand(intake::outakeCoral, intake));
    OUTTAKE_BUTTON.onFalse(new InstantCommand(intake::stopIntakeMotor, intake));
    
    PREP_L2_CORAL.onTrue(new ParallelCommandGroup(
            new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator),
            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot)
    ));
    PREP_L3_CORAL.onTrue(new ParallelCommandGroup(
            new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.TOP), elevator),
            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot)
    ));
  /* Is there code for algea intake?
  R2.whileTrue(
    new InstantCommand()
    );*/
    elevator.setDefaultCommand(
        new ElevatorDefaultCommand(elevator, () -> -OPERATOR_CONTROLLER.getRightY()));
    intakePivot.setDefaultCommand(
        new ManuelIntakePivot(intakePivot, () -> -OPERATOR_CONTROLLER.getLeftY()));
                     
    CLIMB_DOWN.onTrue(new SequentialCommandGroup(
    new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP), intakePivot)
    ,new InstantCommand(climb::lower, climb)));
    CLIMB_DOWN.onFalse(new InstantCommand(climb::stop, climb));
    
    CLIMB_UP.onTrue(new InstantCommand(climb::raise, climb));
    CLIMB_UP.onFalse(new InstantCommand(climb::stop, climb));
    
    ALGAE_BUMP.whileTrue(new SequentialCommandGroup(
            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Rotations.ALGAE_BUMP), intakePivot).withTimeout(Units.Seconds.of(2)),
            new InstantCommand(intake::bumpAlgae, intake)
    ));
    ALGAE_BUMP.onFalse(new ParallelCommandGroup(
            new InstantCommand(() -> intakePivot.setSetpoint(IntakePivot.Rotations.OUTTAKE), intakePivot),
            new InstantCommand(intake::stopIntakeMotor, intake)
    ));
  }

  public Command getAutonomousCommand() {
    return autoChooser.getSelected();
  }

  @Override
  public void close() {
    climb.close();
  }
}
