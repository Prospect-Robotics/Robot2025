"""
Class for running Orchestra with devices
"""

"""
Copyright (C) Cross The Road Electronics.  All rights reserved.
License information can be found in CTRE_LICENSE.txt
For support and suggestions contact support@ctr-electronics.com or file
an issue tracker at https://github.com/CrossTheRoadElec/Phoenix-Releases
"""

import ctypes
from phoenix6.hardware.parent_device import ParentDevice
from phoenix6.units import second
from phoenix6.status_code import StatusCode
from phoenix6.phoenix_native import Native

class Orchestra:
    """
    Orchestra is used to play music through devices. It uses a "Chirp" (.chrp) music
    file that can be generated using Phoenix Tuner. Chirp files are generated from
    standard MIDI files.

    Any Chirp file located in the src/main/deploy directory of your FRC project will
    automatically be copied to the roboRIO on code deploy.

    Unless AudioConfigs.allow_music_dur_disable is enabled, the robot must be enabled
    to play music. Additionally, devices playing in Orchestra will not run any other
    control requests while Orchestra is running. Users can :ref:pause: or :ref:stop:
    the Orchestra to re-enable device control.

    Each device can only play a single track within the music file. For multi-track
    files, multiple devices are needed. Devices can be added with an explicit track
    number. Otherwise, the first track will be played through the first Talon FX added,
    the second track will be played through the second Talon FX added, etc.

    To use Orchestra:

    - Add the Talon FXs to be used as instruments using :ref:add_instrument:.
    - Load the Chirp file to be played using :ref:load_music:. This can also
    be done in the Orchestra constructor.

    Both of these can also be done in the Orchestra constructor.

    Once ready, the Orchestra can be controlled using :ref:play:/:ref:pause:/:ref:stop:.
    New music files can be loaded at any time.

    :param instruments: A list of devices that will be used as instruments in the orchestra
    :type instruments: list[ParentDevice]
    :param filepath: The path to the music file to immediately load into the orchestra.
                     The API is blocking on the file read.
    :type filepath: str
    """

    def __init__(self, instruments: list[ParentDevice] = [], filepath: str = ""):
        id = ctypes.c_uint16()
        Native.instance().c_ctre_phoenix6_orchestra_Create(ctypes.byref(id))
        self.__id = id.value

        for instrument in instruments:
            self.add_instrument(instrument)

        if len(filepath) > 0:
            self.load_music(filepath)

    def __enter__(self) -> 'Orchestra':
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        """
        Closes this Orchestra instance.
        """
        Native.instance().c_ctre_phoenix6_orchestra_Close(self.__id)
        self.__id = 0

    def add_instrument(self, instrument: ParentDevice) -> StatusCode:
        """
        Adds an instrument to the orchestra.

        This adds the instrument to the next track; it does not wrap
        back to track 0 if all tracks have been filled. To assign
        multiple instruments to a track, use add_instrument_with_track.

        :param instrument: The device to add to the orchestra
        :type instrument: ParentDevice
        :returns: Status code of adding the device
        :rtype: StatusCode
        """
        c_network = ctypes.c_char_p(bytes(instrument.network, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_AddDevice(self.__id, c_network, instrument.device_hash))

    def add_instrument_with_track(self, instrument: ParentDevice, track_number: int) -> StatusCode:
        """
        Adds an instrument to the orchestra on the given track.

        This can be used to assign multiple instruments to a track.
        
        :param instrument: The device to add to the orchestra
        :type instrument: ParentDevice
        :param track_number: The track number the device should play, starting at 0
        :type track_number: int
        :returns: Status code of adding the device
        :rtype: StatusCode
        """
        c_network = ctypes.c_char_p(bytes(instrument.network, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_AddDeviceWithTrack(self.__id, c_network, instrument.device_hash, track_number))

    def clear_instruments(self) -> StatusCode:
        """
        Clears all instruments in the orchestra.
        
        :returns: Status code of clearing all devices
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_ClearDevices(self.__id))

    def load_music(self, filepath: str) -> StatusCode:
        """
        Loads a Chirp file at the specified file path.

        If the Chirp file is inside your "src/main/deploy" directory, it will be
        automatically deployed to a default directory on the roboRIO when you
        deploy code. For these files, the name and file extension is sufficient.

        A Chirp file can be created from a MIDI file using Phoenix Tuner.

        This API is blocking on the file read.

        :param filepath: The path to the Chirp file
        :type filepath: str
        :returns: Status code of loading the Chirp file
        :rtype: StatusCode
        """
        c_filepath = ctypes.c_char_p(bytes(filepath, 'utf-8'))
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_LoadMusic(self.__id, c_filepath))

    def play(self) -> StatusCode:
        """
        Plays the loaded music file. If the player is paused, this will resume
        the orchestra.

        :returns: Status code of playing the orchestra
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_Play(self.__id))

    def pause(self) -> StatusCode:
        """
        Pauses the loaded music file. This saves the current position in the
        track so it can be resumed later.

        :returns: Status code of pausing the orchestra
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_Pause(self.__id))

    def stop(self) -> StatusCode:
        """
        Stops the loaded music file. This resets the current position in the
        track to the start.

        :returns: Status code of stopping the orchestra
        :rtype: StatusCode
        """
        return StatusCode(Native.instance().c_ctre_phoenix6_orchestra_Stop(self.__id))

    def is_playing(self) -> bool:
        """
        Gets whether the current track is actively playing.

        :returns: True if Orchestra is playing the music file
        :rtype: bool
        """
        is_playing = ctypes.c_int()
        Native.instance().c_ctre_phoenix6_orchestra_IsPlaying(self.__id, ctypes.byref(is_playing))
        return is_playing.value != 0

    def get_current_time(self) -> second:
        """
        Gets the current timestamp of the music file. The timestamp will reset
        to zero whenever :ref:load_music: or :ref:stop: is called.

        If :ref:isPlaying: returns false, this method can be used to determine
        if the music is stopped or paused.

        :returns: The current timestamp of the music file, in seconds
        :rtype: second
        """
        time_seconds = ctypes.c_double()
        Native.instance().c_ctre_phoenix6_orchestra_GetCurrentTime(self.__id, ctypes.byref(time_seconds))
        return time_seconds.value
