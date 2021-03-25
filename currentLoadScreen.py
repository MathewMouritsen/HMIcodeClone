# Makes the Screen that shows the current load registered by the load cell

import time
import sys
import tkinter as tk
import platform

if platform.system() == "Linux":
    import RPi.GPIO as GPIO
    from hx711 import HX711

    EMULATE_HX711 = False
else:
    from emulated_hx711 import HX711

    EMULATE_HX711 = True

referenceUnit = 2180


class CurrentLoad:

    def __init__(self, hx):
        # Values
        self.fontsize = 18
        self.current_load_value = 0
        self.hx = hx

        # Window
        self.window = tk.Tk()
        self.window.title("Setting the Load")
        self.window.geometry("700x500")
        self.right = True

        # Fullscreen Settings
        if platform.system() == "Linux":
            self.is_fullscreen = True
        else:
            self.is_fullscreen = False
        self.window.attributes("-fullscreen", self.is_fullscreen)

        # Jobs that need to be able to be cancelled in other methods
        self.job = self.window.after(0, self.__nothing)

        # Label values that need to access functions to change the count
        self.current_load_number = tk.Label(self.window, text=0, font=(None, self.fontsize))
        self.current_load_number.grid(row=1, column=2, padx=30)

        # Labels
        current_load = tk.Label(self.window, text="Current Load", font=(None, self.fontsize))
        current_load.grid(row=1, column=1, pady=30)

        # Buttons
        go_button = tk.Button(self.window, text="GO", command=self.HX711main)
        go_button.grid(row=2, column=0, columnspan=2, ipady=20, ipadx=30)

        done_button = tk.Button(self.window, text="DONE", bg="blue", command=self.__done, activebackground="blue")
        done_button.grid(row=2, column=4, columnspan=2, ipady=20, ipadx=30)

        self.window.protocol("WM_DELETE_WINDOW", self.__done)
        self.window.mainloop()

    def __display_load(self):
        # Displays the current load registered by the load cell
        self.HX711main()

    def __done(self):
        self.window.destroy()
        self.window.quit()

    def cleanAndExit(self):
        print("Cleaning...")

        if not EMULATE_HX711:
            GPIO.cleanup()

        print("Bye!")
        sys.exit()

    def HX711main(self):
        # to use both channels, you'll need to tare them both
        # hx.tare_A()
        # hx.tare_B()
        self.get_weight(self.hx)

    def get_weight(self, hx):
        try:
            # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
            # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
            # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.

            # np_arr8_string = hx.get_np_arr8_string()
            # binary_string = hx.get_binary_string()
            # print binary_string + " " + np_arr8_string

            # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
            val = round(hx.get_weight(5) - 10.35, 2)
            self.current_load_number.config(text=val)
            self.window.update()

            # To get weight from both channels (if you have load cells hooked up
            # to both channel A and B), do something like this
            # val_A = hx.get_weight_A(5)
            # val_B = hx.get_weight_B(5)
            # print "A: %s  B: %s" % ( val_A, val_B )

            hx.power_down()
            hx.power_up()
            time.sleep(0.1)
            self.job = self.window.after(0, self.HX711main())

        except (KeyboardInterrupt, SystemExit):
            self.cleanAndExit()

    def __nothing(self):
        pass