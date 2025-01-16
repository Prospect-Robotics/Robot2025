"""
Phoenix 6 library built for Python.

View documentation for Phoenix 6, Tuner, and other CTR documentation
at the CTR documentation landing page: docs.ctr-electronics.com
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""


from .all_timestamps import AllTimestamps
from .timestamp import Timestamp
from .units import *
from .base_status_signal import BaseStatusSignal
from .status_signal import StatusSignal, SignalMeasurement
from .signal_logger import SignalLogger
from .hoot_replay import HootReplay
from .orchestra import Orchestra
from .canbus import CANBus
from .status_code import StatusCode
from . import hardware
from . import controls
from . import configs
from . import signals
from . import sim

__all__ = [
    "BaseStatusSignal",
    "StatusSignal",
    "SignalMeasurement",
    "volt",
    "ampere",
    "rotation",
    "rotations_per_second",
    "rotations_per_second_squared",
    "rotations_per_second_cubed",
    "degree",
    "degrees_per_second",
    "celsius",
    "microsecond",
    "millisecond",
    "second",
    "microtesla",
    "g",
    "hertz",
    "Timestamp",
    "AllTimestamps",
    "SignalLogger",
    "HootReplay",
    "Orchestra",
    "CANBus",
    "StatusCode",
    "ParentDevice",
    "hardware",
    "controls",
    "configs",
    "signals",
    "sim",
]
