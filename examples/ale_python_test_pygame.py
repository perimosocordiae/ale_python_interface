#!/usr/bin/env python

# ale_python_test_pygame.py
# Author: Ben Goodrich
#
# This modified ale_python_test1.py to display screen contents using pygame
import sys
from ale_python_interface import ALEInterface
import numpy as np
import pygame

if(len(sys.argv) < 2):
    print("Usage ./ale_python_test_pygame.py <ROM_FILE_NAME>")
    sys.exit()

ale = ALEInterface(sys.argv[1])

max_frames_per_episode = ale["max_num_frames_per_episode"]
ale["random_seed"] = 123

random_seed = ale["random_seed"]
print("random_seed: " + str(random_seed))

legal_actions = ale.minimal_actions

print("width/height: %s/%s" % ale.screen_dims)

#init pygame
pygame.init()
screen = pygame.display.set_mode(ale.screen_dims)
pygame.display.set_caption("Arcade Learning Environment Random Agent Display")

pygame.display.flip()

episode = 0
total_reward = 0.0
while episode < 10:
    exit = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit=True
            break
    if exit:
        break

    a = np.random.choice(legal_actions)
    reward = ale.act(a)
    total_reward += reward

    numpy_surface = np.frombuffer(screen.get_buffer(),dtype=np.int32)
    ale.fill_screen_rgb(numpy_surface)
    pygame.display.flip()
    if ale.is_game_over:
        episode_frame_number = ale.episode_frame_number
        frame_number = ale.frame_number
        print("Frame Number: %d Episode Frame Number: %d" % (
              frame_number, episode_frame_number))
        print("Episode %d ended with score: %g" % (episode, total_reward))
        ale.reset_game()
        total_reward = 0.0
        episode += 1
