# Materials
This document describes the needed materials to modify a gunpla kit to use this software.  Individual guides contain specific list parts with regard to LEDs.

There are 2 ways to install LEDs, a soldered version and solderless.  

The soldered method is the preferred method and gives you far offers more flexibility in design, routing wires through the gunpla kit, etc.  It requires basic soldering skills, primarily joining wires together and soldering wires to the holes on the Raspberry Pi Pico W.  This is not covered in this project but tutorials can be found on youtube and the internet.  This solution is a more permanent solution and is usually more difficult to change.

The solderless method is an alternative for those:
* who do not have soldering skills or equipment
* who want an easy way to install things
* who are test building and designing lightshows
* who just try this repo out
It is also recommended to use the screw terminal boards listed in the [Solderless kit](#solderless-kit) for some time as it is easier to move LEDs to different pins while configs stabilize.

## Common Materials
This is a small list of common materials needed irregardless of Solder vs Non-Solder construction
* A gunpla kit
* [Drill bits](https://www.gundamplanet.com/db-03-tungsten-steel-drill-bit-set.html)
  * A 3/16th when resistor is needed
* Various hobby tools
  * Hobby knife, tweezers, wirecutters, etc for cutting gunpla, wires etc. 

## Solder Kit (Preferred Method)
The following is recommended if you know how to solder. 
* Soldering iron, lead-free solder, etc
* [Raspbery Pi Pico W](https://thepihut.com/products/raspberry-pi-pico-w?variant=41952994754755)
* [Pioc or Z LEDs in the appropriate color](https://evandesigns.com/products/chip-nano-pico-leds?variant=40800157204528)
  *  In ```3 volt DC``` option
* 15 ohm Resistor 1/2w (0.5Watt) ±1% 
  * The Raspberry Pi Pico board outputs a 3.3 volts but the 3 volt LED's need a resistor for it.
  * Evandesigns offers a ```5-12 volt DC``` variant that has a resistor presoldered.

Optional (But Recommended parts)
* [Shrink tube for resistor](https://evandesigns.com/products/shrink-tube?variant=6763932680240)
  * ```1/16th``` variant
  * This allows you to connect the LED wire to the resistor and secure the soldered joints
  * Electrical tape is also an option, but not as clean.
* Heat gun to shrink the tube or possible hair dryer
  * Various options exist across multiple pricepoints 
* [Additional wire](https://evandesigns.com/products/magnet-wire-twisted-50-ft-spool)
  * Larger kits may need additional wire spliced in to extend the LED wiring

## Solderless kit
This is very similar to the above but has some modifications for those that cannot or do not wish to solder wiring.
* [Raspberry Pi Pico WH](https://thepihut.com/products/raspberry-pi-pico-w?variant=41952994787523)
  * This has headers pre installed for an additional charge, but lets you plug in the Pico board into a common terminal.
* [Pico Or Z LEDs in the appropriate color](https://evandesigns.com/products/chip-nano-pico-leds?variant=32158377967664)
  * ```5-12 volt DC``` variant
    * This essentially is the ```3 volt DC``` but has a resistor pre-soldered in.  This resistance is incorrect, but will prevent LED's from burning out.
  * The wiring may be too short for this, but EvanDesigns may be able to custom offer longer versions.
* [Screw terminal board](https://www.amazon.com/naughtystarts-Brekaout-Soldered-Compatible-Raspberry/dp/B0B1H2S57S/)
  * There are various versions and makers that exist and any will do. This will let you wire in the LEDs to the Pico board and secure them by screwing down contacts.

## Developer kit
If you intend to write custom light shows or contribute to the project, having a dedicated test kit to debug effects, server operations, etc can be cumbersome.  So far it's recommended to use [this](https://thepihut.com/products/screw-terminal-expansion-board-for-raspberry-pi-pico) screw terminal development board. It allows easy modifications to wiring and has built in LED's to help debug without connecting to an existing kit.


