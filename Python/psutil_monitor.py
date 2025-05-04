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
  *   Ver.03 (2025/05) :
  *     - add display for total incoming/outoging bytes
  *     - layout change     
  *
  *   Ver.02 (2024/12) :
  *     - add network up/down indicator
  *     - minor layout change
  *
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

### Ver. 02
var_net_init_stat = None
var_net_updt_stat = None
var_up_rate = None
var_dl_rate = None
str_up_ind  = None
str_dl_ind  = None

### Ver.03
var_net_totalTx_MBytes = None
var_net_totalRx_MBytes = None
str_lcd_header1 = None
str_lcd_value1= None
str_lcd_totalXferByte = None

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
    
    var_net_init_stat           = psutil.net_io_counters()                          # Ver02  get initial xfer 
    
    var_cpu_percentage_used     = psutil.cpu_percent(interval=1, percpu=False)      # cycles every 1 seconds.
    var_mem_percentage_used     = psutil.virtual_memory().percent
    var_mem_percentage_avail    = ((psutil.virtual_memory().free)/(psutil.virtual_memory().total))*100.0

    var_net_updt_stat           = psutil.net_io_counters()                          # Ver02  get updated xfer 

    var_temperature_all         = psutil.sensors_temperatures()
    var_temperature_cpu_core    = var_temperature_all['coretemp']
    var_temperature_cpu_package = var_temperature_cpu_core[0]

    var_uptime_raw_int  = int(time.monotonic())
    var_uptime_dd       = format(int(var_uptime_raw_int/(60*60*24)), '03')
    var_uptime_hh       = format(int((var_uptime_raw_int%(60*60*24))/(60*60)), '02')
    var_uptime_mm       = format(int((var_uptime_raw_int%(60*60))/60), '02')
    var_uptime_ss       = format((var_uptime_raw_int%60), '02')

    var_up_rate         = (var_net_updt_stat.bytes_sent - var_net_init_stat.bytes_sent) / 1
    var_dl_rate         = (var_net_updt_stat.bytes_recv - var_net_init_stat.bytes_recv) / 1

    if (var_up_rate > 1024) :
      str_up_ind = '^'        
    else :
      str_up_ind = '-'

    if (var_dl_rate > 1024) :
      str_dl_ind = 'v'        
    else :
      str_dl_ind = '-'

    # Ver03 new
    var_net_totalTx_MBytes = int( ((var_net_updt_stat.bytes_sent) / 1000000) )
    var_net_totalRx_MBytes = int( ((var_net_updt_stat.bytes_recv) / 1000000) )

    ### create string
    # str_lcd_currtime    =            str(now.strftime('%y-%m-%d %H:%M:%S')) + "\n"
    # str_lcd_uptime      = "> " + str(var_uptime_dd) + "D " + str(var_uptime_hh) + ":" + str(var_uptime_mm) + ":" + str(var_uptime_ss) + "\n"  # Ver02
    str_lcd_uptime      = "> " + str(var_uptime_dd) + "D " + str(var_uptime_hh) + ":" + str(var_uptime_mm) + ":" + str(var_uptime_ss) + " " + str_up_ind + "|" + str_dl_ind + "\n"   # Ver02
    
    # ~Ver02
    str_lcd_cpu_usage   = "CPU ( %): " + str(var_cpu_percentage_used) + "  \n"
    str_lcd_mem_usage   = "MEM ( %): " + str(var_mem_percentage_used) + "  \n"
    str_lcd_temperature = "TEMP('C): " + str(var_temperature_cpu_package.current) + "\n"

    # Ver03 new
    str_lcd_header1     = "CPU%  MEM%  TEMP'c\n"
    str_lcd_value1      = str(int(var_cpu_percentage_used)).zfill(3) + "   " + str(int(var_mem_percentage_used)).zfill(3) + "   " + str(int(var_temperature_cpu_package.current)).zfill(3) + "\n"
    str_lcd_totalXferByte = "T " + str(var_net_totalTx_MBytes).zfill(7) + " R " + str(var_net_totalRx_MBytes).zfill(7) + "\n"
    
    ### merge to single string
    # ~Ver02
    # str_lcd_total = str_lcd_uptime + str_lcd_cpu_usage + str_lcd_mem_usage + str_lcd_temperature
    
    # Ver03
    str_lcd_total = str_lcd_uptime + str_lcd_header1 + str_lcd_value1 + str_lcd_totalXferByte

    ### Display!
    ser.write(str.encode(str_lcd_total))
###

# ***************************************************************** END OF FILE
