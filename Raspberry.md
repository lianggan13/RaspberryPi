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



开发工具 
	vs code
	finalshell

VS Code SSH 远程
	安装插件 Remote - SSH
		Windows10 设置开发人员模式,安装 OpenSSH
		插件配置路径 C:\Windows\System32\OpenSSH\ssh.exe

	管理员身份打开 PowerShell
		ssh-keygen -t rsa -b 4096 // 4096 加密的深度
		(C:\Users\lianggan13/.ssh/id_rsa)
	
	打开 Linux 终端(树莓派)
	
		ssh-keygen -t rsa -b 4096
		cat id_rsa.pub >> authorized_keys
		sudo chmod 600 authorized_keys
		sudo chmod 700 -R .ssh
		
	同步 id_rsa 和 id_rsa.pub 文件
		
	sudo vi /etc/ssh/sshd_config
		PermitRootLogin yes
		RSAAuthentication yes
		PubkeyAuthentication yes
		AuthorizedKeysFile .ssh/authorized_keys

选择 Python 解释器
	命令盘(Ctrl + Shift + P)中输入: select interpreter





vim 常用指令


​	

Pioneer600
	使用教程 https://www.waveshare.net/wiki/Pioneer600
	RPI使用教程：提供BCM2835、WiringPi、文件IO、RPI（Python）库例程
	

https://blog.csdn.net/weixin_37988176/article/details/109423815