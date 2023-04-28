# Tools for working with ST17H66 BLE 5 chipsets

[Lenzetech](https://www.lenzetech.com/) ST17H66 chipsets ([PDF datasheet](https://www.lenzetech.com/public/store/pdf/jsggs/ST17H66B2_BLE_SoC_Datasheet_v1.1.2.pdf) can be founnd in a number of home consumer IoTs - i.e. device tracking tags and RGB LED controllers.

Their tooling is based on Kiel IDE and a custom downloader.

There is no documentation / datasheet on how to prorgam the chip otehr than using their own LeKit tooling

This repo is a combination of ideas pulled from other makers on how to program and probe the ST17H66 chip over UART

# Main GUI

Top level, there is a simple GUI which allows you to connect to a chip over raw UART RX/TX lines and execute simple commands

# Notes

To get the chip into programming mode, the chip must detect a certain character sequence upon power-up at 9600 baud
This is quite sensitive: the chip needs to see this within 50-100ms of power-on, so if writing any code to do this, make sure you are polling on UART first, and that the pollnig is not stuck waiting for serial input (i.e. have a timeout). Also, take care to handle garbage data that might be seen on the line
Connect your UART (e.g. a USB to TTL device) to the RX (pin 5 named 'P9') and TX (pin 6 named 'P10')
Once connected and the UART flips to 115200 baud, one can send smiple commands over UART and await repsonse
So far, commands in use:
- rdrev
- rdreg
- wrreg
- er512
- er54k
- era4k
- cpbin <> <> <>


This is what the tool does when you hit Connect

Again, the tool provides this interace with the Execute section
