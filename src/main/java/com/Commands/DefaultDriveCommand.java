package com.Commands;

import java.util.function.DoubleSupplier;

import com.team2813.subsystems.Drive;

import edu.wpi.first.wpilibj2.command.Command;

public class DefaultDriveCommand extends Command{
    private final Drive driveSubsystem;
    private final DoubleSupplier translationXSupplier;
    private final DoubleSupplier translationYSupplier;
    private final DoubleSupplier rotationSupplier;

    public DefaultDriveCommand(DoubleSupplier translationXSupplier,
                               DoubleSupplier translationYSupplier,
                               DoubleSupplier rotationSupplier,
                               Drive driveSubsystem) {
        this.translationXSupplier = translationXSupplier;
        this.translationYSupplier = translationYSupplier;
        this.rotationSupplier = rotationSupplier;
        this.driveSubsystem = driveSubsystem;

        addRequirements(driveSubsystem);

         @Override
    public void execute() {
        driveSubsystem.drive(
			translationXSupplier.getAsDouble(),
			translationYSupplier.getAsDouble(),
			rotationSupplier.getAsDouble()
			);
    }
    
    
}
