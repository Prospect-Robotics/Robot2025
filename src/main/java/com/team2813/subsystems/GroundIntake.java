package com.team2813.subsystems;

import static com.team2813.Constants.GROUND_INTAKE_WHEEL;

import com.team2813.lib2813.control.InvertType;
import com.team2813.lib2813.control.motors.TalonFXWrapper;
import edu.wpi.first.wpilibj2.command.Command;

/**
 * The Ground intake for the 2025 Robot. This is for intaking coral on the ground and depositing it
 * in L1.
 *
 * @author spderman333
 */
public final class GroundIntake extends IntakeSubsystem {
  // +rotation = intake, -rotation = outtake.
  static final Params PARAMS = Params.builder().setIntakeSpeed(8).setOuttakeSpeed(-2.75).build();

  static final double FAST_OUTTAKE_VOLTAGE = 12;

  public GroundIntake() { // TODO: Ensure this constructor is actually functional.
    super(new TalonFXWrapper(GROUND_INTAKE_WHEEL, InvertType.CLOCKWISE), PARAMS);
  }

  public Command fastOuttakeCoralCommand() {
    return setMotorSpeedCommand(FAST_OUTTAKE_VOLTAGE);
  }
}
