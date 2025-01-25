# epd-pico-example

## Pervasive Displays E-Paper Display Pico Kit

[Pervasive Displays E-Paper Display Pico Kit](https://www.pervasivedisplays.com/product/epd-pico-kit-epdk/)

EPD Pico Kit (EPDK) is our new development kit consisting of [EPD Extension board](https://docs.pervasivedisplays.com/epd-usage/extension-kits/ext3-1) (EXT3), [Raspberry Pi Pico (RP2040)](https://www.raspberrypi.com/products/raspberry-pi-pico/) and [2.66 inch E ink Display](https://www.pervasivedisplays.com/product/2-66-e-ink-displays/) with built-in Pervasive Displays Library Suite (PDLS) to provide you a powerful, rich and comprehensive key parts to kick-start your low power display devices for any interactive, visual experience, ultra-fast refresh and eco-friendly IoT (Internet of Things) and HMI (Human Machine Interface) applications.

## Arduino example

Customized example based of [EPD_Driver Demo](https://github.com/PervasiveDisplays/EPD_Driver_GU_small/tree/main/examples/Demo_271)

## MicroPython example
![Micropython](micropython/micropython.png)
Ported from [driver](https://github.com/PervasiveDisplays/EPD_Driver_GU_small)

## CircuitPython example
![CircuitPython](circuitpython/blinka.bmp)

EPD driver depends on:
* [Adafruit CircuitPython EPD](https://github.com/adafruit/Adafruit_CircuitPython_EPD)
* [font5x8.bin found in the examples bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle)
* [Blinka bitmap](https://cdn-learn.adafruit.com/assets/assets/000/057/705/original/adafruit_products_blinka.bmp) 

Customized example based of [CircuitPython displayio driver for Pervasive Displays Spectra-based iTC/COG ePaper Displays](https://github.com/fergbrain/Fergcorp_CircuitPython_PDISpectra)