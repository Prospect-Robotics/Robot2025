from __future__ import annotations
import ntcore._ntcore
import typing
import wpimath.filter._filter
import wpimath.units
__all__ = ['BooleanEvent', 'EventLoop', 'NetworkBooleanEvent']
class BooleanEvent:
    """
    This class provides an easy way to link actions to active high logic signals.
    Each object represents a digital signal to which callback actions can be
    bound using :meth:`.IfHigh`.
    
    BooleanEvents can easily be composed for advanced functionality using
    {@link #operator&&}, {@link #operator||}, and {@link #operator!}.
    
    To get a new BooleanEvent that triggers when this one changes see {@link
    #Falling()} and :meth:`.Rising`.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, loop: EventLoop, signal: typing.Callable[[], bool]) -> None:
        """
        Creates a new event that is active when the condition is true.
        
        :param loop:   the loop that polls this event
        :param signal: the digital signal represented by this object.
        """
    def castTo(self, ctor: typing.Callable) -> typing.Any:
        """
        A method to "downcast" a BooleanEvent instance to a subclass (for example,
        to a command-based version of this class).
        
        :param ctor: a method reference to the constructor of the subclass that
                     accepts the loop as the first parameter and the condition/signal as the
                     second.
        
        :returns: an instance of the subclass.
        """
    def debounce(self, debounceTime: wpimath.units.seconds, type: wpimath.filter._filter.Debouncer.DebounceType = ...) -> BooleanEvent:
        """
        Creates a new debounced event from this event - it will become active when
        this event has been active for longer than the specified period.
        
        :param debounceTime: The debounce period.
        :param type:         The debounce type.
        
        :returns: The debounced event.
        """
    def falling(self) -> BooleanEvent:
        """
        Creates a new event that triggers when this one changes from true to false.
        
        :returns: the event.
        """
    def getAsBoolean(self) -> bool:
        """
        Returns the state of this signal (high or low) as of the last loop poll.
        
        :returns: true for the high state, false for the low state. If the event was
                  never polled, it returns the state at event construction.
        """
    def ifHigh(self, action: typing.Callable[[], None]) -> None:
        """
        Bind an action to this event.
        
        :param action: the action to run if this event is active.
        """
    def rising(self) -> BooleanEvent:
        """
        Creates a new event that triggers when this one changes from false to true.
        
        :returns: the new event.
        """
class EventLoop:
    """
    A declarative way to bind a set of actions to a loop and execute them when
    the loop is polled.
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self) -> None:
        ...
    def bind(self, action: typing.Callable[[], None]) -> None:
        """
        Bind a new action to run when the loop is polled.
        
        :param action: the action to run.
        """
    def clear(self) -> None:
        """
        Clear all bindings.
        """
    def poll(self) -> None:
        """
        Poll all bindings.
        """
class NetworkBooleanEvent(BooleanEvent):
    """
    A Button that uses a NetworkTable boolean field.
    
    This class is provided by the NewCommands VendorDep
    """
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self, loop: EventLoop, topic: ntcore._ntcore.BooleanTopic) -> None:
        """
        Creates a new event with the given boolean topic determining whether it is
        active.
        
        :param loop:  the loop that polls this event
        :param topic: The boolean topic that contains the value
        """
    @typing.overload
    def __init__(self, loop: EventLoop, sub: ntcore._ntcore.BooleanSubscriber) -> None:
        """
        Creates a new event with the given boolean subscriber determining whether
        it is active.
        
        :param loop: the loop that polls this event
        :param sub:  The boolean subscriber that provides the value
        """
    @typing.overload
    def __init__(self, loop: EventLoop, table: ntcore._ntcore.NetworkTable, topicName: str) -> None:
        """
        Creates a new event with the given boolean topic determining whether it is
        active.
        
        :param loop:      the loop that polls this event
        :param table:     The NetworkTable that contains the topic
        :param topicName: The topic name within the table that contains the value
        """
    @typing.overload
    def __init__(self, loop: EventLoop, tableName: str, topicName: str) -> None:
        """
        Creates a new event with the given boolean topic determining whether it is
        active.
        
        :param loop:      the loop that polls this event
        :param tableName: The NetworkTable name that contains the topic
        :param topicName: The topic name within the table that contains the value
        """
    @typing.overload
    def __init__(self, loop: EventLoop, inst: ntcore._ntcore.NetworkTableInstance, tableName: str, topicName: str) -> None:
        """
        Creates a new event with the given boolean topic determining whether it is
        active.
        
        :param loop:      the loop that polls this event
        :param inst:      The NetworkTable instance to use
        :param tableName: The NetworkTable that contains the topic
        :param topicName: The topic name within the table that contains the value
        """
