#!/usr/bin/env python3
import tkinter as tk
import os

from oscola import OscOla

# https://stackoverflow.com/questions/26286660/how-to-make-a-window-fullscreen-in-a-secondary-display-with-tkinter
# https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter

def no_fx ():
    """ initialization of FX function """
    return



class Gui:
    fullscreen = False

    def __init__(self, action = None):
        self.root = tk.Tk()
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("f", self.toggleFullScreen)
        self.root.bind("<Alt-Return>", self.toggleFullScreen)
        self.root.bind("<Control-w>", self.quit)
        self.root.bind ("q", self.quit)
        self.root.geometry("640x360+30+30")
        self.fx_func = no_fx


    def toggleFullScreen(self, event):
        if self.fullscreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullscreen = True

        if os.name == "posix":
            self.root.attributes ("-fullscreen", True)
            self.root.update()
        else:
            self.root.state("zoomed")
        self.root.overrideredirect(True)
        self.root.config (cursor="none")


    def deactivateFullscreen(self):
        self.fullscreen = False
        if os.name == "posix":
            self.root.geometry("170x200+30+30")
            self.root.attributes ("-fullscreen", False)
        else:
            self.root.state("normal")

        self.root.geometry("640x360+30+30")
        self.root.overrideredirect(False)
        self.root.config (cursor="")

    def quit(self, event=None):
        print("quiting...", event)
        self.root.quit()


    def background (self, red, green, blue):
        """ Background-Farbe festlegen """
        backcol = f"#{red:02x}{green:02x}{blue:02x}"
        self.root['background'] = backcol

    
    def set_fx (self, newfunc):
        """ FX Funkion zuweisen """
        self.fx_func = newfunc

    def run_fx (self):
        """ FX in mainloop ausführen """
        self.fx_func ()
        self.root.after (10, self.run_fx)




# -----------------------------------------------------------------------
if __name__ == '__main__':

    w = Gui()
    oscola = OscOla ()

    def colorchanger ():
        # Hintergrundfarbe ändern
        rgb = oscola.get_channels (1,3)
        w.background (rgb[0], rgb[1], rgb[2])    

    w.set_fx (colorchanger)
    w.run_fx ()
    try:
        w.root.mainloop()
    except:
        oscola.shutdown ()
        w.quit ()
    

