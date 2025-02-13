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
    public static final int CLIMB_1 = 14;
    public static final int CLIMB_2 = 15;

    public static final int ELEVATOR_1 = 16;
    public static final int ELEVATOR_2 = 17;

    public static final int INTAKE_PIVOT = 18;
    public static final int INTAKE_WHEEL = 19;
    public static final int INTAKE_ENCODER = 20;

    // Algae Mechanisms (might not be used)
    public static final int ALGAE_PIVOT = 21;
    public static final int ALGAE_WHEEL = 22;
    public static final int ALGAE_ENCODER = 23;

    public static final class DriverConstants {
        private DriverConstants() {
            throw new AssertionError("Not instantiable");
        }
        public static final CommandPS4Controller DRIVER_CONTROLLER = new CommandPS4Controller(0);
        public static final Trigger SYSID_RUN = DRIVER_CONTROLLER.cross();
    }

    public static final class OperatorConstants {
        private OperatorConstants() {
            throw new AssertionError("Not instantiable");
        }
        public static final CommandPS4Controller OPERATOR_CONTROLLER = new CommandPS4Controller(1);
    }

    private Constants() {
        throw new AssertionError("Not instantiable");
    }
}
