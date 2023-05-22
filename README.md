# GunplaLED

## What is this?
This repo contains Python code that deploys to a [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w-and-pico-wh) that runs a web server allowing you to control individual LED's or program lightshows for a Gundam (or other gunpla) model kit.

## Why?
When I was building RX-93 Nu Gundam ver ka, it lets you use a green LED module to light up the head.  It was basically out of stock everywhere, so I had to look for alternatives.  I also didn't like the idea of not having easy access to the on/off of the LED and having to replace batteries.  So I wanted something more hardwired into an outlet that I could plug/unplug.  I also do a lot of home automation, so I thought it'd be cool to have it connected to a smart plug.  Seeing others on r/gunpla do more complicated LED setups and all the above made me think of running some sort of server I can cURL to make it light up.  Then research led me here.  
**tl;dr** A Pico W and green LED is about the same cost as the official LED module but cooler.

## Goals of this project
* Be simple for anyone not technical to install and configure LEDs to their gunpla
* Widespread Gunpla kit support
* Simple installation and configuration
* Eventual support of additional microcontrollers
* Widespread community support

## Project Status
This project is in early alpha.  It is considered to be functional and fulfills the minimum requirements of hosting a webserver that can control individual LEDs.  However, there is still much to be done in terms of adding support for more gunpla models, expanding lightshows, bug fixes, etc.  Therefore, until this project hits beta, there is no backwards support as areas of the codebase are rapidly changing and improving.  Thus, when upgrading, it is recommended to start from the initial setup.

# Installation
At this time installation requires setting up a local Python development environment as some of the tooling requires it.  The recommended OS's are Linux and MacOS.  Windows is not currently supported but is on the roadmap as it has a more complicated way of talking to the Raspberry Pi.
See [asdf](docs/installation.md) for a full walkthrough of how to 
## Requirements
* cli: make, python, pip, pyenv (optional)

# Developer Setup
The developer setup to add and contribute to the project mainly consists of setting up an IDE environment.  Please follow the process in [asdf](docs/installation.md) before continuing.
The recommended IDE is [Pycharm Community](https://www.jetbrains.com/pycharm). You will need to install the [micropython plugin](https://plugins.jetbrains.com/plugin/9777-micropython).


# Contributing
Contributions are very much welcome.  For bugs and/or feature requests file a [issue]().  If you'd like to contribute to a specific area such as HTML, additonal kit support, etc submit an issue as well.

# Roadmap
* Better documentation for installation of each LED's on each kit
* More Gunpla model support 
* Windows support
* Better UI
* More lightshows and LED effects
* Easier installation and configuration
* Internal webserver

