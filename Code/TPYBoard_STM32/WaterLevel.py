#Water level sensor.
#VCC 
#GND
#AO <--> ADC Port(A7) Analog data

#AO is the specific value.

import pyb
from pyb import Pin

adc = pyb.ADC(Pin('A7'))       # create an analog object from a pin
adc = pyb.ADC(pyb.Pin.board.A7)
# read an analog value

def getWaterLevel():               
    print('WaterLevel Ao')
    return adc.read()

def ADCDemo1():
    adc = pyb.ADC(Pin('Y11'))       # create an analog object from a pin
    # 8位最大255，10位最大1023，12位最大4095
    val = adc.read()                # read an analog value


def ADCDemo2():
    adc = pyb.ADC(pyb.Pin.board.X19)    # create an ADC on pin X19
    tim = pyb.Timer(6, freq=10)         # create a timer running at 10Hz
    buf = bytearray(100)                # creat a buffer to store the samples
    adc.read_timed(buf, tim)            # sample 100 values, taking 10s

def ADCDemo3():
    adc = pyb.ADC(pyb.Pin.board.X19)    # create an ADC on pin X19
    buf = bytearray(100)                # create a buffer of 100 bytes
    adc.read_timed(buf, 10)             # read analog values into buf at 10Hz
                                        #   this will take 10 seconds to finish
    for val in buf:                     # loop over all values
        print(val)                      # print the value out

def ADCDemo4():
    # resolution: 8/10/12
    adc = pyb.ADCAll(resolution)    # create an ADCAll object,分辨率（resolution=12）
    # channel: 16-temp 17-verf 18-bat
    val = adc.read_channel(channel) # read the given channel
    val = adc.read_core_temp()      # read MCU temperature
    val = adc.read_core_vbat()      # read MCU VBAT  后备电池电压（1.21v参考）
    val = adc.read_core_vref()      # read MCU VREF  3.3V电源作为参考基准电压
    
    # v33 = 3.3 * 1.21 / adc.read_core_vref()
    # vback = adc.read_core_vbat() * 1.21 / adc.read_core_vref()


if __name__ == "__main__":
    getWaterLevel()