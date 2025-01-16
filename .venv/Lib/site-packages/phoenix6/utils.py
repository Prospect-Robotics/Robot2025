"""
Utility functions in Phoenix 6
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.units import second

try:
    from wpilib import Timer

    USE_WPILIB = True
except ImportError:
    USE_WPILIB = False


def get_current_time_seconds() -> second:
    """
    Get the current timestamp in seconds.

    This is the time source used for status signals.

    This time source is typically continuous and monotonic.
    However, it may be overridden in simulation to use a
    non-monotonic, non-continuous source.

    :returns: Current time in seconds
    :rtype: second
    """
    return Native.instance().c_ctre_phoenix6_get_current_time_seconds()

def get_system_time_seconds() -> second:
    """
    Get the system timestamp in seconds.

    This is NOT the time source used for status signals.
    Use GetCurrentTImeSeconds instead when working with
    status signal timing.

    This time source is guaranteed to be continuous and
    monotonic, making it useful for measuring time deltas
    in a robot program.

    :returns: System time in seconds
    :rtype: second
    """
    return Native.instance().c_ctre_phoenix6_get_system_time_seconds()


def is_simulation() -> bool:
    """
    Get whether the program is running in simulation.

    :returns: True if in simulation
    :rtype: bool
    """
    return Native.instance().c_ctre_phoenix6_is_simulation()

def is_replay() -> bool:
    """
    Get whether the program is running in replay mode.

    :returns: True if in replay mode
    :rtype: bool
    """
    return Native.instance().c_ctre_phoenix6_is_replay()

if USE_WPILIB:
    def fpga_to_current_time(fpga_time: second) -> second:
        """
        Converts an FPGA timestamp to the timebase
        reported by get_current_time_seconds().

        :param fpga_time: The FPGA timestamp
        :type fpga_time: second
        :returns: The equivalent get_current_time_seconds() timestamp
        :rtype: second
        """
        return (get_current_time_seconds() - Timer.getFPGATimestamp()) + fpga_time
