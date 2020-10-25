from threading import Thread
import random
from time import sleep
from pynput.keyboard import Key, Controller


class command_handler(Thread):
    eeg_data = None
    keyboard = Controller()

    def __init__(self, eeg_data):
        Thread.__init__(self)
        self.eeg_data = eeg_data
        self.daemon = True
        self.start()

    def filter_data(self):
        sleep(0.25)

    def predict_command(self):
        return random.randint(0, 8)

    def press_release(self, key):
        self.keyboard.press(key)
        self.keyboard.release(key)

    def command_to_keyboard_action(self, command):
        # command 0 is no-action
        if command == 0:
            return
        elif command == 1:
            self.press_release('z')
        elif command == 2:
            self.press_release(Key.up)
        elif command == 3:
            self.press_release('x')
        elif command == 4:
            self.press_release(Key.left)
        elif command == 5:
            self.press_release(Key.right)
        elif command == 6:
            self.press_release(Key.enter)
        elif command == 7:
            self.press_release(Key.down)
        elif command == 8:
            self.press_release(Key.shift_r)

    def run(self):
        print("Starting thread")
        self.filter_data()
        command = self.predict_command()
        print("PRESSING: {}".format(command))
        self.command_to_keyboard_action(command)

        print("Ending thread")


