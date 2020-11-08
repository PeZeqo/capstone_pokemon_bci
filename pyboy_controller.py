from pyboy import WindowEvent


class pyboy_controller():
    pyboy = None

    def __init__(self, pyboy):
        self.pyboy = pyboy

    def send_command(self, command):
        actions = []
        command = command.upper()
        print("BUTTON PRESSED: {}".format(command))

        # switch statement to create WindowEvents (button commands for PyBoy)
        if command == 'UP':
            actions = [WindowEvent.PRESS_ARROW_UP, WindowEvent.RELEASE_ARROW_UP]
        elif command == 'DOWN':
            actions = [WindowEvent.PRESS_ARROW_DOWN, WindowEvent.RELEASE_ARROW_DOWN]
        elif command == 'LEFT':
            actions = [WindowEvent.PRESS_ARROW_LEFT, WindowEvent.RELEASE_ARROW_LEFT]
        elif command == 'RIGHT':
            actions = [WindowEvent.PRESS_ARROW_RIGHT, WindowEvent.RELEASE_ARROW_RIGHT]
        elif command == 'Z':
            actions = [WindowEvent.PRESS_BUTTON_B, WindowEvent.RELEASE_BUTTON_B]
        elif command == 'X':
            actions = [WindowEvent.PRESS_BUTTON_A, WindowEvent.RELEASE_BUTTON_A]
        elif command == 'SELECT':
            actions = [WindowEvent.PRESS_BUTTON_SELECT, WindowEvent.RELEASE_BUTTON_SELECT]
        elif command == 'START':
            actions = [WindowEvent.PRESS_BUTTON_START, WindowEvent.RELEASE_BUTTON_START]

        # if actions list isn't empty, send commands to pyboy and tick the pyboy window to process each command
        if actions:
            for action in actions:
                self.pyboy.send_input(WindowEvent(action))
                self.pyboy.tick()
