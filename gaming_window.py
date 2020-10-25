import arcade
import os
import random
from project_constants import FREQUENCY, PATTERN_LENGTH, OFF_BITS, GAME_SCALE, \
    GAME_HEIGHT, GAME_WIDTH, CHECKERBOARD_SIZE, PADDING, BASE_HEIGHT, BASE_WIDTH
import sdl2
from PIL import Image
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import arcade
import ctypes
from command_handler import command_handler

# Class for the testing window
class gaming_window(arcade.Window):

    # screen and image size vars
    screen_width = None
    screen_height = None
    game_width = None
    game_height = None
    checkerboard_size = CHECKERBOARD_SIZE
    padding = PADDING

    # textures and frequencies vars
    texture_list = []
    flicker_frequency = []
    tick = 0
    last_state = []
    checkerboard_pos_list = []
    draw_scale = None

    # PyBoy vars
    pyboy = None
    bot_sup = None
    scrn = None

    def __init__(self, width, height, title):
        # scale the game width to make the game screen bigger
        self.game_width = GAME_WIDTH * GAME_SCALE
        self.game_height = GAME_HEIGHT * GAME_SCALE

        # set total screen size since we also need space to draw checkerboards
        self.screen_width = self.game_width + CHECKERBOARD_SIZE * 2 + PADDING
        self.screen_height = self.game_height + CHECKERBOARD_SIZE * 2 + PADDING

        self.draw_scale = self.screen_height / BASE_HEIGHT

        # let Arcade Window run it's setup
        super().__init__(self.screen_width, self.screen_height, title, resizable=True)

        # set frame rate as (1 / desired_frame_rate)
        self.set_update_rate(1/FREQUENCY)

    def setup(self):
        self.setup_checkerboards()
        self.setup_pyboy()

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
        width_offset = (self.game_width / 2) + half_checkerboard + self.padding
        height_offset = (self.game_height / 2) + half_checkerboard + self.padding

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

    def on_update(self, delta_time):
        self.pyboy.tick()
        self.on_draw()
        self.tick += 1
        self.tick %= FREQUENCY
        if self.tick == 0:
            command_handler([])

    def resize_drawing_vars(self):
        if self.screen_height <= self.screen_width:
            self.draw_scale = self.screen_height / BASE_HEIGHT
        else:
            self.draw_scale = self.screen_width / BASE_WIDTH
        self.checkerboard_size = CHECKERBOARD_SIZE * self.draw_scale
        self.game_width = GAME_WIDTH * GAME_SCALE * self.draw_scale
        self.game_height = GAME_HEIGHT * GAME_SCALE * self.draw_scale
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
        self.draw_game()

        # Draw checkerboards
        self.draw_checkerboards()

        # Finish the render
        arcade.finish_render()

    def draw_game(self):
        screen_colors = self.scrn.screen_ndarray()
        img = Image.fromarray(screen_colors)
        texture = arcade.Texture("img", img)
        arcade.draw_scaled_texture_rectangle(self.width / 2, self.height / 2, texture, GAME_SCALE * self.draw_scale)

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

    def main():
        game = gaming_window(0, 0, "Game Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    gaming_window.main()
