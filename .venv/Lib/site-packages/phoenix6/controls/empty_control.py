"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
from phoenix6.units import hertz
import ctypes


class EmptyControl:
    """
    Generic Empty Control class used to do nothing.
    """

    def __init__(self):
        """
        Constructs an empty control request
        """
        self._name = "EmptyControl"

    @property
    def name(self) -> str:
        """
        Gets the name of this control request.

        :returns: Name of the control request
        :rtype: str
        """
        return self._name

    def __str__(self) -> str:
        return "class: EmptyControl"

    def _send_request(self, network: str, device_hash: int) -> StatusCode:
        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlEmpty(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, 0))

    @property
    def control_info(self) -> dict:
        """
        Gets information about this control request.

        :returns: Dictonary of control parameter names and corresponding applied values
        :rtype: dict
        """
        control_info = {}
        control_info["name"] = self._name
        return control_info

    def with_update_freq_hz(self, _: hertz) -> 'EmptyControl':
        """
        Sets the period at which this control will update at.
        This is designated in Hertz, with a minimum of 20 Hz
        (every 50 ms) and a maximum of 1000 Hz (every 1 ms).

        If this field is set to 0 Hz, the control request will
        be sent immediately as a one-shot frame. This may be useful
        for advanced applications that require outputs to be
        synchronized with data acquisition. In this case, we
        recommend not exceeding 50 ms between control calls.

        :param new_update_freq_hz: Parameter to modify
        :type new_update_freq_hz: hertz
        :returns: Itself
        :rtype: EmptyControl
        """
        return self
