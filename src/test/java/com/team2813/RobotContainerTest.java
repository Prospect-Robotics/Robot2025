package com.team2813;

import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.JUnit4;

@RunWith(JUnit4.class)
public final class RobotContainerTest {
    private final FakeShuffleboardTabs shuffleboard = new FakeShuffleboardTabs();

    @Test
    public void constructorDoesNotRaise() {
        new RobotContainer(shuffleboard);
    }

    @Test
    public void conBeConstructedMultipleTimes() {
        new RobotContainer(shuffleboard);
    }
}
