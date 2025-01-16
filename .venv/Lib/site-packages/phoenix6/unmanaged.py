"""
Functions related to more barebones control of devices,
including manually feeding the enable
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.units import second

def feed_enable(timeout_seconds: second):
    """
    Feeds the enable signal with a timeout specified in seconds.
    This function does nothing on a roboRIO during FRC use.

    :param timeout_seconds: Time to remain enabled in seconds
    :type timeout_seconds: second
    """
    Native.instance().c_ctre_phoenix6_unmanaged_feed_enable(int(timeout_seconds * 1000))

def get_api_compliancy() -> int:
    """
    Gets this API's compliancy version

    This is purely used to check compliancy of API against firmware,
    and if there is a mismatch to report to the user.

    :returns: This API's compliancy version
    :rtype: int
    """
    return Native.instance().c_ctre_phoenix6_unmanaged_get_api_compliancy()

def get_phoenix_version() -> int:
    """
    Gets this version of Phoenix

    :returns: This version of Phoenix
    :rtype: int
    """
    return Native.instance().c_ctre_phoenix6_unmanaged_get_phoenix_version()

def get_enable_state() -> bool:
    """
    :returns: true if non-FRC enabled
    :rtype: bool
    """
    return Native.instance().c_ctre_phoenix6_unmanaged_get_enable_state()

def set_phoenix_diagnostics_start_time(start_time_seconds: second):
    """
    Sets the duration of the delay before starting the Phoenix 
    diagnostics server.

    :param start_time_seconds: Magnitude of the delay (in seconds) before
    starting the server. A value of 0 will start the server immediately. A
    negative value will signal the server to shutdown or never start.
    :type start_time_seconds: second
    """
    return Native.instance().c_Phoenix_Diagnostics_SetSecondsToStart(start_time_seconds)

def load_phoenix():
    """
    Calling this function will load and start the Phoenix background tasks.

    This can be useful if you need the Enable/Disable functionality for CAN
    devices but aren't using any of the CAN device classes.

    This function does NOT need to be called if you are using any of the
    Phoenix CAN device classes.
    """
    Native.instance().c_ctre_phoenix6_unmanaged_load_phoenix()
