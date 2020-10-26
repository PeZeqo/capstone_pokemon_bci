import os
from project_constants import FREQUENCY, PATTERN_LENGTH, PADDING, BASE_HEIGHT, BASE_WIDTH, ARROW_SIZE, ARROW_SCALE, \
    CHECKERBOARD_SIZE, RECORDINGS_PER_ICON, SECONDS_PER_RECORDING, PAUSE_TO_RECORD_RATIO, COMMAND_SEND_FREQUENCY
import arcade
import winsound
from cortex.cortex import Cortex
import pandas as pd
import numpy as np

# Class for the testing window
class data_collection_window(arcade.Window):

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
    record_ticks = FREQUENCY * SECONDS_PER_RECORDING
    pause_ticks = record_ticks * PAUSE_TO_RECORD_RATIO
    currently_recording = False
    wait_on_user = True
    recordings_done = 0
    beep_frequency = 2500
    beep_duration = 100

    # data collection vars
    generator = None
    recording_data = []
    cortex = None
    data_columns = ["P7", "O1", "O2", "P8", "TIME"]

    def __init__(self, width, height, title):
        # set total screen size since we also need space to draw checkerboards
        self.screen_width = self.arrow_size + CHECKERBOARD_SIZE * 2 + PADDING
        self.screen_height = self.arrow_size + CHECKERBOARD_SIZE * 2 + PADDING

        self.draw_scale = self.screen_height / BASE_HEIGHT

        # let Arcade Window run it's setup
        super().__init__(self.screen_width, self.screen_height, title, resizable=True)

        # set frame rate as (1 / desired_frame_rate)
        self.set_update_rate(1/FREQUENCY)

    def setup(self):
        self.setup_checkerboards()
        self.load_arrows()
        self.setup_cortex()

    def setup_cortex(self):
        self.cortex = Cortex(None)
        self.cortex.do_prepare_steps()
        self.generator = self.cortex.sub_request(['eeg'])
        self.recording_data = pd.DataFrame(columns=self.data_columns)

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
        # self.on_draw()
        self.exhaust()
        self.tick += 1
        if not self.wait_on_user:
            self.handle_recording()

        # if self.tick % COMMAND_SEND_FREQUENCY == 0:
        #     self.create_command_task()

    def create_command_task(self):
        pass

    def beep(self):
        winsound.Beep(self.beep_frequency, self.beep_duration)

    def exhaust(self):
        next(self.generator)

    def add_recording(self):
        to_append = np.asarray(list(next(self.generator).queue))
        a_series = pd.DataFrame(to_append, columns=self.recording_data.columns)
        self.recording_data = self.recording_data.append(a_series, ignore_index=True)

    def export_recording(self):
        self.recording_data.to_csv('recordings\\checkerboard_recording_sultan_{}.csv'.format(self.selected_arrow))
        self.recording_data.drop(self.recording_data.index, inplace=True)

    def handle_recording(self):
        # if not on pause and the allotted pause time has passed, start recording again
        if not self.currently_recording and self.tick == self.pause_ticks:
            self.currently_recording = True
            self.tick = 0
            self.beep()

        # if recording and the allotted recording time has passed, start pause again
        elif self.currently_recording and self.tick == self.record_ticks:
            self.add_recording()
            self.currently_recording = False
            self.recordings_done += 1
            self.tick = 0
            self.beep()

            # finished all recordings for this icon
            if self.recordings_done == RECORDINGS_PER_ICON:
                self.recordings_done = 0
                self.export_recording()
                self.wait_on_user = True
                self.selected_arrow += 1

                # went through all arrows, means we recorded all checkerboards
                if self.selected_arrow == len(self.arrow_textures):
                    self.exit_window()

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
        arcade.draw_scaled_texture_rectangle(self.width / 2, self.height / 2, self.arrow_textures[self.selected_arrow],
                                             ARROW_SCALE * self.draw_scale)

    def draw_timer(self):
        arcade.draw_text("Timer: " + str(round(self.tick / FREQUENCY, 2)), (self.width / 2) - (PADDING * 1.2) * self.draw_scale,
                         (self.height + self.arrow_size) / 2 - (PADDING * self.draw_scale), arcade.color.WHITE,
                         40 * self.draw_scale)

        arcade.draw_text("Recordings Left: " + str(RECORDINGS_PER_ICON - self.recordings_done), (self.width / 2) - (PADDING * 2) * self.draw_scale,
                         (self.height - self.arrow_size) / 2 + (PADDING * self.draw_scale), arcade.color.WHITE,
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
        # switch statement to control data collection
        if (key == arcade.key.SPACE):
            self.wait_on_user = False
            self.currently_recording = False
            self.tick = 0

    def exit_window(self):
        exit()

    def main():
        window = data_collection_window(0, 0, "Data Collection Window")
        window.setup()
        arcade.run()


if __name__ == "__main__":
    data_collection_window.main()
