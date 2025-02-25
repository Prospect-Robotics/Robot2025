package com.team2813;

import static com.google.common.truth.Truth.assertWithMessage;

import org.junit.rules.ExternalResource;

import java.util.function.Supplier;

public final class RobotContainerProvider extends ExternalResource  {
  private final Supplier<RobotContainer> supplier;
  private RobotContainer robotContainer = null;

  public RobotContainerProvider() {
    this(() -> new RobotContainer(new FakeShuffleboardTabs()));
  }

  public RobotContainerProvider(Supplier<RobotContainer> supplier) {
    this.supplier = supplier;
  }

  public RobotContainer get() {
    if (robotContainer == null) {
      throw new IllegalStateException("Cannot call get() until the RobotContainerProvider @Rule is run");
    }
    return robotContainer;
  }

  @Override
  protected void before() throws Throwable {
    assertWithMessage("before() cannot be called twice").that(robotContainer).isNull();;
    robotContainer = this.supplier.get();
  }

  @Override
  protected void after() {
    if (robotContainer != null) {
      robotContainer.close();
    }
  }
}
