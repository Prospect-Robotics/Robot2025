package com.team2813;


import org.junit.Rule;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

@RunWith(JUnit4.class)
public final class RobotContainerTest {
    private final FakeShuffleboardTabs shuffleboard = new FakeShuffleboardTabs();
    
    @Rule
    public final NetworkTableResource networkTable = new NetworkTableResource();

    @Test
    public void constructorDoesNotRaise() {
        //noinspection EmptyTryBlock
        try (var container = new RobotContainer(shuffleboard, networkTable.getNetworkTableInstance())) {}
    }

    @Test
    public void conBeConstructedMultipleTimes() {
        //noinspection EmptyTryBlock
        try (var container = new RobotContainer(shuffleboard, networkTable.getNetworkTableInstance())) {}
    }
}
