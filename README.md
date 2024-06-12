# CLCD_SysMon
![Alt text](https://github.com/TerraIncognitaKR/CLCD_SysMon/blob/main/_ImageRes/CLCD_SysMon_Running.jpg)
## (Linux PC + Python) x (ESP8266 + I2C CLCD) = 'Real' System Monitor Gadget
***
### Device : ESP8266 + 20x4 I2C CLCD

use **ESP8266_SERIAL_TO_I2C_CLCD.ino**. 

I used the ESP8266 NodeMCU, but maybe use it on other Arduino-Like boards with a little modification to the code. Any target devices/MCUs that supports UART will probably work. (NOT tested with other target board/MCUs.)

There are some pictures in "_ImageRes" directory for hardware reference.


***
### PC : 

connect device & run **psutil_monitor.py**. root privileges may be required. (use _sudo_)

by default, it works when your device is recognized as /dev/ttyUSB0. if it doesn't fit, edit python script. 

    SERIAL_PORT = '/dev/ttyUSB0'



***
### Display Info :

updates every 1 seconds.

1. System Uptime (DDD HH:MM:SS)
2. CPU Usage (%) 
3. RAM Usage (%)
4. Temperature of CPU Package (℃)

