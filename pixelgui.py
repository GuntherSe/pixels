#!/usr/bin/env python3

""" pixelgui.py:

A Tkinter Gui for a fullscreen output. It combines DMX input with a set of 16 * 9 (= 144) 
LED simulating section on a screen respective projector.

"""
# from tkinter import *
# from tkinter import ttk
import tkinter as tk

import os
from pictures import Pictures

image_x, image_y = 100, 100

def no_fx ():
    """ initialization of FX function """
    return


# https://stackoverflow.com/questions/26286660/how-to-make-a-window-fullscreen-in-a-secondary-display-with-tkinter
# https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter

class Rgbpixel:

    def __init__(self) -> None:
        self.center = [10,10] # Mittelpunkt
        self.address = 1 # dmx Start, 1 <= address <= 509

    def set_center (self, newcenter:list):
        """ neues center setzen """
        self.center = newcenter

    def set_address (self, newaddress:int):
        """ neue dmx Adresse setzen """
        if 1 <= newaddress <= 509:
            self.address = newaddress


class Gui:
    fullscreen = False

    def __init__(self, action = None):
        self.root = tk.Tk()
        # Keyboard bindings:
        self.root.bind("<F11>", self.toggleFullScreen)
        self.root.bind("f", self.toggleFullScreen)
        # self.root.bind("<Alt-Return>", self.toggleFullScreen)
        self.root.bind("<Control-w>", self.quit)
        self.root.bind ("q", self.quit)

        self.root.geometry("640x360+30+30")
        self.fx_func = no_fx

        # https://stackoverflow.com/questions/24945467/python-tkinter-set-entry-grid-width-100
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.createWidgets()


    def createWidgets (self):
        """ widgets for pixel screen 
        """
        self.root.update()
        self.canvas = tk.Canvas (self.root, background="black") 
        self.canvas.config (highlightthickness=0) # remove border
        self.canvas.grid (column=0, row=0, sticky="N, W, E, S")

        # geometry:
        self.cols = 16 # Anzahl der Pixel in einer Reihe
        self.rows = 9  # Anzahl der Reihen
        count = self.cols * self.rows # Anzahl der Pixel = 144

        radx_base = self.root.winfo_width()/32 # Pixelbreite = 2*radx
        rady_base = self.root.winfo_height()/18 # Pixelhöhe = 2*rady
        self.radx_mod = 60  # size of radx can be modified
        self.rady_mod = 60  # size of rady can be modified
        radx = int (radx_base*self.radx_mod/60)
        rady = int (rady_base*self.rady_mod/60)

        # pixels:
        self.pixinfo = [Rgbpixel() for i in range (count)]
        self.pixels = [] # Liste der canvas-Polygone
        # circles:
        self.circles = []
        # images:
        self.pictures = Pictures ("pictures")
        self.images = [] # list of resized images, = canvas objects!
        self.image_numbers = [0 for i in range (count)]
        self.pictures.resize (2*radx, 2*rady)

        for i in range (count):
            self.pixinfo[i].address = 1 + 3*i
            col = i % 16 # Spalten von 0 bis 15
            row = int (i / 16) # Reihen von 0 bis 8
            self.pixinfo[i].set_center ([col*radx_base*2 + radx_base, 
                                         row*rady_base*2 + rady_base ]) 
            self.pixels.append (self.canvas.create_polygon (
                self.pixinfo[i].center[0] - radx,
                self.pixinfo[i].center[1] - rady,
                self.pixinfo[i].center[0] + radx,
                self.pixinfo[i].center[1] - rady,
                self.pixinfo[i].center[0] + radx,
                self.pixinfo[i].center[1] + rady,
                self.pixinfo[i].center[0] - radx,
                self.pixinfo[i].center[1] + rady,
                tags=("pixel"),    # set tag 'pixel'
                fill="#ff0000", outline="#000000"
            ))
            self.circles.append (self.canvas.create_oval (
                self.pixinfo[i].center[0] - radx,
                self.pixinfo[i].center[1] - rady,
                self.pixinfo[i].center[0] + radx,
                self.pixinfo[i].center[1] + rady,
                tags=("circle"),
                fill=("#00FF00"),
                state="hidden"
            ))
            self.images.append (self.canvas.create_image (
                self.pixinfo[i].center[0] - radx,
                self.pixinfo[i].center[1] - rady, 
                anchor="nw", 
                tags=("image"),
                image=self.pictures.resized[0],
                state="hidden"
            ))


    def toggleFullScreen(self, event):
        if self.fullscreen:
            self.deactivateFullscreen()
        else:
            self.activateFullscreen()

    def activateFullscreen(self):
        self.fullscreen = True

        if os.name == "posix":
            # width = self.root.winfo_screenwidth ()
            # height = self.root.winfo_screenheight ()
            geometry = self.root.winfo_geometry ()
            self.root.geometry (geometry)
            self.root.attributes ("-fullscreen", True)
            self.root.update()
        else:
            self.root.state("zoomed")
        self.root.overrideredirect(True)
        self.root.config (cursor="none")
        self.resize_pixels ()


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
        self.resize_pixels ()

    def winsize (self):
        """ get window size """
        # print (f"Breite: {self.root.winfo_width()}, Höhe: {self.root.winfo_height()}")
        return (self.root.winfo_width(), self.root.winfo_height())

    def quit(self, event=None):
        print("quiting...", event)
        self.root.quit()

    def set_fx (self, newfunc):
        """ FX Funkion zuweisen """
        self.fx_func = newfunc

    def run_fx (self):
        """ FX in mainloop ausführen """
        self.fx_func ()
        self.root.after (100, self.run_fx)

    # Effekte: 

    def resize_pixels (self):
        """ Pixelgröße an Fenstergröße anpassen """
        self.root.update () 
        width, height = self.winsize ()

        radx_base = width/32 # Pixelbreite = 2*radx
        rady_base = height/18 # Pixelhöhe = 2*rady
        radx = int (radx_base*self.radx_mod/60)
        rady = int (rady_base*self.rady_mod/60)
        self.pictures.resize (2*radx, 2*rady)

        for k, v in enumerate (self.pixinfo):
            col = k % 16 # Spalten von 0 bis 15
            row = int (k / 16) # Reihen von 0 bis 8
            v.set_center ([col*radx_base*2 + radx_base, row*rady_base*2 + rady_base ]) 
            self.canvas.coords (self.pixels[k], 
                                v.center[0] - radx,
                                v.center[1] - rady,
                                v.center[0] + radx,
                                v.center[1] - rady,
                                v.center[0] + radx,
                                v.center[1] + rady,
                                v.center[0] - radx,
                                v.center[1] + rady )
            self.canvas.coords (self.circles[k],
                                v.center[0] - radx,
                                v.center[1] - rady,
                                v.center[0] + radx,
                                v.center[1] + rady )
            self.canvas.itemconfigure (self.images[k], 
                image=self.pictures.resized[self.image_numbers[k]]) 
            # TODO: remember last picture in every position
            self.canvas.coords (self.images[k], 
                                v.center[0] - radx,
                                v.center[1] - rady)

    def blur (self):
        """ make an outline with same color as pixel fill color
        
        outline with is calculated, outline color is darker than fill color
        """
        # width of outline:
        coords = self.canvas.coords (self.pixels[0])
        width = int ((coords[2] - coords[0]) / 16 )
        self.canvas.itemconfigure ("pixel", width=width)
        for px in self.pixels:
            # get pixel color:
            col = self.canvas.itemcget (px, "fill")
            # reduce brightness
            try:
                red = int (int (col[1:3], 16) /2)
                green = int (int (col[3:5], 16) /2)
                blue = int (int (col[5:], 16) /2)
                rgbcol = f"#{red:02x}{green:02x}{blue:02x}"
            except:
                rgbcol= "#000000"
            self.canvas.itemconfigure (px, outline=rgbcol)


    def unblur (self):
        """ remove blur effect """
        self.canvas.itemconfigure ("pixel", width=0, outline="#000000")


    # def image_name (self) -> str:
    #     """ return full name of image 
    #     """
    #     thispath  = os.path.dirname(os.path.realpath(__file__))  
    #     fullname = os.path.join (thispath, "ahornblatt2.png")     
    #     return fullname



if __name__ == "__main__":
    w = Gui()

    def setsplinestep (count):
        """ test splinestep """
        w.canvas.itemconfigure ("pixel", smooth=1, splinesteps=count)

    def splinestepoff ()    :
        w.canvas.itemconfigure ("pixel", smooth=0)

    def activatecircles ():
        w.canvas.itemconfigure ("pixel", state="hidden")
        w.canvas.itemconfigure ("circle", state="normal")
        
    def activatepixels ():
        w.canvas.itemconfigure ("pixel", state="normal")
        w.canvas.itemconfigure ("circle", state="hidden")
        


    w.root.bind ("0", lambda e: splinestepoff())
    w.root.bind ("1", lambda e: setsplinestep(1))
    w.root.bind ("2", lambda e: setsplinestep(2))
    w.root.bind ("3", lambda e: setsplinestep(3))
    w.root.bind ("4", lambda e: setsplinestep(4))
    w.root.bind ("b", lambda e: w.blur())
    w.root.bind ("n", lambda e: w.unblur())
    w.root.bind ("c", lambda e: activatecircles())
    w.root.bind ("v", lambda e: activatepixels())

    w.canvas.itemconfigure ("pixel", smooth=1, splinesteps=1,
                width=3)
    try:
        w.root.mainloop()
    except:
        w.quit ()

