# pixels

**pixels** is a Python script that draws circles or other objects on screen in a matrix of 16x9. Color, shape, size and more attributes can be modified. The modification of these attributes is done through byte values transmitted by OSC.

With the help of Open Lighting Architecture ([OLA](https://www.openlighting.org/)) a lighting desk with pixel mapping capabilities can light show on screen: Each pixel is represented by a LED spot in the lighting desk. In other words, **pixels** enables a light designer to produce video content.

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

**pixels** doesn't need an installation, just put all files of this repository into a folder of your choice, for example ~/Documents/python/pixels.

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

    I wrote a documentation of the steps you have to take. Have a look at Google groups here: https://groups.google.com/g/open-lighting/c/rDIbzhqnWxQ/m/W7c_xUznCAAJ and search for my contribution on 2020-07-14. Follow the steps until you find the line "At this point OLA is ready to use."


### Configure OLA

First, start the OLA Admin webpage: 127.0.0.1:9090

Here you create a new Universe and patch an available input, for example Enttec USB DMX pro or a network DMX protocol like ArtNet. 
