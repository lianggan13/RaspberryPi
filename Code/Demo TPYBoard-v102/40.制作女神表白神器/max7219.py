import pyb
from pyb import Pin
import font_max7219

#8*8����������
class Lattice():

    def __init__(self,clk,cs,din,num=1):
        
        self.P_CLK = Pin(clk,Pin.OUT_PP)
        self.P_CS = Pin(cs,Pin.OUT_PP)
        self.P_DIN = Pin(din,Pin.OUT_PP)
        
        self.font = font_max7219.FONT8_8
        self.num = num
        self.write_data(0x09, 0x00)#���뷽ʽ��BCD��
        self.write_data(0x0a, 0x03)#����
        self.write_data(0x0b, 0x07)#ɨ����ޣ�8���������ʾ
        self.write_data(0x0c, 0x01)#����ģʽ��0����ͨģʽ��1
        self.write_data(0x0f, 0x00)#��ʾ���ԣ�1�����Խ�����������ʾ��0
            
    def write_byte(self,data):
        for i in range(8):
            self.P_CLK.value(0)
            self.P_DIN.value(data&0x80)
            data <<= 1
            self.P_CLK.value(1)

    def write_data(self,addr,dat):
        self.P_CS.value(0)
        for i in range(self.num):
            self.write_byte(addr)
            self.write_byte(dat)
        self.P_CS.value(1)
        pyb.udelay(1)
    def display(self,msg):
        for i in msg:
            if i in self.font.keys():
                DATA = self.font[i]
                for k,d in enumerate(DATA):
                    self.write_data(k+1,d)
                pyb.delay(1500)