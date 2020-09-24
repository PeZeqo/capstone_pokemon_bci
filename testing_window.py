import arcade
import os
import random
from project_constants import SCREEN_WIDTH, SCREEN_HEIGHT, FREQUENCY, GRID_HEIGHT, SCORE_BOARD_HEIGHT, PATTERN_LENGTH


# Class for the testing window
class testing_window(arcade.Window):
    screen_width = None
    screen_height = None
    board_width = None
    board_height = None
    key_presses = {}
    texture_list = []
    flicker_frequency = []
    tick = 0
    score_list = []

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.screen_width = width
        self.screen_height = height
        self.set_update_rate(1/FREQUENCY)

    def setup(self):
        for direction in ["up", "down", "left", "right"]:
            self.key_presses[direction] = 0

        self.board_width = self.screen_width
        self.board_height = GRID_HEIGHT
        arcade.set_background_color(arcade.color.WHITE)

        # self.flicker_frequency = [2] * 4 #range(5, 25, 5)

        off_bits = 30
        sample_list = [1] * (PATTERN_LENGTH - off_bits) + [0] * off_bits
        for x in range(4):
            random.shuffle(sample_list)
            self.flicker_frequency.append(sample_list)

        self.load_icons()

    def load_icons(self):
        # Set up dir paths
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_dir = os.path.join(dir_path, 'images')
        icon_dir = os.path.join(image_dir, 'icons')
        icon_list = os.listdir(icon_dir)

        for icon in icon_list:
            self.texture_list.append(arcade.load_texture(os.path.join(icon_dir, icon)))

    def on_key_press(self, key, key_modifiers):
        if (key == arcade.key.UP):
            self.key_presses["up"] += 1
            print("Key pressed: {}".format("up"))
        elif (key == arcade.key.DOWN):
            self.key_presses["down"] += 1
            print("Key pressed: {}".format("down"))
        elif (key == arcade.key.LEFT):
            self.key_presses["left"] += 1
            print("Key pressed: {}".format("left"))
        elif (key == arcade.key.RIGHT):
            self.key_presses["right"] += 1
            print("Key pressed: {}".format("right"))

        # self.on_draw()

    def on_update(self, delta_time):
        self.on_draw()
        self.tick %= FREQUENCY
        self.tick += 1

    def draw_board(self):
        # Draw a grid
        # Draw vertical lines every 256 pixels
        for x in [256]:
            arcade.draw_line(x, 0, x, self.board_height, arcade.color.BLACK, 2)

        # Draw horizontal lines every 256 pixels
        for y in [256, 512, self.screen_height]:
            arcade.draw_line(0, y, self.screen_width, y, arcade.color.BLACK, 2)

        # Prep x,y pairs for where to print icons
        pos_list = []

        for x in [1, 3]:
            for y in [1, 3]:
                pos_list.append([self.screen_width * (x / 4), self.board_height * (y / 4)])

        # Load and draw all icons
        for ind, texture in enumerate(self.texture_list):
            freq = self.flicker_frequency[ind]
            pos = pos_list[ind]
            scale = .8
            # if self.tick % freq == 0 and self.tick != 0:
            if freq[self.tick % PATTERN_LENGTH]:
                arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, scale, 0)

    def draw_score_board(self):
        # Draw vertical lines every 128 pixels
        for x in [x * self.screen_width for x in range(1, 4)]:
            arcade.draw_line(x, self.screen_height, x, self.board_height, arcade.color.BLACK, 2)

        draw_x = self.screen_width * 1/16
        draw_y = self.board_height + SCORE_BOARD_HEIGHT * 1/2
        for dir, presses in self.key_presses.items():
            arcade.draw_text("{} pressed\n{} times".format(dir, presses), draw_x, draw_y, arcade.color.BLACK, 12)
            draw_x += self.screen_width * 1/4

    def on_draw(self):
        # Start the render process. This must be done before any drawing commands.
        arcade.start_render()

        # Draw grid
        self.draw_board()

        # Draw selection score board
        self.draw_score_board()

        # Finish the render.
        # Nothing will be drawn without this.
        # Must happen after all draw commands
        arcade.finish_render()

    def main():
        game = testing_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Testing Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    testing_window.main()
