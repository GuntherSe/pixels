#!/usr/bin/env python3

""" class Pictures: get fullname, path, number of pictures in folder 'pictures' 

    resize pictures to desired size
"""

import os, os.path
import glob
from tkinter import *
from PIL import Image, ImageTk #, ImageFilter

class Pictures:

    def __init__(self, picdir) -> None:
        self.PATH      = os.path.dirname(os.path.realpath(__file__))
        self.imagepath = os.path.join (self.PATH, picdir, "*.png")
        self.imagelist = sorted (glob.glob (self.imagepath))
        self.image_x = 100
        self.image_y = 100
        self.resized = []


    def count (self) -> int:
        self.imagelist = sorted (glob.glob (self.imagepath))
        return len (self.imagelist)
    
    def list (self) -> list:
        self.imagelist = sorted (glob.glob (self.imagepath))
        return self.imagelist
    
    def resize (self, x_size, y_size):
        """ set image size to correct dimensions
        
        https://www.tutorialspoint.com/how-to-resize-an-image-using-tkinter
        resize only if x_size != image_x and/or y_size != image_y
        """
        if x_size == self.image_x and y_size == self.image_y:
            return

        if x_size > 0 and y_size > 0:
            self.image_x = x_size
            self.image_y = y_size
            self.resized.clear ()
            for item in self.list ():
                img = (Image.open (item))
                resize_img = img.resize ((x_size,y_size))
                self.resized.append (ImageTk.PhotoImage (resize_img))


if __name__ == '__main__':
    root = Tk ()
    pics = Pictures ("pictures") 
    # searchpath = os.path.join (pics.imagepath, "*.png")
    print (f"pictures: {pics.count()}")
    for img in pics.imagelist:
        print (img)

    print (f"Number of resized pics: {len(pics.resized)}")    
    pics.resize (25,25)
    print (f"Number of resized pics: {len(pics.resized)}")