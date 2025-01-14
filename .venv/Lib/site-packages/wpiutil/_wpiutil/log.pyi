from __future__ import annotations
import typing
import typing_extensions
__all__ = ['BooleanArrayLogEntry', 'BooleanLogEntry', 'DataLog', 'DataLogEntry', 'DataLogReader', 'DataLogRecord', 'DoubleArrayLogEntry', 'DoubleLogEntry', 'FloatArrayLogEntry', 'FloatLogEntry', 'IntegerArrayLogEntry', 'IntegerLogEntry', 'MetadataRecordData', 'RawLogEntry', 'StartRecordData', 'StringArrayLogEntry', 'StringLogEntry', 'StructArrayLogEntry', 'StructLogEntry']
class BooleanArrayLogEntry(_BooleanArrayLogEntryImpl):
    """
    Log array of boolean values.
    """
    kDataType: typing.ClassVar[str] = 'boolean[]'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, arr: list[bool], timestamp: int = 0) -> None:
        """
        Appends a record to the log.  For find functions to work, timestamp
        must be monotonically increasing.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    @typing.overload
    def update(self, arr: list[bool], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    @typing.overload
    def update(self, arr: list[int], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class BooleanLogEntry(_BooleanLogEntryImpl):
    """
    Log boolean values.
    """
    kDataType: typing.ClassVar[str] = 'boolean'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, value: bool, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, value: bool, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class DataLog:
    """
    A data log for high-speed writing of data values.
    
    The lifetime of the data log object must be longer than any data log entry
    objects that refer to it.
    
    Finish() is needed only to indicate in the log that a particular entry is
    no longer being used (it releases the name to ID mapping).  Finish() is not
    required to be called for data to be flushed to disk; entries in the log
    are written as Append() calls are being made.  In fact, Finish() does not
    need to be called at all; this is helpful to avoid shutdown races where the
    DataLog object might be destroyed before other objects.  It's often not a
    good idea to call Finish() from destructors for this reason.
    
    DataLog calls are thread safe.  DataLog uses a typical multiple-supplier,
    single-consumer setup.  Writes to the log are atomic, but there is no
    guaranteed order in the log when multiple threads are writing to it;
    whichever thread grabs the write mutex first will get written first.
    For this reason (as well as the fact that timestamps can be set to
    arbitrary values), records in the log are not guaranteed to be sorted by
    timestamp.
    """
    _kBlockSize: typing.ClassVar[int] = 16384
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def _bufferFull(self) -> bool:
        """
        Called when internal buffers reach the maximum count.  Called with internal
        mutex held; do not call any other DataLog functions from this function.
        
        :returns: true if log should be paused (don't call PauseLog)
        """
    def _bufferHalfFull(self) -> None:
        """
        Called when internal buffers are half the maximum count.  Called with
        internal mutex held; do not call any other DataLog functions from this
        function.
        """
    def _startFile(self) -> None:
        """
        Starts the log.  Appends file header and Start records and schema data
        values for all previously started entries and schemas.  No effect unless
        the data log is currently stopped.
        """
    @typing.overload
    def addSchema(self, name: str, type: str, schema: typing_extensions.Buffer, timestamp: int = 0) -> None:
        """
        Registers a data schema.  Data schemas provide information for how a
        certain data type string can be decoded.  The type string of a data schema
        indicates the type of the schema itself (e.g. "protobuf" for protobuf
        schemas, "struct" for struct schemas, etc). In the data log, schemas are
        saved just like normal records, with the name being generated from the
        provided name: "/.schema/<name>".  Duplicate calls to this function with
        the same name are silently ignored.
        
        :param name:      Name (the string passed as the data type for records using this
                          schema)
        :param type:      Type of schema (e.g. "protobuf", "struct", etc)
        :param schema:    Schema data
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    @typing.overload
    def addSchema(self, name: str, type: str, schema: str, timestamp: int = 0) -> None:
        """
        Registers a data schema.  Data schemas provide information for how a
        certain data type string can be decoded.  The type string of a data schema
        indicates the type of the schema itself (e.g. "protobuf" for protobuf
        schemas, "struct" for struct schemas, etc). In the data log, schemas are
        saved just like normal records, with the name being generated from the
        provided name: "/.schema/<name>".  Duplicate calls to this function with
        the same name are silently ignored.
        
        :param name:      Name (the string passed as the data type for records using this
                          schema)
        :param type:      Type of schema (e.g. "protobuf", "struct", etc)
        :param schema:    Schema data
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def addStructSchema(self, type: type, timestamp: int = 0) -> None:
        """
        Registers a struct schema. Duplicate calls to this function with the same
        name are silently ignored.
        
        @tparam T struct serializable type
        
        :param type:      optional struct type info
        :param timestamp: Time stamp (0 to indicate now)
        """
    def appendBoolean(self, entry: int, value: bool, timestamp: int) -> None:
        """
        Appends a boolean record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param value:     Boolean value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendBooleanArray(self, entry: int, arr: list[bool], timestamp: int) -> None:
        """
        Appends a boolean array record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param arr:       Boolean array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendDouble(self, entry: int, value: float, timestamp: int) -> None:
        """
        Appends a double record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param value:     Double value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendDoubleArray(self, entry: int, arr: list[float], timestamp: int) -> None:
        """
        Appends a double array record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param arr:       Double array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendFloat(self, entry: int, value: float, timestamp: int) -> None:
        """
        Appends a float record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param value:     Float value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendFloatArray(self, entry: int, arr: list[float], timestamp: int) -> None:
        """
        Appends a float array record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param arr:       Float array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendInteger(self, entry: int, value: int, timestamp: int) -> None:
        """
        Appends an integer record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param value:     Integer value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendIntegerArray(self, entry: int, arr: list[int], timestamp: int) -> None:
        """
        Appends an integer array record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param arr:       Integer array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendRaw(self, entry: int, data: typing_extensions.Buffer, timestamp: int) -> None:
        """
        Appends a raw record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param data:      Byte array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendRaw2(self, entry: int, data: list[typing_extensions.Buffer], timestamp: int) -> None:
        """
        Appends a raw record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param data:      Byte array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendString(self, entry: int, value: str, timestamp: int) -> None:
        """
        Appends a string record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param value:     String value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def appendStringArray(self, entry: int, arr: list[str], timestamp: int) -> None:
        """
        Appends a string array record to the log.
        
        :param entry:     Entry index, as returned by Start()
        :param arr:       String array to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def finish(self, entry: int, timestamp: int = 0) -> None:
        """
        Finish an entry.
        
        :param entry:     Entry index
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def flush(self) -> None:
        """
        Explicitly flushes the log data to disk.
        """
    def hasSchema(self, name: str) -> bool:
        """
        Returns whether there is a data schema already registered with the given
        name.
        
        :param name: Name (the string passed as the data type for records using this
                     schema)
        
        :returns: True if schema already registered
        """
    def pause(self) -> None:
        """
        Pauses appending of data records to the log.  While paused, no data records
        are saved (e.g. AppendX is a no-op).  Has no effect on entry starts /
        finishes / metadata changes.
        """
    def resume(self) -> None:
        """
        Resumes appending of data records to the log.
        """
    def setMetadata(self, entry: int, metadata: str, timestamp: int = 0) -> None:
        """
        Updates the metadata for an entry.
        
        :param entry:     Entry index
        :param metadata:  New metadata for the entry
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def start(self, name: str, type: str, metadata: str = '', timestamp: int = 0) -> int:
        """
        Start an entry.  Duplicate names are allowed (with the same type), and
        result in the same index being returned (Start/Finish are reference
        counted).  A duplicate name with a different type will result in an error
        message being printed to the console and 0 being returned (which will be
        ignored by the Append functions).
        
        :param name:      Name
        :param type:      Data type
        :param metadata:  Initial metadata (e.g. data properties)
        :param timestamp: Time stamp (may be 0 to indicate now)
        
        :returns: Entry index
        """
    def stop(self) -> None:
        """
        Stops appending start/metadata/schema records to the log.
        """
class DataLogEntry:
    """
    Log entry base class.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def finish(self, timestamp: int = 0) -> None:
        """
        Finishes the entry.
        
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def setMetadata(self, metadata: str, timestamp: int = 0) -> None:
        """
        Updates the metadata for the entry.
        
        :param metadata:  New metadata for the entry
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class DataLogReader:
    """
    Data log reader (reads logs written by the DataLog class).
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, filename: str) -> None:
        ...
    @typing.overload
    def __init__(self, buffer: typing_extensions.Buffer, name: str = '') -> None:
        ...
    def __iter__(self) -> typing.Iterator[DataLogRecord]:
        ...
    def getBufferIdentifier(self) -> str:
        """
        Gets the buffer identifier, typically the filename.
        
        :returns: Identifier string
        """
    def getExtraHeader(self) -> str:
        """
        Gets the extra header data.
        
        :returns: Extra header data
        """
    def getVersion(self) -> int:
        """
        Gets the data log version. Returns 0 if data log is invalid.
        
        :returns: Version number; most significant byte is major, least significant
                  is minor (so version 1.0 will be 0x0100)
        """
    def isValid(self) -> bool:
        """
        Returns true if the data log is valid (e.g. has a valid header).
        """
class DataLogRecord:
    """
    A record in the data log. May represent either a control record (entry == 0)
    or a data record. Used only for reading (e.g. with DataLogReader).
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getBoolean(self) -> bool:
        """
        Decodes a data record as a boolean. Note if the data type (as indicated in
        the corresponding start control record for this entry) is not "boolean",
        invalid results may be returned or TypeError will be raised.
        """
    def getBooleanArray(self) -> list:
        """
        Decodes a data record as a boolean array. Note if the data type (as
        indicated in the corresponding start control record for this entry) is not
        "boolean[]", invalid results may be returned or a TypeError may be raised.
        """
    def getDouble(self) -> float:
        """
        Decodes a data record as a double. Note if the data type (as indicated in
        the corresponding start control record for this entry) is not "double",
        invalid results may be returned or TypeError will be raised.
        """
    def getDoubleArray(self) -> list[float]:
        """
        Decodes a data record as a double array. Note if the data type (as
        indicated in the corresponding start control record for this entry) is not
        "double[]", invalid results may be returned or a TypeError may be raised.
        """
    def getEntry(self) -> int:
        """
        Gets the entry ID.
        
        :returns: entry ID
        """
    def getFinishEntry(self) -> int:
        """
        Decodes a finish control record. Raises TypeError on error.
        """
    def getFloat(self) -> float:
        """
        Decodes a data record as a float. Note if the data type (as indicated in
        the corresponding start control record for this entry) is not "float",
        invalid results may be returned or TypeError will be raised.
        """
    def getFloatArray(self) -> list[float]:
        """
        Decodes a data record as a float array. Note if the data type (as
        indicated in the corresponding start control record for this entry) is not
        "float[]", invalid results may be returned or a TypeError may be raised.
        """
    def getInteger(self) -> int:
        """
        Decodes a data record as an integer. Note if the data type (as indicated in
        the corresponding start control record for this entry) is not "int64",
        invalid results may be returned or TypeError will be raised.
        """
    def getIntegerArray(self) -> list[int]:
        """
        Decodes a data record as an integer array. Note if the data type (as
        indicated in the corresponding start control record for this entry) is not
        "int64[]", invalid results may be returned or a TypeError may be raised.
        """
    def getRaw(self) -> bytes:
        """
        Gets the raw data. Use the GetX functions to decode based on the data type
        in the entry's start record.
        """
    def getSetMetadataData(self) -> MetadataRecordData:
        """
        Decodes a set metadata control record. Raises TypeError on error.
        """
    def getSize(self) -> int:
        """
        Gets the size of the raw data.
        
        :returns: size
        """
    def getStartData(self) -> StartRecordData:
        """
        Decodes a start control record. Raises TypeError on error.
        """
    def getString(self) -> str:
        """
        Decodes a data record as a string. Note if the data type (as indicated in
        the corresponding start control record for this entry) is not "string",
        invalid results may be returned or TypeError will be raised.
        """
    def getStringArray(self) -> list[str]:
        """
        Decodes a data record as a string array. Note if the data type (as
        indicated in the corresponding start control record for this entry) is not
        "string[]", invalid results may be returned or a TypeError may be raised.
        """
    def getTimestamp(self) -> int:
        """
        Gets the record timestamp.
        
        :returns: Timestamp, in integer microseconds
        """
    def isControl(self) -> bool:
        """
        Returns true if the record is a control record.
        
        :returns: True if control record, false if normal data record.
        """
    def isFinish(self) -> bool:
        """
        Returns true if the record is a finish control record. Use GetFinishEntry()
        to decode the contents.
        
        :returns: True if finish control record, false otherwise.
        """
    def isSetMetadata(self) -> bool:
        """
        Returns true if the record is a set metadata control record. Use
        GetSetMetadataData() to decode the contents.
        
        :returns: True if set metadata control record, false otherwise.
        """
    def isStart(self) -> bool:
        """
        Returns true if the record is a start control record. Use GetStartData()
        to decode the contents.
        
        :returns: True if start control record, false otherwise.
        """
class DoubleArrayLogEntry(_DoubleArrayLogEntryImpl):
    """
    Log array of double values.
    """
    kDataType: typing.ClassVar[str] = 'double[]'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, arr: list[float], timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, arr: list[float], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class DoubleLogEntry(_DoubleLogEntryImpl):
    """
    Log double values.
    """
    kDataType: typing.ClassVar[str] = 'double'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, value: float, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, value: float, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class FloatArrayLogEntry(_FloatArrayLogEntryImpl):
    """
    Log array of float values.
    """
    kDataType: typing.ClassVar[str] = 'float[]'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, arr: list[float], timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, arr: list[float], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class FloatLogEntry(_FloatLogEntryImpl):
    """
    Log float values.
    """
    kDataType: typing.ClassVar[str] = 'float'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, value: float, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, value: float, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class IntegerArrayLogEntry(_IntegerArrayLogEntryImpl):
    """
    Log array of integer values.
    """
    kDataType: typing.ClassVar[str] = 'int64[]'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, arr: list[int], timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, arr: list[int], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class IntegerLogEntry(_IntegerLogEntryImpl):
    """
    Log integer values.
    """
    kDataType: typing.ClassVar[str] = 'int64'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, value: int, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, value: int, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class MetadataRecordData:
    """
    Data contained in a set metadata control record as created by
    DataLog::SetMetadata(). This can be read by calling
    DataLogRecord::GetSetMetadataData().
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def entry(self) -> int:
        """
        Entry ID.
        """
    @property
    def metadata(self) -> str:
        """
        New metadata for the entry.
        """
class RawLogEntry(_RawLogEntryImpl):
    """
    Log arbitrary byte data.
    """
    kDataType: typing.ClassVar[str] = 'raw'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, type: str, timestamp: int = 0) -> None:
        ...
    def append(self, data: typing_extensions.Buffer, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param data:      Data to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, data: typing_extensions.Buffer, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param data:      Data to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class StartRecordData:
    """
    Data contained in a start control record as created by DataLog::Start() when
    writing the log. This can be read by calling DataLogRecord::GetStartData().
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def __repr__(self) -> str:
        ...
    @property
    def entry(self) -> int:
        """
        Entry ID; this will be used for this entry in future records.
        """
    @property
    def metadata(self) -> str:
        """
        Initial metadata.
        """
    @property
    def name(self) -> str:
        """
        Entry name.
        """
    @property
    def type(self) -> str:
        """
        Type of the stored data for this entry, as a string, e.g. "double".
        """
class StringArrayLogEntry(_StringArrayLogEntryImpl):
    """
    Log array of string values.
    """
    kDataType: typing.ClassVar[str] = 'string[]'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    def append(self, arr: list[str], timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, arr: list[str], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param arr:       Values to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class StringLogEntry(_StringLogEntryImpl):
    """
    Log string values.
    """
    kDataType: typing.ClassVar[str] = 'string'
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, type: str, timestamp: int = 0) -> None:
        ...
    def append(self, value: str, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def update(self, value: str, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param value:     Value to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class StructArrayLogEntry(DataLogEntry):
    """
    Log raw struct serializable array of objects.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, type: type, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, type: type, timestamp: int = 0) -> None:
        ...
    def append(self, data: list[typing.Any], timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param data:      Data to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def getLastValue(self) -> list[typing.Any] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
    def update(self, data: list[typing.Any], timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param data:      Data to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class StructLogEntry(DataLogEntry):
    """
    Log raw struct serializable objects.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, type: type, timestamp: int = 0) -> None:
        ...
    @typing.overload
    def __init__(self, log: DataLog, name: str, metadata: str, type: type, timestamp: int = 0) -> None:
        ...
    def append(self, data: typing.Any, timestamp: int = 0) -> None:
        """
        Appends a record to the log.
        
        :param data:      Data to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
    def getLastValue(self) -> typing.Any | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
    def update(self, data: typing.Any, timestamp: int = 0) -> None:
        """
        Updates the last value and appends a record to the log if it has changed.
        
        .. note:: The last value is local to this class instance; using Update() with
           two instances pointing to the same underlying log entry name will likely
           result in unexpected results.
        
        :param data:      Data to record
        :param timestamp: Time stamp (may be 0 to indicate now)
        """
class _BooleanArrayLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> list[int] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _BooleanLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> bool | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _DoubleArrayLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> list[float] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _DoubleLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> float | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _FloatArrayLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> list[float] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _FloatLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> float | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _IntegerArrayLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> list[int] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _IntegerLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> int | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _RawLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> list[int] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _StringArrayLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> list[str] | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
class _StringLogEntryImpl(DataLogEntry):
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def getLastValue(self) -> str | None:
        """
        Gets the last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: Last value (empty if no last value)
        """
    def hasLastValue(self) -> bool:
        """
        Gets whether there is a last value.
        
        .. note:: The last value is local to this class instance and updated only with
           Update(), not Append().
        
        :returns: True if last value exists, false otherwise.
        """
