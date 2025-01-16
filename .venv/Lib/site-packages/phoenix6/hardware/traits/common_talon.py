"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from phoenix6.status_signal import *
from phoenix6.units import *
from phoenix6.hardware.traits.has_talon_controls import HasTalonControls
from phoenix6.hardware.traits.has_talon_signals import HasTalonSignals

class CommonTalon(HasTalonControls, HasTalonSignals):
    """
    Contains everything common between Talon motor controllers.
    """





