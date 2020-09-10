from pynput.keyboard import Key, Listener

# Class for listening to keyboard actions
class keyboard_listener:

    def on_press(self, key):
        print('{0} pressed'.format(key))

    def on_release(self, key):
        # print('{0} release'.format(key))
        if key == Key.esc:
            # Stop listener
            return False

    def being_listener(self):
        # Collect events until released
        with Listener(
                on_press=self.on_press,
                on_release=self.on_release) as listener:
            listener.join()