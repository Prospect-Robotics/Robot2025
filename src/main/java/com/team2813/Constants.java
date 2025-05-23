package com.team2813;

import edu.wpi.first.wpilibj2.command.button.CommandPS4Controller;
import edu.wpi.first.wpilibj2.command.button.Trigger;

public final class Constants {

  // Drive train CAN IDs
  // Front Right swerve module
  public static final int FRONT_RIGHT_STEER_ID = 1;
  public static final int FRONT_RIGHT_ENCODER_ID = 2;
  public static final int FRONT_RIGHT_DRIVE_ID = 3;
  // Back Right swerve module
  public static final int BACK_RIGHT_STEER_ID = 4;
  public static final int BACK_RIGHT_ENCODER_ID = 5;
  public static final int BACK_RIGHT_DRIVE_ID = 6;
  // Back Left swerve module
  public static final int BACK_LEFT_STEER_ID = 7;
  public static final int BACK_LEFT_ENCODER_ID = 8;
  public static final int BACK_LEFT_DRIVE_ID = 9;
  // Front Left swerve module
  public static final int FRONT_LEFT_STEER_ID = 10;
  public static final int FRONT_LEFT_ENCODER_ID = 11;
  public static final int FRONT_LEFT_DRIVE_ID = 12;

  public static final int PIGEON_ID = 13;

  // Mechanism CAN IDs
  /** Climb Top */
  public static final int CLIMB_1 = 14;

  /** Climb Bottom */
  public static final int CLIMB_2 = 15;

  /** Elevator Top */
  public static final int ELEVATOR_1 = 16;

  /** Elevator Bottom */
  public static final int ELEVATOR_2 = 17;

  public static final int INTAKE_PIVOT = 18;
  public static final int INTAKE_WHEEL = 19;
  public static final int INTAKE_ENCODER = 20;

  public static final int GROUND_INTAKE_WHEEL = 21;
  public static final int GROUND_INTAKE_PIVOT = 22;

  public static final class DriverConstants {
    private DriverConstants() {
      throw new AssertionError("Not instantiable");
    }

    public static final CommandPS4Controller DRIVER_CONTROLLER = new CommandPS4Controller(0);
    public static final Trigger SYSID_RUN = DRIVER_CONTROLLER.cross().and(() -> false);
    public static final Trigger SLOWMODE_BUTTON = DRIVER_CONTROLLER.L1();
    public static final Trigger PLACE_CORAL = DRIVER_CONTROLLER.R1();
    public static final Trigger RESET_POSE = DRIVER_CONTROLLER.triangle();

    public static Trigger AUTO_ALIGN_LEFT = DRIVER_CONTROLLER.povUp();
    public static Trigger AUTO_ALIGN_RIGHT = DRIVER_CONTROLLER.povDown();

    public static Trigger SETPOSE = DRIVER_CONTROLLER.circle();

    public static final Trigger GROUND_CORAL_INTAKE = DRIVER_CONTROLLER.L2();
    public static final Trigger CATCH_CORAL = DRIVER_CONTROLLER.R2();
  }

  public static final class OperatorConstants {
    private OperatorConstants() {
      throw new AssertionError("Not instantiable");
    }

    public static final CommandPS4Controller OPERATOR_CONTROLLER = new CommandPS4Controller(1);
    public static final Trigger INTAKE_BUTTON = OPERATOR_CONTROLLER.R1();
    public static final Trigger OUTTAKE_BUTTON =
        OPERATOR_CONTROLLER.L1().or(DriverConstants.PLACE_CORAL);
    public static final Trigger PREP_L2_CORAL = OPERATOR_CONTROLLER.cross();
    public static final Trigger PREP_L3_CORAL = OPERATOR_CONTROLLER.triangle();
    public static final Trigger ALGAE_BUMP = OPERATOR_CONTROLLER.L2();
    public static final Trigger CLIMB_DOWN = OPERATOR_CONTROLLER.povDown();
    public static final Trigger CLIMB_UP = OPERATOR_CONTROLLER.povUp();
    public static final Trigger SLOW_OUTTAKE = OPERATOR_CONTROLLER.R2();

    public static final Trigger MANUAL_GROUND_OUTTAKE = OPERATOR_CONTROLLER.square();
    public static final Trigger MANUAL_FAST_GROUND_OUTTAKE = OPERATOR_CONTROLLER.options();
    public static final Trigger MANUAL_GROUND_INTAKE = OPERATOR_CONTROLLER.circle();
    public static final Trigger MANUAL_GROUND_UP = OPERATOR_CONTROLLER.povLeft();
    public static final Trigger MANUAL_GROUND_DOWN = OPERATOR_CONTROLLER.povRight();
    public static final Trigger MANUAL_GROUND_STOW = OPERATOR_CONTROLLER.share();
  }

  private Constants() {
    throw new AssertionError("Not instantiable");
  }
}
