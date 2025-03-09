package com.team2813;

import edu.wpi.first.networktables.NetworkTableInstance;
import org.junit.rules.ExternalResource;

public final class NetworkTableResource extends ExternalResource {
  private NetworkTableInstance networkTableInstance;

  @Override
  protected void before() {
    networkTableInstance = NetworkTableInstance.create();
  }

  @Override
  protected void after() {
    networkTableInstance.close();
    networkTableInstance = null;
  }

  public NetworkTableInstance getNetworkTableInstance() {
    return networkTableInstance;
  }
}
