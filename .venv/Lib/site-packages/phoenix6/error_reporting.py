"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
import traceback as tb
from phoenix6.status_code import StatusCode
from phoenix6.phoenix_native import Native

def report_status_code(status: StatusCode, location: str):
    """
    Reports an error to the Driver Station.
    """
    stack_trace = "".join(tb.format_stack()[:-1])
    Native.instance().c_ctre_phoenix_report_error(
        status.is_error(),
        status.value,
        0,
        ctypes.c_char_p(bytes(status.description, encoding='utf-8')),
        ctypes.c_char_p(bytes(location, encoding='utf-8')),
        ctypes.c_char_p(bytes(stack_trace, encoding='utf-8'))
    )
