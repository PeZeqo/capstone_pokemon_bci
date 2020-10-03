import arcade
import os
import random
from project_constants import SCREEN_WIDTH, SCREEN_HEIGHT, FREQUENCY, GRID_HEIGHT, SCORE_BOARD_HEIGHT, PATTERN_LENGTH
import time
import sdl2
from PIL import Image
from pyboy import PyBoy
import arcade

# Class for the testing window
class game_draw(arcade.Window):
    screen_width = None
    screen_height = None
    board_width = None
    board_height = None
    key_presses = {}
    texture_list = []
    flicker_frequency = []
    tick = 0
    score_list = []
    pyboy = None
    bot_sup = None
    scrn = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.screen_width = width
        self.screen_height = height
        self.set_update_rate(1/FREQUENCY)

    def setup(self):
        arcade.set_background_color(arcade.color.WHITE)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        rom_dir = os.path.join(dir_path, 'roms')
        self.pyboy = PyBoy(os.path.join(rom_dir, 'Pokemon.gb'))

        self.bot_sup = self.pyboy.botsupport_manager()
        self.scrn = self.bot_sup.screen()

    def on_update(self, delta_time):
        self.pyboy.tick()
        self.on_draw()
        self.tick += 1

    def draw_board(self):
        screen_colors = self.scrn.screen_ndarray()
        img = Image.fromarray(screen_colors)
        texture = arcade.Texture("img", img)
        arcade.draw_scaled_texture_rectangle(self.width / 2, self.height / 2, texture, 5.0)

    def on_draw(self):
        # Start the render process. This must be done before any drawing commands.
        arcade.start_render()

        # Draw grid
        self.draw_board()

        # Finish the render.
        # Nothing will be drawn without this.
        # Must happen after all draw commands
        arcade.finish_render()

    def main():
        game = game_draw(160 * 5, 144 * 5, "Game Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    # pyboy = PyBoy('Pokemon.gb')
    # while not pyboy.tick():
    #     pass
    game_draw.main()
