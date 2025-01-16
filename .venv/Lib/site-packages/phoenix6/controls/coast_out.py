"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.phoenix_native import Native
from phoenix6.status_code import StatusCode
from phoenix6.units import *
import ctypes


class CoastOut:
    """
    Request coast neutral output of actuator.  The bridge is disabled and the rotor
    is allowed to coast.
    
    :param use_timesync:    Set to true to delay applying this control request until
                            a timesync boundary (requires Phoenix Pro and CANivore).
                            This eliminates the impact of nondeterministic network
                            delays in exchange for a larger but deterministic
                            control latency.
                            
                            This requires setting the ControlTimesyncFreqHz config
                            in MotorOutputConfigs. Additionally, when this is
                            enabled, the UpdateFreqHz of this request should be set
                            to 0 Hz.
    :type use_timesync: bool
    """

    def __init__(self, use_timesync: bool = False):
        self._name = "CoastOut"
        self.update_freq_hz: hertz = 100.0
        """
        The period at which this control will update at.
        This is designated in Hertz, with a minimum of 20 Hz
        (every 50 ms) and a maximum of 1000 Hz (every 1 ms).

        If this field is set to 0 Hz, the control request will
        be sent immediately as a one-shot frame. This may be useful
        for advanced applications that require outputs to be
        synchronized with data acquisition. In this case, we
        recommend not exceeding 50 ms between control calls.
        """
        
        self.use_timesync = use_timesync
        """
        Set to true to delay applying this control request until a timesync boundary
        (requires Phoenix Pro and CANivore). This eliminates the impact of
        nondeterministic network delays in exchange for a larger but deterministic
        control latency.
        
        This requires setting the ControlTimesyncFreqHz config in MotorOutputConfigs.
        Additionally, when this is enabled, the UpdateFreqHz of this request should be
        set to 0 Hz.
        """

    @property
    def name(self) -> str:
        """
        Gets the name of this control request.

        :returns: Name of the control request
        :rtype: str
        """
        return self._name

    def __str__(self) -> str:
        ss = []
        ss.append("Control: CoastOut")
        ss.append("    use_timesync: " + str(self.use_timesync))
        return "\n".join(ss)

    def _send_request(self, network: str, device_hash: int) -> StatusCode:
        """
        Sends this request out over CAN bus to the device for
        the device to apply.

        :param network: Network to send request over
        :type network: str
        :param device_hash: Device to send request to
        :type device_hash: int
        :returns: Status of the send operation
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlCoastOut(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, self.use_timesync))

    
    def with_use_timesync(self, new_use_timesync: bool) -> 'CoastOut':
        """
        Modifies this Control Request's use_timesync parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to true to delay applying this control request until a timesync boundary
        (requires Phoenix Pro and CANivore). This eliminates the impact of
        nondeterministic network delays in exchange for a larger but deterministic
        control latency.
        
        This requires setting the ControlTimesyncFreqHz config in MotorOutputConfigs.
        Additionally, when this is enabled, the UpdateFreqHz of this request should be
        set to 0 Hz.
    
        :param new_use_timesync: Parameter to modify
        :type new_use_timesync: bool
        :returns: Itself
        :rtype: CoastOut
        """
        self.use_timesync = new_use_timesync
        return self

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'CoastOut':
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
        :rtype: CoastOut
        """
        self.update_freq_hz = new_update_freq_hz
        return self

    @property
    def control_info(self) -> dict:
        """
        Gets information about this control request.

        :returns: Dictonary of control parameter names and corresponding applied values
        :rtype: dict
        """
        control_info = {}
        control_info["name"] = self._name
        control_info["use_timesync"] = self.use_timesync
        return control_info
