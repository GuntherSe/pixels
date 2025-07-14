# pixels

**pixels** is a collection of Python scripts that draw circles or other objects on screen in a matrix of 16x9. Color, shape, size and more attributes can be modified. The modification of these attributes is done through byte values transmitted by OSC.

With the help of Open Lighting Architecture ([OLA](https://www.openlighting.org/)) a lighting desk with pixel mapping capabilities can produce a light show on screen: Each pixel is represented by a LED spot in the lighting desk. In other words, **pixels** enables a light designer to produce video content.

## Hardware and OS

**pixels** is written in Python, therefore it is platform independent. It was developed on a Windows machine and tested on Raspberry PI and various Debian machines. I recommend using a Linux machine, where you can run **pixels** and OLA simultaneously. 

## Installation

**pixels** needs a few packages to run: Tkinter, Pillow, python-osc. Here you'll find instructions to install these packages. If you need further info, please follow these links:

[Tkinter](https://tkdocs.com/tutorial/install.html#install-x11-python)

[Pillow](https://pypi.org/project/Pillow/)

[python-osc](https://pypi.org/project/python-osc/)

    sudo apt install python3-tk python3-venv
    cd ~
    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install python-osc
    python3 -m pip install Pillow

**pixels** doesn't need an installation, just put all files of this repository into a folder of your choice, for example ~/Documents/python/pixels. For your convenience it's recommended to set the execute flag on the shell scripts, then you can start the scripts quicker:

    chmod +x *.sh

### Install OLA

OLA needs an installation, this can be done either with apt or by downloading the latest version from Github and compiling it. I'll describe both versions.

* Install OLA with apt: 

        sudo nano /etc/apt/sources.list

    If you are on a Raspberry PI, add the following line at the end of the file:

        deb http://apt.openlighting.org/raspbian wheezy main

    If you are on a Debian computer, add the following line:

        deb http://apt.openlighting.org/debian wheezy main

    After restarting the computer, OLA can be installed:

        sudo apt install ola

* Install the latest OLA version from Github:

    For the use of **pixels** there is no need to install the latest version of OLA from Github. If you plan to use OLA with DMX hardware, it might be necessary to go through the process of installing from Github (the use of Eurolite DMX adapter is such a case).

    I wrote a documentation of the steps you have to take. Have a look at Google groups here: https://groups.google.com/g/open-lighting/c/rDIbzhqnWxQ/m/W7c_xUznCAAJ and search for my contribution on 2025-07-14. Follow the steps until you reach the instructions for Eurolite USB.


### Configure OLA

OLA is needed to convert DMX data to OSC, which is the input information for **pixels**. First, start the OLA Admin webpage: 127.0.0.1:9090

Here you create a new Universe and patch an available input, for example Enttec USB DMX Pro or a network DMX protocol like ArtNet. 

As an output, you have to configure OLA to send OSC data to **pixels**, it listens to /ola2screen on port 8000. This is the OSC information you have to tell OLA. Edit the config file ola-osc.conf (not sure where to find it? Have a look at the plugins page on the OLA Admin webpage, it's most probably /etc/ola/ola-osc.conf or /home/\<user>/.ola/ola-osc.conf)

    sudo nano /etc/ola/ola-osc.conf

    Here: port_0_targets = 127.0.0.1:8000/ola2screen

After saving the config file, restart the plugins, and pixels is ready for receiving data from your light-desk.

## Play with pixels

After having installed the Python packages and OLA, you are ready to run three different video processing tools: colorscreen, a 16 x 9 circle matrix and a 16 x 9 pixel matrix. The pixel matrix was part of a performance project, it's the more versatile variation of the three software versions.

### First step:

Let's do it step by step. We start the **colorscreen** script in a terminal:

    bash ~/Documents/python/pixels/startcolorscreen.py

you should see a black rectangle on the screen.

We test the functionality by changing the DMX values manually in OLA. Start your browser and navigate to the OLA admin page (127.0.0.1:9090). Open the DMX console tab and move the first fader, that is DMX 1. The rectangle should change it's color to red. The second fader is DMX 2, which represents the color green, the third fader (DMX 3) represents blue.

You have to remember a few keybord commands for the **pixels** software, they are the same on the three versions (colorscreen, circles and pixels):

* **Q**  and **\<Ctrl>+W**   quit the app.
* **F**  and **\<F11>**   toggle between window and fullscreen mode

### Second step:

At this point you are ready to use a lightdesk for changing the color of your screen. Just patch a RGB LED to your setting, on the universe you are going to send to OLA. Start address of the LED is 1. 

I use Art-Net to transfer data from the lightdesk to **pixels**. Have a look in the manual of your lightdesk to find out how Art-Net output is configured. Here is a remark on unsing Art-Net in OLA: Every universe in OLA has an ID. In my configuration I have created in OLA a universe with ID 5. When I configure Art-Net as input, the Art-Net universe is 0:0:5. 

### Third step:

We are almost ready to take off. We quit the **colorscreen** script andstart the **circles** script now:

    bash ~/Documents/python/pixels/startcircles.py

Here we have 145 RGB-LED to play with, a matrix of 16 x 9 circles, which are 144 LED for the circles, and 1 LED for background color. That is, we can play with 435 DMX addresses.

Let's look at the first circle in the top left corner. It's DMX addresses are 1-3, and the circle is handled like a RGB LED with a virtual intensity dimmer. That means, the intensity is the highest of the three DMX values. It defines the radius of the circle. The ratio between the three DMX values defines the color of the circle.

Have a look at the screen: If you use just one color, e.g. red, and slide from 0 to 100 % on your light software, you'll see a red dot growing to a red circle.

### Fourth step:

The third variant, the **pixel** script, is a little bit under construction. It has almost too many possibilities: 

* A matrix of 16 x 9 pixels, each pixel with individual RGB color. (DMX 1 - 432)
* Background color (DMX 433 - 435)
* Switch for more options, common to all pixels. (DMX 436)
If more options are switched on, then the following modifications of the pixels are possible. Due to the limitation of a DMX universe with 512 values, the modifications are common to all pixels:
* pixel x-size (DMX 437)
* pixel y-size (DMX 438)
* smoothness (DMX 439):   With DMX 439 the pixels appear as squares, increasing value of DMX 439 adds corners to the edges of the square, the form of the pixels change to diamonds, octacon, ...
* outline color (DMX 440-442)
* outline width (DMX 443)
* blur effect (DMX 444): This is not a real blur effect, but it darkens the color of the outline.
* use image switch (DMX 445): With this swich on, you can place images instead of pixels.

TODO: descrption of the image usage

### Final step:

Create shortcuts for starting the desired **pixels**-script. Or create an autostart script.

TODO: instructions ...

## And now ...

work on your lighting desk and have fun!


