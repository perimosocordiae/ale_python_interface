# ale_python_interface.py
# Author: Ben Goodrich
# This directly implements a python version of the arcade learning environment interface.
# It requires the C wrapper library to be built and on shared object path, as "ale_c_wrapper.so"

from ctypes import cdll
import numpy as np
from numpy.ctypeslib import as_ctypes
import os

__all__ = ['ALEInterface']

ale_lib = cdll.LoadLibrary(os.path.join(os.path.dirname(__file__),
                                        'ale_c_wrapper.so'))

# Properties taken from Arcade-Learning-Environment/src/common/Defaults.cpp
PROPS = {
    'random_seed': str,
    'game_controller': str,
    'player_agent': str,
    'max_num_episodes': int,
    'max_num_frames': int,
    'max_num_frames_per_episode': int,
    'system_reset_steps': int,
    'record_trajectory': bool,
    'restricted_action_set': bool,
    'use_starting_actions': bool,
    'use_environment_distribution': bool,
    'random_seed': str,
    'disable_color_averaging': bool,
    'send_rgb': bool,
    'frame_skip': int,
    'display_screen': bool,
}
GETTERS = {
    str: ale_lib.getString,
    int: ale_lib.getInt,
    bool: ale_lib.getBool,
    float: ale_lib.getFloat,
}
SETTERS = {
    str: ale_lib.setString,
    int: ale_lib.setInt,
    bool: ale_lib.setBool,
    float: ale_lib.setFloat,
}


class ALEInterface(object):
    def __init__(self, rom_file):
        self._obj = ale_lib.ALE_new()
        ale_lib.loadROM(self._obj, rom_file)

    def __del__(self):
        ale_lib.ALE_del(self._obj)

    def __getitem__(self, key):
        if key not in PROPS:
            raise ValueError('Invalid key: %s' % key)
        getter = GETTERS[PROPS[key]]
        return getter(self._obj, key)

    def __setitem__(self, key, value):
        if key not in PROPS:
            raise ValueError('Invalid key: %s' % key)
        setter = SETTERS[PROPS[key]]
        setter(self._obj, key, value)

    @property
    def legal_actions(self):
        act_size = ale_lib.getLegalActionSize(self._obj)
        act = np.zeros(act_size, dtype=np.int32)
        ale_lib.getLegalActionSet(self._obj, as_ctypes(act))
        return act

    @property
    def minimal_actions(self):
        act_size = ale_lib.getMinimalActionSize(self._obj)
        act = np.zeros(act_size, dtype=np.int32)
        ale_lib.getMinimalActionSet(self._obj, as_ctypes(act))
        return act

    @property
    def frame_number(self):
        return ale_lib.getFrameNumber(self._obj)

    @property
    def episode_frame_number(self):
        return ale_lib.getEpisodeFrameNumber(self._obj)

    @property
    def screen_dims(self):
        """returns a tuple that contains (screen_width,screen_height)
        """
        width = ale_lib.getScreenWidth(self._obj)
        height = ale_lib.getScreenHeight(self._obj)
        return width, height

    @property
    def ram_size(self):
        return ale_lib.getRAMSize(self._obj)

    @property
    def is_game_over(self):
        return ale_lib.game_over(self._obj)

    def act(self,action):
        return ale_lib.act(self._obj, int(action))

    def reset_game(self):
        ale_lib.reset_game(self._obj)

    def fill_screen(self, screen_data=None):
        """This function fills screen_data with the RAW Pixel data
        screen_data MUST be a numpy array of uint8.
        Note: This is the raw pixel values from the atari,
        before any RGB palette transformation takes place.
        """
        if screen_data is None:
            size = np.prod(self.screen_dims)
            screen_data = np.zeros(size, dtype=np.uint8)
        ale_lib.getScreen(self._obj, as_ctypes(screen_data))
        return screen_data

    def fill_screen_rgb(self, screen_data=None):
        """This function fills screen_data with the data
        screen_data MUST be a numpy array of uint32.
        """
        if screen_data is None:
            size = np.prod(self.screen_dims)
            screen_data = np.zeros(size, dtype=np.uint32)
        ale_lib.getScreenRGB(self._obj, as_ctypes(screen_data))
        return screen_data

    def fill_ram(self, ram=None):
        """This function grabs the atari RAM.
        ram MUST be a numpy array of uint8.
        """
        if ram is None:
            ram = np.zeros(self.ram_size, dtype=np.uint8)
        ale_lib.getRAM(self._obj,as_ctypes(ram))
        return ram
