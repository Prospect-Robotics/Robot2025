"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_signal import *
from phoenix6.units import *
from typing import overload
from phoenix6.status_code import StatusCode
from phoenix6.hardware.parent_device import SupportsSendRequest
from phoenix6.controls.music_tone import MusicTone

class SupportsMusic():
    """
    Contains all control functions available for motors that support playing music.
    """
    
    
    @overload
    def set_control(self, request: MusicTone) -> StatusCode:
        """
        Plays a single tone at the user specified frequency.
        
            - MusicTone Parameters: 
                - audio_frequency: Sound frequency to play.  A value of zero will
                                   silence the device. The effective frequency range is
                                   10-20000 Hz.  Any nonzero frequency less than 10 Hz
                                   will be capped to 10 Hz.  Any frequency above 20 kHz
                                   will be capped to 20 kHz.
    
        :param request: Control object to request of the device
        :type request: MusicTone
        :returns: Code response of the request
        :rtype: StatusCode
        """
        ...

    @overload
    def set_control(self, request: SupportsSendRequest) -> StatusCode:
        """
        Control device with generic control request object.

        If control request is not supported by device, this request
        will fail with StatusCode NotSupported

        :param request: Control object to request of the device
        :type request: SupportsSendRequest
        :returns: StatusCode of the request
        :rtype: StatusCode
        """
        ...

    def set_control(self, request: SupportsSendRequest) -> StatusCode:
        pass
    

