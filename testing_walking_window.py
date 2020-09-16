import testing_window
import os
import arcade

class testing_walking_window(testing_window.testing_window, arcade.Window):
    background_width = 1323
    background_height = 884
    background = None

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

    def setup(self):
        super().setup()
        self.load_background()
        self.board_width = self.background_width
        self.board_height = self.background_height

    def load_background(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_dir = os.path.join(dir_path, 'images')
        background_dir = os.path.join(image_dir, 'backgrounds')

        print(os.path.isfile(os.path.join(background_dir, 'walking_screen.png')))

        self.background = arcade.load_texture(os.path.join(background_dir, 'walking_screen.png'))

    def draw_board(self):
        # Load background if not loaded properly
        if self.background is None:
            print(self.background)
            self.load_background()
            print(self.background)

        # Draw screen background
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            self.background_width, self.background_height,
                                            self.background)

        # Draw horizontal lines
        for y in [self.background_height]:
            arcade.draw_line(0, y, self.background_width, y, arcade.color.BLACK, 2)

        # Prep x,y pairs for where to print icons
        pos_list = []

        for x in [1, 3]:
            for y in [1, 3]:
                pos_list.append([self.background_width * (x / 4), self.background_height * (y / 4)])

        # Load and draw all icons
        for ind, texture in enumerate(self.texture_list):
            freq = self.flicker_frequency[ind]
            pos = pos_list[ind]
            scale = .5
            # if self.tick % freq == 0 and self.tick != 0:
            if freq[self.tick % testing_window.PATTERN_LENGTH]:
                arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, scale, 0)

    def main():
        game = testing_walking_window(1323, 884 + testing_window.SCORE_BOARD_HEIGHT,
                                      "Testing Walking Window")
        game.setup()
        arcade.run()


if __name__ == "__main__":
    testing_walking_window.main()
