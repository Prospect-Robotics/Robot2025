package com.team2813;

import org.junit.Rule;
import org.junit.Test;

public final class RobotContainerTest {
    @Rule
    public RobotContainerResource robotContainer = new RobotContainerResource();
    @Test
    public void constructorDoesNotRaise() {
        robotContainer.getRobotContainer();
    }
}
