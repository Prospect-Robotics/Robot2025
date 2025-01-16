"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

from .has_talon_signals import HasTalonSignals
from .has_talon_controls import HasTalonControls
from .supports_foc import SupportsFOC
from .supports_music import SupportsMusic
from .has_external_motor import HasExternalMotor
from .common_talon_with_external_motor import CommonTalonWithExternalMotor
from .common_talon import CommonTalon
from .common_talon_with_foc import CommonTalonWithFOC

__all__ = [
    "HasTalonSignals",
    "HasTalonControls",
    "SupportsFOC",
    "SupportsMusic",
    "HasExternalMotor",
    "CommonTalonWithExternalMotor",
    "CommonTalon",
    "CommonTalonWithFOC",
]

