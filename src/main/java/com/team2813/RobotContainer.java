// Copyright (c) FIRST and other WPILib contributors.
// Open Source Software; you can modify and/or share it under the terms of
// the WPILib BSD license file in the root directory of this project.

package com.team2813;

import com.Commands.DefaultDriveCommand;
import com.team2813.subsystems.Drive;
import com.team2813.subsystems.Intake;

import edu.wpi.first.wpilibj.XboxController;
import edu.wpi.first.wpilibj.simulation.XboxControllerSim;
import edu.wpi.first.wpilibj2.command.Command;
import edu.wpi.first.wpilibj2.command.Commands;
import edu.wpi.first.wpilibj2.command.button.CommandPS4Controller;
import edu.wpi.first.wpilibj2.command.button.Trigger;

public class RobotContainer {
  private final CommandPS4Controller driverController = new CommandPS4Controller(0);
  private final Drive drive = new Drive();
  private final Intake intake = new Intake();
  private final Trigger slowmodeButton = driverController.L1(); //slowmode
  private final Trigger placeCoral = driverController.R1();
  private final Trigger autoPlaceLeft = driverController.square();
  private final Trigger autoPlaceRight = driverController.circle();
  private final Trigger scoreAlgea = driverController.L2();
  //private final IntakePivot intakePivot = new IntakePivot();
  
  public RobotContainer() {
    configureBindings();
      drive.setDefaultCommand(new DefaultDriveCommand(
				() -> -modifyAxis(driverController.getLeftY()) * Drive.MAX_VELOCITY,
				() -> -modifyAxis(driverController.getLeftX()) * Drive.MAX_VELOCITY,
				() -> -modifyAxis(driverController.getRightX()) * Drive.MAX_ANGULAR_VELOCITY,
				drive));
    ));
    

  }

  private void configureBindings() {
    Trigger l1 = driverController.l1();
  }
  public void addDriveCommand()
  public Command getAutonomousCommand() {
    return Commands.print("No autonomous command configured");
  } 
}
