"""
/**
  *****************************************************************************
  * @file           : psutil_monitor.py
  * @brief          : Monitoring system (CPU/RAM usage & Temperature)
  *                   and display to external LCD device
  *
  *****************************************************************************
  * @attention
  *
  *  2024 TeIn
  *  https://blog.naver.com/bieemiho92
  *
  *  Target :
  *      x86-64 PC / running ubuntu 22.04 LTS
  *
  *  (Tested) LCD Device :
  *     ESP8266 NodeMCU + 20x4 I2C CLCD
  *
  *
  * @note
  *   Ver.01 (2024/06) :
  *     - Initial Release
  *
  *****************************************************************************
  */
"""



# *****************************************************************************
import time
import psutil
import serial
from datetime import datetime
now = time


# *****************************************************************************
var_cpu_percentage_used = None
var_mem_percentage_used = None
var_mem_percentage_avail = None
var_temperature_all = None
var_temperature_cpu_core = None
var_temperature_cpu_package = None
var_uptime_raw_int = None
var_uptime_dd = None
var_uptime_hh = None
var_uptime_mm = None
var_uptime_ss = None
str_lcd_cpu_usage = None
str_lcd_mem_usage = None
str_lcd_currtime = None
str_lcd_uptime = None
str_lcd_temperature = None
str_lcd_total = None


# *****************************************************************************

### Open Serial Port
print (" >>> Starting Monitor...")
SERIAL_PORT = '/dev/ttyUSB0'
ser = serial.Serial(SERIAL_PORT, baudrate=115200, timeout=1)
ser.close()
ser.open()
# ser.close()
print (" >>> to stop, press [CTRL+C]")


### Do main rotines
while True :
    ### retrive values
    var_cpu_percentage_used     = psutil.cpu_percent(interval=1, percpu=False)      # cycles every 1 seconds.
    var_mem_percentage_used     = psutil.virtual_memory().percent
    var_mem_percentage_avail    = ((psutil.virtual_memory().free)/(psutil.virtual_memory().total))*100.0

    var_temperature_all         = psutil.sensors_temperatures()
    var_temperature_cpu_core    = var_temperature_all['coretemp']
    var_temperature_cpu_package = var_temperature_cpu_core[0]

    var_uptime_raw_int  = int(time.monotonic())
    var_uptime_dd       = format(int(var_uptime_raw_int/(60*60*24)), '03')
    var_uptime_hh       = format(int((var_uptime_raw_int%(60*60*24))/(60*60)), '02')
    var_uptime_mm       = format(int((var_uptime_raw_int%(60*60))/60), '02')
    var_uptime_ss       = format((var_uptime_raw_int%60), '02')

    ### create string
    # str_lcd_currtime    =            str(now.strftime('%y-%m-%d %H:%M:%S')) + "\n"
    str_lcd_uptime      = "UP  " + str(var_uptime_dd) + "D " + str(var_uptime_hh) + ":" + str(var_uptime_mm) + ":" + str(var_uptime_ss) + "\n"
    str_lcd_cpu_usage   = "CPU(%) :   " + str(var_cpu_percentage_used) + "\n"
    str_lcd_mem_usage   = "MEM(%) :   " + str(var_mem_percentage_used) + "\n"
    str_lcd_temperature = "TEMP   :   " + str(var_temperature_cpu_package.current) + " 'C\n"

    ### merge to single string
    str_lcd_total = str_lcd_uptime + str_lcd_cpu_usage + str_lcd_mem_usage + str_lcd_temperature

    ### Display!
    ser.write(str.encode(str_lcd_total))
###

# ***************************************************************** END OF FILE
