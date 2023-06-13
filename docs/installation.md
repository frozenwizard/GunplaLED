# Installation

The following describes how to set up the necessary software tooling and deploys software to the Pico board.

It is assumed that the user knows what a terminal, shell, etc is and how to use it, but has nothing configured on their
system. TODO: Link to an external overview of what the terminal and shell is, and how to use it

## Tooling Setup

### Prerequisites

#### macOS

Install [brew.sh](https://brew.sh) to install the macOS package manager

```shell
brew install pyenv git wget markdownlint-cli
```

#### GNU/Linux(Ubuntu)

```shell
sudo apt install pyenv git wget make markdownlint-cli
```

After this make sure Pyenv is enabled correctly on your [shell](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)

### Clone this repo

If you have not done so yet git clone this repo to your desired directory.  The green '<>code' button in GitHub will
give you options on how to do that.

### Install tooling

Run the following make command to download micropython, install python, python requirements and generate the config
file.  This is a one time setup.

```shell
make setup && pyenv activate gunpla
```

### Install MicroPython to the Raspberry Pico board

MicroPython needs to be installed on the board before the project can be deployed.  Plug a Micro-USB cable into the Pico
board, hold down the [bootsel button](https://projects-static.raspberrypi.org/projects/getting-started-with-the-pico/725a421f3b51a5674c539d6953db5f1892509475/en/images/Pico-bootsel.png)
and then plug the cable into your computer.  
This sets the Pico board as a usb mass storage device.  The following OS appropriate command will automatically deploy
MicroPython to the Pico board.

```shell
make install-micropython-osx
```

Or

```shell
make install-micropython-ubuntu
```

After completion the board will disappear as a device and reappear silently, so wait 10 seconds before continuing.

## Deploy the test build

The test build is a simple Python script that helps to make sure the tooling has been setup correctly and things work.
The test file will blink the onboard Pico LED several times and then stop. Run the following command, once the transfer
has completed, unplug the Raspberry Pi Pico W and then plug it back in.  You should see the onboard LEDs flash.

```shell
make build-test deploy
```

If there are any errors, they should be corrected before continuing to configure your gunpla.

## Deploy your gunpla server

Follow the steps in [configuring your gunpla](/docs/configuring_gunpla.md) to configure some important settings and make
any modifications. It is recommended to set the configuration to the GenericGundam and make sure all the settings are
correct before installing an LED's.  Afterwards, run the following to build and deploy your configuration to the Pico
board

```shell
make build deploy
```

Afterwards, you should be able to open a webpage to the hostname you set in the ```settings.py``` or find the IP address
in your routers connected device list.  If neither works, follow the [debugging guide](/docs/developer_setup.md)
