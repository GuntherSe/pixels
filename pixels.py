# !/usr/bin/env python3

""" pixels.py: 

Fullscreen Pixel mapping with OSC input. A 16x9 matrix of circles is drawn, 
each circle gets its color from three byte values (red, green, blue). 

The OSC byte values correspond to a DMX universe, so the 16x9 matrix of circles 
correspond to 144 RGB spots. This uses 432 DMX addresses, starting from 1.
Background color can be changed similar to a RGB spot, the DMX addresses are 433-435.

"""
from tkinter import *
# from tkinter import ttk
# from PIL import Image,ImageTk
# import os

from pixelgui import Gui
from oscola import OscOla

# https://stackoverflow.com/questions/26286660/how-to-make-a-window-fullscreen-in-a-secondary-display-with-tkinter
# https://stackoverflow.com/questions/7966119/display-fullscreen-mode-on-tkinter



# -----------------------------------------------------------------------
# if __name__ == '__main__':

w = Gui()
oscola = OscOla ()

def colorpixels ():
    """ Farbe der 16x9 Pixel ändern, benutzt die ersten 432 DMX Werte.
    more_dmx: DMX 433 acts as a switch: if the value > 127 then the following 
    DMX values are evaluated for 
        background color (DMX 434-436) 
        pixel x-size (DMX 437) 
        pixel y-size (DMX 438)
        smoothness (DMX 439):   
            0-19 -> smooth off
            20-39 -> smooth, splinesteps = 1
            40-59 -> smooth, splinesteps = 2
            60-79 -> smooth, splinesteps = 3
            80-99 -> smooth, splinesteps = 4
            100-119 -> smooth, splinesteps = 5
            120-139 -> smooth, splinesteps = 6
            140-159 -> smooth, splinesteps = 7
            160-179 -> smooth, splinesteps = 8
            180-199 -> smooth, splinesteps = 9
            200-219 -> smooth, splinesteps = 10
            220-239 -> smooth, splinesteps = 11
            240-255 -> smooth, splinesteps = 12
        outline color (DMX 440-442)
        outline width (DMX 443)
        blur effect (DMX 444):
            0-127 -> blur off
            128-255 -> blur on
        use image (DMX 445)
    if the value of DMX 433 <= 127 then the pixel radius is calculated to get 
    the pixels touch each other.
    """

    dmxinfo = oscola.get_channels (1,511) # get the universe
    more_dmx = dmxinfo[432]
    width, height = w.winsize ()
    radx_base = width/32 # Pixelbreite = 2*radx
    rady_base = height/18 # Pixelhöhe = 2*rady

    if more_dmx > 127:
        # background color:
        bkcol = f"#{dmxinfo[433]:02x}{dmxinfo[434]:02x}{dmxinfo[435]:02x}"
        # pixel radius:
        w.radx_mod = dmxinfo[436]
        w.rady_mod = dmxinfo[437]
        radx = int (radx_base*w.radx_mod/60)
        rady = int (rady_base*w.rady_mod/60)
        # smoothness:
        smoothie = dmxinfo[438]
        if smoothie < 20:
            smoothtoggle = 0
            steps = 12
        else:
            smoothtoggle = 1
            steps = int(smoothie/20)
        # outline:
        check_blur = dmxinfo[443]
        if check_blur <= 127:
            # don't use blur effect
            outlinecol = f"#{dmxinfo[439]:02x}{dmxinfo[440]:02x}{dmxinfo[441]:02x}"
            outlinewidth = int (dmxinfo[442]/10)
            if outlinewidth:
                outlinevisible = True
            else:
                outlinevisible = False
        else:
            # blur effect: 
            w.blur ()
            outlinevisible = True

        # image or pixels:
        check_image = dmxinfo[444]
        if check_image >= 10:
            # turn off pixels:
            w.canvas.itemconfigure ("pixel", state="hidden")
            # w.canvas.itemconfigure ("image", state="normal")
            use_image = True
            w.pictures.resize (2*radx, 2*rady)
            pic_count = w.pictures.count ()
        else:
            # turn off images:
            w.canvas.itemconfigure ("image", state="hidden")
            use_image = False
            

    else:
        bkcol = "black"
        radx = radx_base
        rady = rady_base
        smoothtoggle = 1
        steps = 12
        outlinevisible = False
        outlinewidth = 0
        use_image = False
        
    w.canvas.configure (bg=bkcol)    

    # pixel colors:
    for px in range (144):
        i = px * 3
        rgbcol = f"#{dmxinfo[i]:02x}{dmxinfo[i+1]:02x}{dmxinfo[i+2]:02x}"
        # show only if DMX values > 0:
        if use_image:   # images visible:
            if dmxinfo[i] : 
                pic_num = min (pic_count-1, int (dmxinfo[i+1]/10)) 
                # 'green' / 10 = picture number, => maximum 25 different pics

                w.canvas.itemconfigure (w.images[px], 
                                        state="normal",
                                        image=w.pictures.resized[pic_num])
                w.canvas.coords (w.images[px], 
                                    w.pixinfo[px].center[0] - radx,
                                    w.pixinfo[px].center[1] - rady)
            else:
                # w.canvas.itemconfigure (w.pixels[px], state="hidden")
                w.canvas.itemconfigure (w.images[px], state="hidden",
                    image=w.pictures.resized[0])

        else: # pixels visible:
            if dmxinfo[i] or dmxinfo[i+1] or dmxinfo[i+2]:
                if outlinevisible and check_blur:
                    w.canvas.itemconfigure (w.pixels[px], state="normal", 
                                        fill=rgbcol, 
                                        # outline=outlinecol,
                                        # width=outlinewidth,
                                        smooth=smoothtoggle,
                                        splinesteps=steps)

                elif outlinevisible and not check_blur:
                    w.canvas.itemconfigure (w.pixels[px], state="normal", 
                                        fill=rgbcol, 
                                        outline=outlinecol,
                                        width=outlinewidth,
                                        smooth=smoothtoggle,
                                        splinesteps=steps)
                else:
                    w.canvas.itemconfigure (w.pixels[px], state="normal", 
                                        fill=rgbcol, 
                                        outline=rgbcol,
                                        width=outlinewidth,
                                        smooth=smoothtoggle,
                                        splinesteps=steps)

                w.canvas.coords (w.pixels[px], 
                                    w.pixinfo[px].center[0] - radx,
                                    w.pixinfo[px].center[1] - rady,
                                    w.pixinfo[px].center[0] + radx,
                                    w.pixinfo[px].center[1] - rady,
                                    w.pixinfo[px].center[0] + radx,
                                    w.pixinfo[px].center[1] + rady,
                                    w.pixinfo[px].center[0] - radx,
                                    w.pixinfo[px].center[1] + rady  )
            else:
                w.canvas.itemconfigure (w.pixels[px], state="hidden")
                # w.canvas.itemconfigure (w.images[px], state="hidden",
                #                         image=w.pictures.resized[0])

w.set_fx (colorpixels)
w.run_fx ()
try:
    w.root.mainloop()
except:
    oscola.shutdown ()
    w.quit ()


