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


class Follower:
    """
    Follow the motor output of another Talon.
    
    If Talon is in torque control, the torque is copied - which will increase the
    total torque applied. If Talon is in percent supply output control, the duty
    cycle is matched.  Motor direction either matches master's configured direction
    or opposes it based on OpposeMasterDirection.
    
    :param master_id:    Device ID of the master to follow.
    :type master_id: int
    :param oppose_master_direction:    Set to false for motor invert to match the
                                       master's configured Invert - which is typical
                                       when master and follower are mechanically
                                       linked and spin in the same direction.  Set
                                       to true for motor invert to oppose the
                                       master's configured Invert - this is typical
                                       where the the master and follower
                                       mechanically spin in opposite directions.
    :type oppose_master_direction: bool
    """

    def __init__(self, master_id: int, oppose_master_direction: bool):
        self._name = "Follower"
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
        
        self.master_id = master_id
        """
        Device ID of the master to follow.
        """
        self.oppose_master_direction = oppose_master_direction
        """
        Set to false for motor invert to match the master's configured Invert - which is
        typical when master and follower are mechanically linked and spin in the same
        direction.  Set to true for motor invert to oppose the master's configured
        Invert - this is typical where the the master and follower mechanically spin in
        opposite directions.
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
        ss.append("Control: Follower")
        ss.append("    master_id: " + str(self.master_id) + " id")
        ss.append("    oppose_master_direction: " + str(self.oppose_master_direction))
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
        return StatusCode(Native.instance().c_ctre_phoenix6_RequestControlFollower(ctypes.c_char_p(bytes(network, 'utf-8')), device_hash, self.update_freq_hz, self.master_id, self.oppose_master_direction))

    
    def with_master_id(self, new_master_id: int) -> 'Follower':
        """
        Modifies this Control Request's master_id parameter and returns itself for
        method-chaining and easier to use request API.
    
        Device ID of the master to follow.
    
        :param new_master_id: Parameter to modify
        :type new_master_id: int
        :returns: Itself
        :rtype: Follower
        """
        self.master_id = new_master_id
        return self
    
    def with_oppose_master_direction(self, new_oppose_master_direction: bool) -> 'Follower':
        """
        Modifies this Control Request's oppose_master_direction parameter and returns itself for
        method-chaining and easier to use request API.
    
        Set to false for motor invert to match the master's configured Invert - which is
        typical when master and follower are mechanically linked and spin in the same
        direction.  Set to true for motor invert to oppose the master's configured
        Invert - this is typical where the the master and follower mechanically spin in
        opposite directions.
    
        :param new_oppose_master_direction: Parameter to modify
        :type new_oppose_master_direction: bool
        :returns: Itself
        :rtype: Follower
        """
        self.oppose_master_direction = new_oppose_master_direction
        return self

    def with_update_freq_hz(self, new_update_freq_hz: hertz) -> 'Follower':
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
        :rtype: Follower
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
        control_info["master_id"] = self.master_id
        control_info["oppose_master_direction"] = self.oppose_master_direction
        return control_info
