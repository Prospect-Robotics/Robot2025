package com.team2813.subsystems.drive;

import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.Supplier;

final class DefaultCommand extends Command {
  private final DriveSubsystem drive;
  private final Supplier<Double> xSupplier;
  private final Supplier<Double> ySupplier;
  private final Supplier<Double> rotationSupplier;

  public DefaultCommand(
      DriveSubsystem drive,
      Supplier<Double> xSupplier,
      Supplier<Double> ySupplier,
      Supplier<Double> rotationSupplier) {
    this.drive = drive;
    this.xSupplier = xSupplier;
    this.ySupplier = ySupplier;
    this.rotationSupplier = rotationSupplier;
    addRequirements(drive);
  }

  @Override
  public void execute() {
    drive.drive(xSupplier.get(), ySupplier.get(), rotationSupplier.get());
  }
}
