#!/usr/bin/env python

# ale_python_test1.py
# Author: Ben Goodrich
#
# This is a direct port to python of the shared library example from ALE provided in
# doc/examples/sharedLibraryInterfaceExample.cpp

import sys
from ale_python_interface import ALEInterface
import numpy as np

if(len(sys.argv) < 2):
    print("Usage ./ale_python_test1.py <ROM_FILE_NAME>")
    sys.exit()

ale = ALEInterface(sys.argv[1])

max_frames_per_episode = ale["max_num_frames_per_episode"]
ale["random_seed"] = 123

random_seed = ale["random_seed"]
print("random_seed: " + str(random_seed))

legal_actions = ale.legal_actions

for episode in range(10):
    total_reward = 0.0
    while not ale.is_game_over:
        a = np.random.choice(legal_actions)
        reward = ale.act(a)
        total_reward += reward
    print("Episode " + str(episode) + " ended with score: " + str(total_reward))
    ale.reset_game()
