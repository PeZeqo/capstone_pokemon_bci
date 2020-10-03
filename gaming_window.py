import arcade
import os
import random
from project_constants import FREQUENCY, PATTERN_LENGTH, GAME_SCALE, GAME_HEIGHT, GAME_WIDTH, CHECKERBOARD_SIZE
import sdl2
from PIL import Image
from pyboy import PyBoy
from pyboy.utils import WindowEvent
import arcade

# Class for the testing window
class gaming_window(arcade.Window):
    screen_width = None
    screen_height = None
    game_width = None
    game_height = None
    texture_list = []
    flicker_frequency = []
    tick = 0
    last_state = []
    checkerboard_pos_list = []
    pyboy = None
    bot_sup = None
    scrn = None

    def __init__(self, width, height, title):
        self.game_width = width * GAME_SCALE
        self.game_height = height * GAME_SCALE
        self.screen_width = self.game_width + CHECKERBOARD_SIZE * 2
        self.screen_height = self.game_height + CHECKERBOARD_SIZE * 2
        super().__init__(self.screen_width, self.screen_height, title)
        self.set_update_rate(1/FREQUENCY)

    def setup(self):
        # Set flicker frequencies for each quadrant
        off_bits = int(PATTERN_LENGTH / 3)
        sample_list = [1] * (PATTERN_LENGTH - off_bits) + [0] * off_bits
        for x in range(4):
            self.flicker_frequency.append(random.sample(sample_list, len(sample_list)))

        # load textures
        self.load_checkerboards()

        # set all checkerboards to normal state
        self.last_state = [0] * 4

        # Prep x,y pairs for where to print icons
        for x in [128, self.screen_width - 128]:
            for y in [128, self.screen_height - 128]:
                self.checkerboard_pos_list.append([x, y])

        # load rom through PyBoy
        dir_path = os.path.dirname(os.path.realpath(__file__))
        rom_dir = os.path.join(dir_path, 'roms')
        self.pyboy = PyBoy(os.path.join(rom_dir, 'Pokemon.gb'))

        # set up PyBoy screen support
        self.bot_sup = self.pyboy.botsupport_manager()
        self.scrn = self.bot_sup.screen()

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

    def on_update(self, delta_time):
        self.pyboy.tick()
        self.on_draw()
        self.tick += 1

    def draw_checkerboards(self):
        # Load and draw all icons
        for ind, last_state in enumerate(self.last_state):
            freq = self.flicker_frequency[ind]
            pos = self.checkerboard_pos_list[ind]
            scale = 1
            texture = self.texture_list[last_state]

            # if self.tick % freq == 0 and self.tick != 0:
            if freq[self.tick % PATTERN_LENGTH]:
                self.last_state[ind] = not last_state

            arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, scale, 0)

    def draw_board(self):
        screen_colors = self.scrn.screen_ndarray()
        img = Image.fromarray(screen_colors)
        texture = arcade.Texture("img", img)
        arcade.draw_scaled_texture_rectangle(self.width / 2, self.height / 2, texture, GAME_SCALE)

    def on_draw(self):
        # Start the render process. This must be done before any drawing commands.
        arcade.start_render()

        # Draw grid
        self.draw_board()
        self.draw_checkerboards()

        # Finish the render.
        # Nothing will be drawn without this.
        # Must happen after all draw commands
        arcade.finish_render()

    def on_key_press(self, key, key_modifiers):
        actions = []
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

        if actions:
            for action in actions:
                self.pyboy.send_input(WindowEvent(action))
                self.pyboy.tick()

    def main():
        game = gaming_window(GAME_WIDTH, GAME_HEIGHT, "Game Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    gaming_window.main()
