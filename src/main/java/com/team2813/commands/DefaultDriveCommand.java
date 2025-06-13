package com.team2813.commands;

import com.team2813.subsystems.Drive;
import com.team2813.subsystems.DriveInterface;
import edu.wpi.first.wpilibj2.command.Command;
import java.util.function.Supplier;

public final class DefaultDriveCommand extends Command {
  private final DriveInterface drive;
  private final Supplier<Double> xSupplier;
  private final Supplier<Double> ySupplier;
  private final Supplier<Double> rotationSupplier;

  public DefaultDriveCommand(
      Drive drive,
      Supplier<Double> xSupplier,
      Supplier<Double> ySupplier,
      Supplier<Double> rotationSupplier) {
    this.drive = drive;
    this.xSupplier = xSupplier;
    this.ySupplier = ySupplier;
    this.rotationSupplier = rotationSupplier;
    addRequirements(drive);
  }

  // Replaces the original drive(x,y, rotation) with the ChassisSpeeds Version.
  @Override
  public void execute() {
    drive.drive(xSupplier.get(), ySupplier.get(), rotationSupplier.get());
  }
}
