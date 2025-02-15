package com.team2813;

import org.junit.rules.ExternalResource;

public class RobotContainerResource extends ExternalResource {
  private static RobotContainer robotContainer = null;
  private static Exception exception = null;
  
  @Override
  protected void before() throws Throwable {
    if (exception == null && robotContainer == null) {
      try {
        robotContainer = new RobotContainer();
      } catch (Exception e) {
        exception = e;
      }
    }
  }
  
  /**
   * Gets the {@link RobotContainer}. Throws an exception if the constructor failed
   * @return The {@link RobotContainer}.
   */
  public RobotContainer getRobotContainer() {
    if (exception != null) {
      throw new RuntimeException(exception);
    }
    return robotContainer;
  }
}
