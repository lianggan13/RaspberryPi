import paho.mqtt.client as mqtt 

# 回调函数。当尝试与 MQTT broker 建立连接时，触发该函数。
# client 是本次连接的客户端实例。
# userdata 是用户的信息，一般为空。但如果有需要，也可以通过 user_data_set 函数设置。
# flags 保存服务器响应标志的字典。
# rc 是响应码。
# 一般情况下，我们只需要关注 rc 响应码是否为 0 就可以了。
# 0: 连接成功
# 1: 连接失败-不正确的协议版本
# 2: 连接失败-无效的客户端标识符
# 3: 连接失败-服务器不可用
# 4: 连接失败-错误的用户名或密码
# 5: 连接失败-未授权
# 6-255: 未定义
# 如果是其它问题，可以检查网络情况，或者确认是否安装了 `paho-mqtt`。


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected success")
    else:
        print(f"Connected fail with code {rc}")

client = mqtt.Client() 
client.on_connect = on_connect 
client.connect("broker.emqx.io", 1883, 60) 
client.loop_forever()
