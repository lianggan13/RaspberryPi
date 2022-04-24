## Raspberry

### Configure Static IP
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
```

	网络配置文件
	sudo vi /etc/network/interfaces
	sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
	sudo vi /etc/dhcpcd.conf

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

8.sudo vi /etc/ssh/sshd_config:
	PermitRootLogin yes
	RSAAuthentication yes
	PubkeyAuthentication yes
	AuthorizedKeysFile .ssh/authorized_keys
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



### Linux Command

```
# 安装包与软件
sudo apt install <package>
# 删除软件及其配置文件
apt-get --purge remove <package>
# 删除没用的依赖包
apt-get autoremove
```







Pioneer600
	使用教程 https://www.waveshare.net/wiki/Pioneer600
	RPI使用教程：提供BCM2835、WiringPi、文件IO、RPI（Python）库例程

https://blog.csdn.net/weixin_37988176/article/details/109423815