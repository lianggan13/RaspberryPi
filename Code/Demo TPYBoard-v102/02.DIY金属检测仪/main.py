# main.py -- put your code here!
import pyb
from machine import Pin

y1 = Pin('Y1', Pin.IN)
x1 = Pin('X1', Pin.OUT_PP)

while 1:
    #�޽���ʱ
    if y1.value() == 1 :
        print(y1.value())
        x1.value(0)
    #�н���ʱ
    else:
        print(y1.value())
        x1.value(1)