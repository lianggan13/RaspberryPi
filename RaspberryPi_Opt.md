## Raspberry

### Start

Keys: rpi-imager

```
https://www.raspberrypi.com/software/
```

### Image

Keys: sourelist --> aliyun

```
编辑 /etc/apt/sources.list 文件，这里推荐就用系统自带的 nano 命令编辑，命令如下：
sudo nano /etc/apt/sources.list

进入编辑界面，删除原有的内容，粘贴如下内容：
deb http://mirrors.aliyun.com/raspbian/raspbian/ bullseye  main non-free contrib rpi
deb-src http://mirrors.aliyun.com/raspbian/raspbian/ bullseye main non-free contrib rpi

更新软件索引清单
sudo apt-get update

比较索引清单更新依赖关系
sudo apt-get upgrade -y
```



### Vim

Keys: install & configure vim

```
dd		删除
yy		复制
p		粘贴
u		撤销	(windows Ctrl z)
Ctrl r	反撤销	(windows Ctrl y)

sudo apt install vim
sudo vi /etc/vim/vimrc
set nu  #显示行号
syntax on  #语法高亮
set tabstop=4  #tab退四格
```

### 

### Static IP

Keys: dhcpcd.conf (方式1)

```py
sudo vi /etc/dhcpcd.conf

interface eth0
inform 192.168.13.13
static routers=192.168.1.1
static domain_name_servers=114.114.114.114
noipv6

interface wlan0
static ip_address=192.168.2.21/24
static routers=192.168.2.1
static domain_name_servers=114.114.114.114
或者 桌面右上角右击 wireless & Wired Network Setttings

reboot

sudo ifconfig eth0 192.168.1.179
```

Keys: rc.local(方式2)

```
 sudo vi /etc/rc.local
 添加固定IP sudo ifconfig eth0 192.168.1.179
 操作系统启动时 会 自动调用 rc.local 脚本
 
 
```

Keys: 网络配置文件

	sudo vi /etc/network/interfaces
	sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
	sudo vi /etc/dhcpcd.conf

### Route

Keys: route.sh

```
#!/bin/bash

# add route for wlan0

echo "sudo route add  default gw 192.168.1.1 dev wlan0 metric 99"
sudo route add  default gw 192.168.1.1 dev wlan0 metric 99

echo "sudo route add  default gw 192.168.10.1 dev wlan0 metric 99"
sudo route add  default gw 192.168.10.1 dev wlan0 metric 99
```

Keys: profile.d

```
# cp and autostart
sudo cp route.sh /etc/profile.d/
```

https://github.com/Python-IoT/Smart-IoT-Planting-System

### Boot

Keys: sudo vi /boot/config.txt 

```
# uncomment to force a console size. By default it will be display's size minus
# overscan.
framebuffer_width=1920
framebuffer_height=1080

# uncomment if hdmi display is not detected and composite is being output
hdmi_force_hotplug=1
```

### Rmote 

Keys: SSH、Python

```
1.Visual Stuido Code & FinalShell

2.Windows10 设置开发人员模式,安装 OpenSSH

3.Install Remote - SSH & Remote - SSH: Editing Configuration Files on vs code
  configure ssh path: C:\Windows\System32\OpenSSH\ssh.exe

4.Run powershell cmd on windows: ssh-keygen -t rsa -b 4096
 (tip: C:\Users\lianggan13/.ssh/id_rsa)
 
5.Run cmds on linux:
	ssh-keygen -t rsa -b 4096
	
6.Copy id_rsa.pub from windows to linux

7.Run cmds on linux:
	cat .ssh/id_rsa.pub >> .ssh/authorized_keys
	sudo chmod 777 .ssh/authorized_keys
	sudo chmod 700 -R .ssh

8.sudo vi /etc/ssh/sshd_config
	PermitRootLogin yes
	PubkeyAuthentication yes
	AuthorizedKeysFile .ssh/authorized_keys

9.再次 ssh-keygen -t rsa -b 4096

10.添加 ssh-key to Github

11.git clone git@github.com:lianggan13/RaspberryPi.git
```

Keys: Visual Stuido Code

```
命令盘(Ctrl + Shift + P)中输入: select interpreter
```

Keys: SSH command

```
sudo service sshd restart 
```

### MQTT

Keys: paho-mqtt

```cmake
The MQTT Broker is the Server.
The MQTT Subscribers and Publishers are the Clients.

pip3 install paho-mqtt
```

Keys: mosquitto

```
sudo apt install mosquitto mosquitto-clients
sudo systemctl status mosquitto
mosquitto -v
sudo lsof -i:1883

mosquitto_sub -h localhost -t "mqtt/pimylifeup"
mosquitto_pub -h localhost -t "mqtt/pimylifeup" -m "Hello world"

mosquitto_passwd -c /etc/mosquitto/passwd gtwang
/etc/mosquitto/mosquitto.conf
    # 設定帳號密碼檔案
    password_file /etc/mosquitto/passwd
    # 禁止匿名登入
    allow_anonymous false
service mosquitto restart
mosquitto_sub -t gtwang/test -u gtwang -P secret123
mosquitto_pub -t gtwang/test -u gtwang -P secret123 -m "Hello, world!"


https://blog.csdn.net/lordwish/article/details/85006228
```

Key: hbmqtt

```
pip install "websockets==8.1"
pip install hbmqtt
hbmqtt
hbmqtt_sub --url mqtt://192.168.1.189:1883 -t /gateway
hbmqtt_pub --url mqtt://192.168.1.189:1883 -t /gateway -m Hi,gateway!
sub.py 


WARNING: The scripts hbmqtt, hbmqtt_pub and hbmqtt_sub are installed in '/home/pi/.local/bin' which is not on PATH.
Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
  
export PATH="~/.local/bin:$PATH"
echo $PATH
sudo vim /etc/profile
echo $PATH

Python 3.9.2 (default, Mar 12 2021, 04:06:34) 

https://github.com/beerfactory/hbmqtt.git
```

Key: amqtt

```
pip install amqtt

amqtt_sub --url mqtt://192.168.1.189:1883 -t /gateway
amqtt_pub --url mqtt://192.168.1.189:1883 -t /gateway -m Hi,gateway!


amqtt_sub --url mqtt://0.0.0.0:1883 -t /gateway
amqtt_pub --url mqtt://0.0.0.0:1883 -t /gateway -m Hi,gatew
```

### Python

Keys: Download &  Compile

```
$ sudo apt-get update
$ sudo apt-get upgrade -y

$ sudo apt-get install build-essential libsqlite3-dev sqlite3 bzip2 libbz2-dev

$ wget https://www.python.org/ftp/python/3.6.12/Python-3.6.12.tgz
$ tar zxvf Python-3.6.12.tgz
$ cd Python-3.6.12

$ sudo ./configure && sudo make && sudo make install
```

Keys: Soft links

```
$ python --version
Python 3.9.2

$ python3 --version
Python 3.6.12

$ which python
/usr/bin/python
$ which python3
/usr/local/bin/python3

$ sudo mv /usr/bin/python /usr/bin/python3.9.2
$ sudo ln -s /usr/local/bin/python3 /usr/bin/python

$ python --version
Python 3.6.12


$ which pip
/usr/bin/pip
$ which pip3
/usr/local/bin/pip3

$ sudo mv /usr/bin/pip  /usr/bin/pip3.9.2
$ sudo ln -s /usr/local/bin/pip3 /usr/bin/pip

$ pip --version
pip 18.1 from /usr/local/lib/python3.6/site-packages/pip (python 3.6)
```

Keys: Remove | Uninstall

```
$ sudo apt remove <Package>
$ sudo apt autoremove
```

Keys: Pi.GPIO、spidev

```
sudo apt-get install python3-dev

sudo apt-get install python3-rpi.gpio

sudo apt-get install python3-smbus

sudo apt-get install python3-serial

安装spidev库，SPI接口库函数

tar -xvf Spidev-3.1.tar.gz
sudo python setup.py install
```





### TCP/IP

```
http://www.python-exemplary.com/index_en.php?inhalt_links=navigation_en.inc.php&inhalt_mitte=raspi/en/communication.inc.php
```



### GPIO

```
sudo raspi-gpio get

```



### Samba

```
sudo apt-get install samba samba-common-bin

sudo vi /etc/samba/smb.conf
    #======================= Share Definitions =======================

    [homes]
       comment = /home/pi
       browseable = yes

    # By default, the home directories are exported read-only. Change the
    # next parameter to 'no' if you want to be able to write to them.
       read only = no

    # File creation mask is set to 0700 for security reasons. If you want to
    # create files with group=rw permissions, set next parameter to 0775.
       create mask = 0777

    # Directory creation mask is set to 0700 for security reasons. If you want to
    # create dirs. with group=rw permissions, set next parameter to 0775.
       directory mask = 0777

sudo /etc/init.d/smbd restart
sudo /etc/init.d/samba-ad-dc restart

sudo smbpasswd -a pi

win10
控制面板 >> 程序
	启动或关闭Windows功能
			>> SMB1.0/CIFS文件共享支持和SMB直通
	
Win+R >> regedit
	\HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\LanmanWorkstation\Parameters
		>>
			AllowInsecureGuestAuth = 1

```

### Install

```
# 安装包与软件
sudo apt install <package>
# 删除软件及其配置文件
apt-get --purge remove <package>
# 删除没用的依赖包
apt-get autoremove


pip install
pip uninstall

```

## TPYBoard-STM32

```

102资料下载
http://www.tpyboard.com/download/data/182.html

TPYBoard v102 micropython Python开发板 pyboard STM32F405

http://www.tpyboard.com/pythoneditor/

http://docs.tpyboard.com/zh/latest/

REPL
Putty
>>> help()
>>> help(pyb.LED)

Ctrl + D 软重启

出厂模式：按住usr键，按一下rst，然后led2和led3交替亮，当两个灯交替亮到三次，且均亮起时，松开usr
USB－HID模式：编辑 boot.py 文件，去掉了pyb.usb_mode('CDC+HID')前的注释符
安全模式：Usr + RST 按一下 等LED3 亮 松开 Usr



```

Keys: VSCode、Pymakr、Micropython IDE

```
Pymakr 
pymakr.json

{
	"address": "COM3",
	"username": "micro",
	"password": "python",
	"sync_folder": "/",
	"open_on_start": false,
	"sync_file_types": "py,txt,log,json,xml,html,js,css,mpy",
	"ctrl_c_on_connect": false,
	"safe_boot_on_upload": false,
	"py_ignore": [
		"pymakr.conf",
		".vscode",
		".gitignore",
		".git",
		"project.pymakr",
		"env",
		"venv"
	],
	"fast_upload": false,
	"sync_all_file_types": false,
	"auto_connect": true,
	"autoconnect_comport_manufacturers": [
		"Pycom",
		"Pycom Ltd.",
		"FTDI",
		"Microsoft",
		"Microchip Technology, Inc.",
		"1a86"
	]
}

Micropython IDE
```



### Serial

```
ref links:
https://www.waveshare.net/study/article-606-1.html

https://chinacqzgp.blog.csdn.net/article/details/116663317?spm=1001.2101.3001.6661.1&depth_1-utm_relevant_index=1

ref link:
https://blog.csdn.net/ShenZhen_zixian/article/details/119531639

如果同时打开了端口和shell打印，就只能用于shell调试，不能当普通串口使用，不然会导致串口数据传输不稳定，偶尔出现乱码

sudo apt-get install minicom

sudo vim /boot/config.txt
在最后一行添加 dtoverlay=pi3-miniuart-bt
sudo minicom -D /dev/ttyAMA0 -b115200

USB转TTL的模块

sudo apt-get install minicom

1：输入crtl+A，再输入E，可以打开串口发送显示（默认是关闭显示的），再操作一遍则是隐藏显示。
2：输入crtl+A，再输入Q，Enter，可以退出minicom窗口。

#!/usr/bin/python
# -*- coding:utf-8 -*-
import serial

#ser = serial.Serial("/dev/ttyAMA0",115200)
ser = serial.Serial("/dev/ttyS0",115200)

print("serial test start ...")
ser.write("Hello Wrold !!!\n")
try:
    while True:
        ser.write(ser.read())
except KeyboardInterrupt:
    if ser != None:
        ser.close()


sudo usermod -aG　dialout pi
```



## Github

Smart-IoT-Planting-System

Pioneer600
	使用教程 https://www.waveshare.net/wiki/Pioneer600
	RPI使用教程：提供BCM2835、WiringPi、文件IO、RPI（Python）库例程

https://blog.csdn.net/weixin_37988176/article/details/109423815