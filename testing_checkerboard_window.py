import testing_window
import os
import arcade
import random

class testing_checkerboard_window(testing_window.testing_window, arcade.Window):
    background_width = 1600
    background_height = 900
    background = None
    last_state = []
    checkerboard_pos_list = []
    selected_quad = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        super().setup()

        # load textures
        self.load_checkerboards()

        # set all checkerboards to normal state
        self.last_state = [0] * 4

        # set board params
        self.board_width = self.background_width
        self.board_height = self.background_height

        # Prep x,y pairs for where to print icons
        for x in [128, self.board_width - 128]:
            for y in [128, self.board_height - 128]:
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

    def highlight_selection(self):
        if self.selected_quad is None:
            return

        icon_height = 256
        icon_width = 256

        pos = self.checkerboard_pos_list[self.selected_quad]

        arcade.draw_rectangle_outline(pos[0], pos[1], icon_width, icon_height, arcade.color.ORANGE, 10)

    def draw_board(self):
        # Draw background
        arcade.set_background_color(arcade.color.WHITE)

        if self.tick == 1:
            self.selected_quad = (random.randint(0, 3))

        # Load and draw all icons
        for ind, last_state in enumerate(self.last_state):
            freq = self.flicker_frequency[ind]
            pos = self.checkerboard_pos_list[ind]
            scale = 1
            texture = self.texture_list[last_state]

            # if self.tick % freq == 0 and self.tick != 0:
            if freq[self.tick % testing_window.PATTERN_LENGTH]:
                self.last_state[ind] = not last_state

            arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, scale, 0)

        self.highlight_selection()

    def main():
        game = testing_checkerboard_window(1600, 900 + testing_window.SCORE_BOARD_HEIGHT,
                                      "Testing Checkerboard Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    testing_checkerboard_window.main()
