# PS2-Nano-Remote

<img src="https://github.com/GorGylka/PS2-Nano-Remote/blob/main/test.gif">  
<img src="https://github.com/GorGylka/PS2-Nano-Remote/blob/main/ps2_remote1.jpg" width=40% height=40%">  
Nano remote control to On / Off / Reset PS2 ( from SCPH-5000x to SCPH-9000x )  

Easy build (4 parts), nano size, minimal power consumption  


<h3 align="left">You will need:</h3> 

  
- RP2040 Zero  
- IR Diode
  
(If you want a portable keychain)
- CR2032 Coin Battery  
- Tact Button  

<img src="https://github.com/GorGylka/PS2-Nano-Remote/blob/main/ps2_remote.jpg" width=40% height=40%>

<h2 align="left">Firmware:</h3>  

- Install [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) to RP2040 Zero  
- Install [Thonny](https://thonny.org), connect Pico ( ```Tools``` -> ```Options``` -> ```Interpreter``` -> ```MicroPython (Raspberry Pi Pico)``` -> ```OK```)  
- Save Main.py to RP2040 Zero
  
If it's buggy (reset twice instead of turning off) Play with 3 values: ```HOLD_TIME``` (seconds),  ```INTER_REPEAT_MS``` (Miniseconds),  ```CARRIER_DUTY``` (LED brightness, 65536 - 0)
