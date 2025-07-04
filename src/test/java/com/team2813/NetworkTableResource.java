package com.team2813;

import edu.wpi.first.networktables.NetworkTableInstance;
import org.junit.rules.ExternalResource;

/**
 * JUnit Rule for providing an isolated NetworkTableInstance to tests.
 *
 * @deprecated Use {@link com.team2813.lib2813.testing.junit.jupiter.IsolatedNetworkTablesExtension}
 */
@Deprecated
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
