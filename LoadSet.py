# Makes the Screen that lets us set the load

import tkinter as tk
import platform
if platform.system() == "Darwin" or platform.system() == "Windows":
    import lapOut as outputs
else:
    import piOut as outputs

class SettingLoad:

    def __init__(self, output):
        self.out = output
        self.right = True
        self.window = "0" #Becomes window object first time show() is done 
        
    def show(self):
        
        # Window
        self.window = tk.Tk()
        self.window.title("Setting the Load")
        self.window.config(bg="Blue")
        self.window.geometry("700x500")
        self.right = True

        # Buttons
        switch_button = tk.Button(self.window, text="Switch Cylinder", bg="Green", command=self.__switch, activebackground="Green")
        switch_button.grid(row=0, column=0, ipadx=20, ipady=20, padx=30, pady=50)

        stop_button = tk.Button(self.window, text="STOP", bg = "red", command=self.__stop, activebackground="red")
        stop_button.grid(row=0, column=1, ipadx=20, ipady=20, padx=30, pady=50)

        self.__switch()
        self.window.protocol("WM_DELETE_WINDOW", self.__stop)
        self.window.mainloop()

    def __switch(self):
        # Switches the activated load from one side to the other.
        self.out.off()
        if self.right:
            self.right = False
            self.out.leftOn()
        else:
            self.right = True
            self.out.rightOn()
    
    def __stop(self):
        # The stop button that shuts off the load and closes the window.
        self.out.off()
        self.window.destroy()
        self.window.quit()
        