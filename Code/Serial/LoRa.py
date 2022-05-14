#!/usr/bin/env python
#    LoRa.py
#Communication module: LoRa.
#Communication method with device via LoRa.
#Uart port drive LoRa module.
#Parse JSON between device and gateway via LoRa channel.
#LoRa module: E32-TTL-100
#Pin specification:
#M0    <--> GPIO(OUT)     #mode setting
#M1    <--> GPIO(OUT)     #mode setting
#RXD   <--> 8(TXD)        #ttyS0
#TXD   <--> 10(RXD)       #ttyS0
#AUX   <--> GPIO/INT(IN)  #module status detecting
#VCC
#GND

#Install pyserial:
#pip install pyserial    #Python2
#pip3 install pyserial   #Python3

#Config UART port in raspberryPi:
#$ raspi-config
#Would you like a login shell to be accessible over serial? Choose No.
#Would you like the serial port hardware to be enabled?     Choose Yes.
#ttyS0 appear in /dev

import RPi.GPIO as GPIO
import serial  
import time  

M0 = 35
M1 = 37

GPIO.setmode(GPIO.BOARD)
GPIO.setup(M0,GPIO.OUT)
GPIO.setup(M1,GPIO.OUT)

GPIO.output(M0,GPIO.LOW)
GPIO.output(M1,GPIO.LOW)

# pyserial_test = serial.Serial("/dev/ttyS0", 115200)  
ser = serial.Serial("/dev/ttyS0", 9600)  
ser.bytesize = 8 #8位数据位

# ser.parity=serial.PARITY_EVEN#偶校验
ser.parity=serial.PARITY_NONE#无校验
# ser.parity=serial.PARITY_ODD#奇校验

ser.stopbits = 1        #停止位
ser.timeout= 5         #读超时设置
ser.writeTimeout = 2    #写超时
# ser.xonxoff=False       #软件流控
# ser.rtscts=False        #硬件流控
# ser.dsrdtr=False        #硬件流控

# flushInput()            # 丢弃接收缓存中的所有数据
# flushOutput()           # 终止当前写操作，并丢弃发送缓存中的数据。

print(f"start port: {ser.port}")

def main():  
    # pyserial_test.write('AAA'.encode("utf-8"))
    time.sleep(0.2)
    print("start recv...")
    while True:  
        count = ser.inWaiting()  
        if count != 0:  
            recv = "pi return: "+ser.read(count)+"\n"
            print(recv);  
            # pyserial_test.write(recv)
        else:
            print("no data")
            ser.write('AAA'.encode("utf-8"))
        # ser.flushInput()  
        time.sleep(0.1)  
  
if __name__ == '__main__':  
    try:  
        main()  
        GPIO.cleanup()
    except KeyboardInterrupt:  
        print("KeyboardInterrupt")
        GPIO.cleanup()
        if ser != None:  
            ser.close()  
