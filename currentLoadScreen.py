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

referenceUnit = 1

class CurrentLoad:

    def __init__(self):
        # Values
        self.fontsize = 18
        self.current_load_value = 0

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
        done_button.grid(row=2, column=2, columnspan=2, ipady=20, ipadx=30)

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
        hx = HX711(5, 6)

        # I've found out that, for some reason, the order of the bytes is not always the same between versions of python, numpy and the hx711 itself.
        # Still need to figure out why does it change.
        # If you're experiencing super random values, change these values to MSB or LSB until to get more stable values.
        # There is some code below to debug and log the order of the bits and the bytes.
        # The first parameter is the order in which the bytes are used to build the "long" value.
        # The second paramter is the order of the bits inside each byte.
        # According to the HX711 Datasheet, the second parameter is MSB so you shouldn't need to modify it.
        hx.set_reading_format("MSB", "MSB")

        # HOW TO CALCULATE THE REFFERENCE UNIT
        # To set the reference unit to 1. Put 1kg on your sensor or anything you have and know exactly how much it weights.
        # In this case, 92 is 1 gram because, with 1 as a reference unit I got numbers near 0 without any weight
        # and I got numbers around 184000 when I added 2kg. So, according to the rule of thirds:
        # If 2000 grams is 184000 then 1000 grams is 184000 / 2000 = 92.
        # hx.set_reference_unit(113)

        # hx.set_reference_unit(referenceUnit)
        #
        # hx.reset()
        #
        # hx.tare()

        # print("Tare done! Add weight now...")

        # to use both channels, you'll need to tare them both
        # hx.tare_A()
        # hx.tare_B()
        self.get_weight(hx)

    def get_weight(self, hx):
        try:
            # These three lines are usefull to debug wether to use MSB or LSB in the reading formats
            # for the first parameter of "hx.set_reading_format("LSB", "MSB")".
            # Comment the two lines "val = hx.get_weight(5)" and "print val" and uncomment these three lines to see what it prints.

            # np_arr8_string = hx.get_np_arr8_string()
            # binary_string = hx.get_binary_string()
            # print binary_string + " " + np_arr8_string

            # Prints the weight. Comment if you're debbuging the MSB and LSB issue.
            val = round(hx.get_weight(5), 2)
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