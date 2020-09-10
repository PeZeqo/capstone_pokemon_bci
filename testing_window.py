import arcade
import os
import random
from project_constants import SCREEN_WIDTH as screen_width, SCREEN_HEIGHT as screen_height, FREQUENCY as frequency, GRID_HEIGHT as grid_height, SCORE_BOARD_HEIGHT as score_board_height, PATTERN_LENGTH as pattern_length


# Class for the testing window
class testing_window(arcade.Window):
    key_presses = {}
    texture_list = []
    flicker_frequency = []
    tick = 0
    score_list = []

    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.set_update_rate(1/frequency)
        arcade.set_background_color(arcade.color.WHITE)

    def setup(self):
        for direction in ["up", "down", "left", "right"]:
            self.key_presses[direction] = 0

        # self.flicker_frequency = [2] * 4 #range(5, 25, 5)

        off_bits = 2
        sample_list = [1] * (pattern_length - off_bits) + [0] * off_bits
        for x in range(4):
            self.flicker_frequency.append(random.sample(sample_list, len(sample_list)))

        # Set up dir paths
        dir_path = os.path.dirname(os.path.realpath(__file__))
        icon_dir = os.path.join(dir_path, 'icons')
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
        self.tick %= frequency
        self.tick += 1
        if self.tick % frequency == 0:
            print("1 second passed")

    def draw_grid(self):
        # Draw a grid
        # Draw vertical lines every 256 pixels
        for x in [256]:
            arcade.draw_line(x, 0, x, grid_height, arcade.color.BLACK, 2)

        # Draw horizontal lines every 256 pixels
        for y in [256, 512, screen_height]:
            arcade.draw_line(0, y, screen_width, y, arcade.color.BLACK, 2)

        # Prep x,y pairs for where to print icons
        pos_list = []

        for x in [1, 3]:
            for y in [1, 3]:
                pos_list.append([screen_width * (x / 4), grid_height * (y / 4)])

        # Load and draw all icons
        for ind, texture in enumerate(self.texture_list):
            freq = self.flicker_frequency[ind]
            pos = pos_list[ind]
            scale = .8
            # if self.tick % freq == 0 and self.tick != 0:
            if freq[self.tick % pattern_length]:
                arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, scale, 0)

    def draw_score_board(self):
        # Draw vertical lines every 128 pixels
        for x in [128, 256, 384]:
            arcade.draw_line(x, screen_height, x, grid_height, arcade.color.BLACK, 2)

        draw_x = screen_width * 1/20
        draw_y = grid_height + score_board_height * 1/2
        for dir, presses in self.key_presses.items():
            arcade.draw_text("{} pressed\n{} times".format(dir, presses), draw_x, draw_y, arcade.color.BLACK, 12)
            draw_x += screen_width * 1/4


    def on_draw(self):
        # Start the render process. This must be done before any drawing commands.
        arcade.start_render()

        # Draw grid
        self.draw_grid()

        # Draw selection score board
        self.draw_score_board()

        # Finish the render.
        # Nothing will be drawn without this.
        # Must happen after all draw commands
        arcade.finish_render()

    def main():
        game = testing_window(screen_width, screen_height, "Testing Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    testing_window.main()
