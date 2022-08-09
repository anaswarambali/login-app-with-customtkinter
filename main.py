import time
from pynput.keyboard import Listener, Key
import tkinter

text = "na no body does it better"

class User:

    def __init__(self, username, password):
        self.win = tkinter.Tk()
        self.win.geometry("200x300")
        self.label = tkinter.Entry(self.win, textvariable='hi', bg='red')
        self.label.grid()
        self.end_time = time.time()
        self.dwell = self.start_time = self.flight = None
        self.username = username
        self.password = password
        self.sample = "na no body does it better"
        self.i = 0
        self.sample_length = len(self.sample)
        self.dwell_ls = self.flight_ls = [x for x in range(self.sample_length)]
        self.mistake = False

    def listen(self):
        def on_press(key):
            self.start_time = time.time()
            self.flight = self.start_time-self.end_time
            print(str(key), "Key pressed\ntime: ", self.flight)

        def on_release(key):
            self.end_time = time.time()
            self.dwell = self.end_time-self.start_time

            print(str(key), "Key released\ntime: ", self.dwell)
            print('\n', self.i, self.sample_length)

            if key == Key.enter or self.i > self.sample_length-1:
                print("Escape")
                self.i = 0
                return False
            else:
                self.flight_ls[self.i] = self.flight
                self.dwell_ls[self.i] = self.dwell
                self.i += 1


        listener = Listener(on_press=on_press, on_release=on_release)
        listener.start()


app = User('anaswar', 'xyz')
app.listen()
app.win.mainloop()
print(app.flight_ls, '\n', app.dwell_ls)
