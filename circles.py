# !/usr/bin/env python3

""" circles.py: 

Fullscreen Pixel mapping with OSC input. A 16x9 matrix of circles is drawn, 
each circle gets its color from three byte values (red, green, blue). 

The OSC byte values correspond to a DMX universe, so the 16x9 matrix of circles 
correspond to 144 RGB spots. This uses 432 DMX addresses, starting from 1.
Background color can be changed similar to a RGB spot, the DMX addresses are 433-435.

"""
import tkinter as tk # type: ignore

from pixelgui import Gui
from oscola import OscOla

# https://stackoverflow.com/questions/26286660/how-to-make-a-window-fullscreen-in-a-secondary-display-with-tkinter
# https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter



# -----------------------------------------------------------------------

w = Gui()
oscola = OscOla ()

def colorcircles ():
    """ 16 * 9 colored circles, the color is defined by DMX values 1 - 432
    """

    dmxinfo = oscola.get_channels (1,511) # get the universe
    width, height = w.winsize ()
    radx_base = width/32 # Pixelbreite = 2*radx
    rady_base = height/18 # Pixelhöhe = 2*rady

    # background color:
    bkcol = f"#{dmxinfo[432]:02x}{dmxinfo[433]:02x}{dmxinfo[434]:02x}"
    w.canvas.configure (bg=bkcol)    


    # the circles:
    for px in range (144):
        i = px * 3
        maxcol = max (dmxinfo[i], dmxinfo[i+1], dmxinfo[i+2]) # maximum of the color values
        # color:
        if maxcol > 0:
            upscale = 255 / maxcol
            red = int (dmxinfo[i] * upscale)
            green = int (dmxinfo[i+1] * upscale)
            blue = int (dmxinfo[i+2] * upscale)
            rgbcol = f"#{red:02x}{green:02x}{blue:02x}"
        else:
            rgbcol = "#000000"
        # radius:
        radx = rady = int ((maxcol / 255) * radx_base * w.radx_mod/60)

        if radx > 0:
            w.canvas.itemconfigure (w.circles[px], 
                                state="normal", 
                                fill=rgbcol, 
                                outline=rgbcol)
            w.canvas.coords (w.circles[px], 
                                w.pixinfo[px].center[0] - radx,
                                w.pixinfo[px].center[1] - rady,
                                w.pixinfo[px].center[0] + radx,
                                w.pixinfo[px].center[1] + rady  )
        else:
            w.canvas.itemconfigure (w.circles[px], 
                                state="hidden")


w.canvas.itemconfigure ("pixel", state="hidden")
w.set_fx (colorcircles)
w.run_fx ()
try:
    w.root.mainloop()
except:
    oscola.shutdown ()
    w.quit ()


