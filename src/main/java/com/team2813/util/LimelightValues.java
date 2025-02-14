package com.team2813.util;

import java.util.function.Supplier;

import edu.wpi.first.networktables.NetworkTable;
import edu.wpi.first.networktables.NetworkTableEntry;
import edu.wpi.first.networktables.NetworkTableInstance;

public class LimelightValues {
    private final NetworkTableEntry ledMode;
    private final NetworkTableEntry stream;
    private final NetworkTableEntry pipelineIndex;

    private final DoubleArrayValue fieldLocation;
    private final DoubleValue horizonalOffset;
    private final DoubleValue verticalOffset;
    private final DoubleValue hasTargets;
    private final DoubleValue primaryApriltag;

    public static enum LedState {
        /** Use the LED Mode set in the current pipeline. */
        DEFAULT,
    
        /** Force off. */
        OFF,
    
        /** Force blink. */
        BLINK,
        
        /** Force on. */
        ON
    }

    public LimelightValues() {
        this(NetworkTableInstance.getDefault().getTable("limelight"));
    }

    LimelightValues(NetworkTable table) {
        ledMode = table.getEntry("ledMode");
        stream = table.getEntry("stream");
        pipelineIndex = table.getEntry("pipeline");
        
        fieldLocation = new DoubleArrayValue(table, "botpose");
        primaryApriltag = new DoubleValue(table, "tid");
        horizonalOffset = new DoubleValue(table, "tx");
        verticalOffset = new DoubleValue(table, "ty");
        hasTargets = new DoubleValue(table, "tv");
    }

    private static class DoubleValue implements Supplier<Double> {
        private final NetworkTableEntry entry;
    
        DoubleValue(NetworkTable table, String key) {
            entry = table.getEntry(key);
        }

        /** Returns the current value, or NaN if there is no value. */
        @Override
        public Double get() {
            return entry.getDouble(Double.NaN);
        }
    }

    private static class DoubleArrayValue implements Supplier<Double[]> {
        private final NetworkTableEntry entry;
    
        DoubleArrayValue(NetworkTable table, String key) {
            entry = table.getEntry(key);
        }

        /** Returns the current value, or NaN if there is no value. */
        @Override
        public Double[] get() {
            return entry.getDoubleArray(new Double[0]);
        }
    }


    /** Whether the limelight has any valid targets. */
    public boolean hasTargets() {
        return hasTargets.get() == 1;
    }

   /** Id of the primary Apriltag */
    public int primaryApriltag() {
        return primaryApriltag.get().intValue();
    } 

    public double getTx() {
       return horizonalOffset.get();
    }

    public double getTy() {
        return verticalOffset.get();
    }

    public void setLedState(LedState state) {
        ledMode.setNumber(state.ordinal());
    }

    public LedState getLedState() {
        return LedState.values()[(int) ledMode.getNumber(0)];
    }

    public int getLedStateNum() {
        return ledMode.getNumber(-1).intValue();
    }

    public NetworkTableEntry getStream() {
        return stream;
    }

    public NetworkTableEntry getPipelineIndexEntry() {
        return pipelineIndex;
    }

    public int getPipelineIndex() {
        return (int) pipelineIndex.getInteger(-1);
    }

    /**
     * Gets the location on the field.<br>
     * If there location is undefined, returns an array with all 0s
     * @return a {@link Double} array with the following entries: x, y, z, roll, yaw, pitch
     * @see <a href="https://docs.limelightvision.io/en/latest/coordinate_systems_fiducials.html#field-space">Field space</a>
     */
    public Double[] getFieldLocation() {
        Double[] location = fieldLocation.get();
        if (location.length == 0) {
            location = new Double[6];
            for (int i = 0; i < location.length; i++) {
                location[i] = 0.0;
            }
        }
        return location;
    }
}
