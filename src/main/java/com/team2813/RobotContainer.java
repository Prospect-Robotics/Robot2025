// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.ctre.phoenix6.SignalLogger;
import com.pathplanner.lib.auto.AutoBuilder;
import com.pathplanner.lib.config.PIDConstants;
import com.pathplanner.lib.config.RobotConfig;
import com.pathplanner.lib.controllers.PPHolonomicDriveController;
import com.team2813.commands.DefaultDriveCommand;
import com.team2813.commands.LockFunctionCommand;
import com.team2813.commands.RobotCommands;
import com.team2813.subsystems.*;
import com.team2813.sysid.*;
import edu.wpi.first.units.Units;
import edu.wpi.first.wpilibj.DriverStation;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj2.command.*;
import edu.wpi.first.wpilibj2.command.button.Trigger;
import edu.wpi.first.wpilibj2.command.sysid.SysIdRoutine;
import org.json.simple.parser.ParseException;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;

import static com.team2813.Constants.DriverConstants.*;
import static com.team2813.Constants.OperatorConstants.*;

public class RobotContainer {
  private static final DriverStation.Alliance ALLIANCE_USED_IN_PATHS = DriverStation.Alliance.Blue;
  private static SwerveSysidRequest DRIVE_SYSID = new SwerveSysidRequest(MotorType.Drive, RequestType.VoltageOut);
  private static SwerveSysidRequest STEER_SYSID = new SwerveSysidRequest(MotorType.Swerve, RequestType.VoltageOut);
  
  private final Climb climb = new Climb();
  private final Intake intake = new Intake();
  private final Elevator elevator = new Elevator();
  private final Drive drive;
  private final IntakePivot intakePivot = new IntakePivot();
  
  private final SendableChooser<Command> autoChooser;
  private final SysIdRoutineSelector sysIdRoutineSelector;
  
  public RobotContainer(ShuffleboardTabs shuffleboard) {
    this.drive = new Drive(shuffleboard);
    autoChooser = configureAuto(this.drive);
    drive.setDefaultCommand(
            new DefaultDriveCommand(
                    drive,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftY()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getLeftX()) * Drive.MAX_VELOCITY,
                    () -> -modifyAxis(DRIVER_CONTROLLER.getRightX()) * Drive.MAX_ROTATION));
    sysIdRoutineSelector = new SysIdRoutineSelector(new SubsystemRegistry(Set.of(drive)), RobotContainer::getSysIdRoutines, shuffleboard);
    RobotCommands autoCommands = new RobotCommands(intake, intakePivot, elevator);
    configureBindings(autoCommands);
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
                    new PIDConstants(5.0, 0.0, 0.0), // Translation PID constants
                    new PIDConstants(5.0, 0.0, 0.0) // Rotation PID constants
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
  
  private static double deadband(double value, double deadband) {
    if (Math.abs(value) > deadband) {
      if (value > 0) {
        return (value - deadband) / (1 - deadband);
      } else {
        return (value + deadband) / (1 - deadband);
      }
    } else {
      return 0;
    }
  }
  
  private static double modifyAxis(double value) {
    value = deadband(value, 0.1);
    value = Math.copySign(value * value, value);
    return value;
  }
  
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
    PLACE_CORAL.onTrue(autoCommands.placeCoral());
    SLOWMODE_BUTTON.onTrue(new InstantCommand(() -> drive.enableSlowMode(true), drive));
    SLOWMODE_BUTTON.onFalse(new InstantCommand(() -> drive.enableSlowMode(false), drive));
    
    // Every subsystem should be in the set; we don't know what subsystem will be controlled, so assume we control all of them
    SYSID_RUN.whileTrue(new DeferredCommand(sysIdRoutineSelector::getSelected, sysIdRoutineSelector.getRequirements()));
    INTAKE_BUTTON.whileTrue(
            new SequentialCommandGroup(
                    new ParallelCommandGroup(
                            new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator).withTimeout(Units.Seconds.of(2)),
                            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Position.OUTTAKE), intakePivot).withTimeout(Units.Seconds.of(2))
                    ),
                    new InstantCommand(intake::intakeCoral, intake)
            )
    );
    INTAKE_BUTTON.onFalse(new InstantCommand(intake::stopIntakeMotor, intake));
    
    OUTTAKE_BUTTON.onTrue(new InstantCommand(intake::intakeCoral, intake));
    OUTTAKE_BUTTON.onFalse(new InstantCommand(intake::stopIntakeMotor, intake));
    
    PREP_L2_CORAL.onTrue(new ParallelCommandGroup(
            new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.BOTTOM), elevator),
            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Position.OUTTAKE), intakePivot)
    ));
    PREP_L3_CORAL.onTrue(new ParallelCommandGroup(
            new LockFunctionCommand(elevator::atPosition, () -> elevator.setSetpoint(Elevator.Position.TOP), elevator),
            new LockFunctionCommand(intakePivot::atPosition, () -> intakePivot.setSetpoint(IntakePivot.Position.OUTTAKE), intakePivot)
    ));
  /* Is there code for algea intake?
  R2.whileTrue(
    new InstantCommand()
    );*/
    CLIMB_DOWN.onTrue(new InstantCommand(climb::lower, climb));
    CLIMB_DOWN.onFalse(new InstantCommand(climb::stop, climb));
    
    CLIMB_UP.onTrue(new InstantCommand(climb::raise, climb));
    CLIMB_UP.onFalse(new InstantCommand(climb::stop, climb));
  }

  public Command getAutonomousCommand() {
    return autoChooser.getSelected();
  }
}

