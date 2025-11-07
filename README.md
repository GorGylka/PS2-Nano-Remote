# PS2-Nano-Remote
Nano remote control to On / Off / Reset PS2 ( from SCPH-5000x to SCPH-9000x )

<h3 align="left">You will need:</h3> 

  
- RP2040 Zero  
- IR Diode
  
(If you want a portable keychain)
- CR2032 Coin Battery  
- Tact Button  

<img src="https://github.com/GorGylka/PS2-Nano-Remote/blob/main/ps2_remote.jpg" width=40% height=40%>

<h2 align="left">Firmware:</h2>  

- Install [MicroPython](https://www.raspberrypi.com/documentation/microcontrollers/micropython.html) to RP2040 Zero  
- Install [Thonny](https://thonny.org)
- Save Main.py to RP2040 Zero
  
Play with 3 values: ```HOLD_TIME``` (seconds),  ```INTER_REPEAT_MS``` (Miniseconds),  ```CARRIER_DUTY``` (LED brightness, 65536 - 0)
