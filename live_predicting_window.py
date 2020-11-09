# live predicting window, and import csv as user input
# arrow should point to the correct input
# TODO: perhaps a square around the chosen input 
# used some parts from data_collection_window, command_handler, gaming_window

import os
import arcade
from project_constants import FREQUENCY, PATTERN_LENGTH, PADDING, BASE_HEIGHT, BASE_WIDTH, ARROW_SIZE, ARROW_SCALE, \
	CHECKERBOARD_SIZE, RECORDINGS_PER_ICON, SECONDS_PER_RECORDING, COMMAND_SEND_FREQUENCY
import pandas as pd
import numpy as np
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import sdl2
from command_handler import command_handler
from cca_train import cca_handler
import ctypes
import time
import re


class live_predicting_window(arcade.Window):

	# screen and image size vars
	screen_width = None
	screen_height = None
	checkerboard_size = CHECKERBOARD_SIZE
	arrow_size = ARROW_SIZE * ARROW_SCALE
	padding = PADDING

	# textures and frequencies vars
	texture_list = []
	arrow_textures = []
	flicker_frequency = []
	last_state = []
	checkerboard_pos_list = []
	draw_scale = None
	tick = 0
	selected_arrow = 0

	# recording control vars
	currently_recording = False


	# data collection vars
	generator = None
	# recording data is imported from csv
	recording_data = []

	# length of recording data
	record_length = None

	# row number index
	row_index = 0
	channels = ['P7', 'O1', 'O2', 'P8']

	# ML vars
	command_handler = None

	def __init__(self, width, height, title, recording_name='recordings/first_target_0.csv'):
		# set total screen size since we also need space to draw checkerboards
		self.screen_width = self.arrow_size + CHECKERBOARD_SIZE * 2 + PADDING
		self.screen_height = self.arrow_size + CHECKERBOARD_SIZE * 2 + PADDING

		self.draw_scale = self.screen_height / BASE_HEIGHT

		# let Arcade Window run it's setup
		super().__init__(self.screen_width, self.screen_height, title, resizable=True)

		# set frame rate as (1 / desired_frame_rate)
		self.set_update_rate(1/FREQUENCY)

		# set recording name
		self.recording_name = recording_name
		# set arrow target - assume target num is in the name - select first number in filename
		self.target = int(re.findall(r'\d+|$', self.recording_name)[0])
		print('Choose target {}'.format(self.target))

		# import
		self.import_recording()

	def print_stage(self, stage):
		print('-'*20)
		print('{} BEGINNING'.format(stage))
		print('-'*20)

	def setup(self):
		self.print_stage("VISUALS SETUP")
		self.setup_checkerboards()
		self.load_arrows()
		self.print_stage("PYBOY SETUP")
		self.setup_pyboy()
		self.print_stage("COMMAND HANDLER SETUP")
		self.setup_command_handler()

	def setup_command_handler(self):
		# choose the desired command handler
		self.command_handler = cca_handler()

	def setup_checkerboards(self):
		# load textures
		self.load_checkerboards()

		self.resize_drawing_vars()

		self.set_checkerboard_positions()

		# set all checkerboards to normal state (as opposed to inverted checkerboard)
		self.last_state = [0] * len(self.checkerboard_pos_list)

		# set flicker frequencies for each quadrant
		with open('flicker_patterns.txt') as f:
			for sequence in f:
				self.flicker_frequency.append(eval(sequence))


	def set_checkerboard_positions(self):
		# set some useful vars
		half_width = self.screen_width / 2
		half_height = self.screen_height / 2
		half_checkerboard = self.checkerboard_size / 2
		width_offset = (self.arrow_size / 2) + half_checkerboard + self.padding
		height_offset = (self.arrow_size / 2) + half_checkerboard + self.padding

		# empty checkerboard pos list
		self.checkerboard_pos_list = []

		# prep x,y pairs for where to print checkerboards
		for x in [half_width - width_offset, half_width, half_width + width_offset]:
			for y in [half_height - height_offset, half_height, half_height + height_offset]:
				# skip drawing in the middle of board
				if x == half_width and y == half_height:
					continue
				self.checkerboard_pos_list.append([x, y])

	def load_checkerboards(self):
		# Set up dir paths
		dir_path = os.path.dirname(os.path.realpath(__file__))
		image_dir = os.path.join(dir_path, 'images')
		checkerboard_dir = os.path.join(image_dir, 'checkerboards')
		icon_list = os.listdir(checkerboard_dir)

		# empty texture list, load new textures
		self.texture_list = []
		for icon in icon_list:
			if "png" not in icon.lower():
				continue
			self.texture_list.append(arcade.load_texture(os.path.join(checkerboard_dir, icon)))

	def setup_pyboy(self):
		# load rom through PyBoy
		dir_path = os.path.dirname(os.path.realpath(__file__))
		rom_dir = os.path.join(dir_path, 'roms')
		self.pyboy = PyBoy(os.path.join(rom_dir, 'Pokemon.gb'))

		# set up PyBoy screen support
		self.bot_sup = self.pyboy.botsupport_manager()
		self.scrn = self.bot_sup.screen()

		# minimize PyBoy window
		pyboy_handle = ctypes.windll.user32.FindWindowW(None, "PyBoy")
		ctypes.windll.user32.ShowWindow(pyboy_handle, 6)

	def load_arrows(self):
		# Set up dir paths
		dir_path = os.path.dirname(os.path.realpath(__file__))
		image_dir = os.path.join(dir_path, 'images')
		arrow_dir = os.path.join(image_dir, 'arrows')
		icon_list = os.listdir(arrow_dir)

		for icon in icon_list:
			if "png" not in icon.lower():
				continue
			self.arrow_textures.append(arcade.load_texture(os.path.join(arrow_dir, icon)))

	def on_update(self, delta_time):
		# check if done
		if self.row_index >= self.record_length:
			print('-'*20)
			print('Done reading file')
			print('-'*20)
			self.exit_window()
		self.pyboy.tick()
		self.on_draw()
		# self.exhaust()
		self.tick += 1
		self.tick %= FREQUENCY
		if self.tick % COMMAND_SEND_FREQUENCY == 0:
			start = time.time()
			self.command_handler.predict(self.get_eeg_data())
			# print("Guess done in: {}s".format(time.time() - start))
			self.row_index += 128

	# def exhaust(self):
	# 	next(self.generator)

	def get_eeg_data(self):
		# return np.asarray(list(next(self.generator).queue))
		# get 128 rows of recording_data
		return np.asarray(self.recording_data[self.channels][self.row_index:self.row_index + 128])


	def import_recording(self):
		# make sure name is ok
		if 'recordings/' not in self.recording_name:
			self.recording_name = 'recordings/' + self.recording_name
		if '.csv' not in self.recording_name:
			self.recording_name += '.csv'
		self.recording_data = pd.read_csv(self.recording_name)
		self.record_length = len(self.recording_data.index)

	def resize_drawing_vars(self):
		if self.screen_height <= self.screen_width:
			self.draw_scale = self.screen_height / BASE_HEIGHT
		else:
			self.draw_scale = self.screen_width / BASE_WIDTH
		self.checkerboard_size = CHECKERBOARD_SIZE * self.draw_scale
		self.arrow_size = ARROW_SIZE * ARROW_SCALE * self.draw_scale
		self.arrow_size = ARROW_SIZE * ARROW_SCALE * self.draw_scale
		self.padding = PADDING * self.draw_scale

	def on_resize(self, width, height):
		""" This method is automatically called when the window is resized. """

		# Call the parent. Failing to do this will mess up the coordinates, and default to 0,0 at the center and the
		# edges being -1 to 1.
		super().on_resize(width, height)

		self.screen_width = width
		self.screen_height = height

		self.resize_drawing_vars()

		self.set_checkerboard_positions()

	def on_draw(self):
		# Start the render process
		arcade.start_render()

		# Draw game
		self.draw_arrow()
		self.draw_timer()

		# Draw checkerboards
		self.draw_checkerboards()

		# Finish the render
		arcade.finish_render()

	def draw_arrow(self):
		arcade.draw_scaled_texture_rectangle(self.width / 2, self.height / 2, self.arrow_textures[self.target],
											 ARROW_SCALE * self.draw_scale)

	def draw_timer(self):
		arcade.draw_text("Timer: " + str(round(self.tick / FREQUENCY, 2)), (self.width / 2) - (PADDING * 1.2) * self.draw_scale,
						 (self.height) / 2 - (PADDING * self.draw_scale), arcade.color.WHITE,
						 40 * self.draw_scale)

	def draw_checkerboards(self):
		# Load and draw all checkerboards
		for ind, last_state in enumerate(self.last_state):
			freq = self.flicker_frequency[ind]
			pos = self.checkerboard_pos_list[ind]
			texture = self.texture_list[last_state]

			# if this is a switch state, change checkerboard state:
			if freq[self.tick % len(freq)]:
				self.last_state[ind] = not last_state

			arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, self.draw_scale, 0)

	def on_key_press(self, key, key_modifiers):
		actions = []
		print("KEY PRESSED: {}".format(key))

		# switch statement to create WindowEvents (button commands for PyBoy)
		if (key == arcade.key.UP):
			actions = [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP]
		elif (key == arcade.key.DOWN):
			actions = [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN]
		elif (key == arcade.key.LEFT):
			actions = [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT]
		elif (key == arcade.key.RIGHT):
			actions = [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT]
		elif (key == arcade.key.Z):
			actions = [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]
		elif (key == arcade.key.X):
			actions = [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A]
		elif (key == arcade.key.ENTER):
			actions = [WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT]
		elif (key == arcade.key.RSHIFT):
			actions = [WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START]

		# if actions list isn't empty, send commands to pyboy and tick the pyboy window to process each command
		if actions:
			for action in actions:
				self.pyboy.send_input(WindowEvent(action))
				self.pyboy.tick()

	def exit_window(self):
		exit()

	def main():
		# width, height, title, recording_name
		window = live_predicting_window(0, 0, "Live Predicting Window", 'recordings/first_target_1')
		window.setup()
		arcade.run()


if __name__ == "__main__":
	live_predicting_window.main()