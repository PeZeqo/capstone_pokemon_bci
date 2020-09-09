import arcade
import os
from project_constants import SCREEN_WIDTH as screen_width, SCREEN_HEIGHT as screen_height

# screen_width = 512
# screen_height = 512

# Open the window. Set the window title and dimensions (width and height)
arcade.open_window(screen_width, screen_height, "Drawing Primitives Example")

# Set the background color to white
# For a list of named colors see
# http://arcade.academy/arcade.color.html
# Colors can also be specified in (red, green, blue) format and
# (red, green, blue, alpha) format.
arcade.set_background_color(arcade.color.WHITE)

# Start the render process. This must be done before any drawing commands.
arcade.start_render()


# Draw a grid
# Draw vertical lines every 256 pixels
for x in [256]:
    arcade.draw_line(x, 0, x, screen_height, arcade.color.BLACK, 2)

# Draw horizontal lines every 256 pixels
for y in [256]:
    arcade.draw_line(0, y, screen_width, y, arcade.color.BLACK, 2)

# Set up dir paths
dir_path = os.path.dirname(os.path.realpath(__file__))
icon_dir = os.path.join(dir_path, 'icons')
icon_list = os.listdir(icon_dir)


# Prep x,y pairs for where to print icons
pos_list = []

for x in [1,3]:
    for y in [1,3]:
        pos_list.append([screen_width * (x/4), screen_height * (y/4)])

# Load and draw all icons
for ind, icon in enumerate(icon_list):
    texture = arcade.load_texture(os.path.join(icon_dir, icon))
    scale = .9
    pos = pos_list[ind]
    arcade.draw_scaled_texture_rectangle(pos[0], pos[1], texture, scale, 0)

# Finish the render.
# Nothing will be drawn without this.
# Must happen after all draw commands
arcade.finish_render()

# Keep the window up until someone closes it.
arcade.run()