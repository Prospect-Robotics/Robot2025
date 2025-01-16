"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_signal import *
from phoenix6.units import *
from phoenix6.hardware.traits.common_talon import CommonTalon
from phoenix6.hardware.traits.supports_foc import SupportsFOC
from phoenix6.hardware.traits.supports_music import SupportsMusic

class CommonTalonWithFOC(CommonTalon, SupportsFOC, SupportsMusic):
    """
    Contains everything common between Talon motor controllers that support FOC
    (requires Phoenix Pro).
    """





