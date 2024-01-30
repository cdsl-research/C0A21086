import os
import network
import machine
from machine import Pin, SoftI2C
import utime
import webrepl

# Wi-FiおよびWebREPLの設定

lab_wifi_pass = "Wi-Fiのパスワード"
SSID_NAME_LAB = ['Wi-FiのSSID']

machine.freq(240000000)

print('boot is ok')
utime.sleep(1)

f = open('data.txt', 'r')
try:
    data = f.read()
    size = len(data)
    #print(size)
    if size < 231660:
        execfile("temp_sensor.py")
    else:
        execfile("socket_client.py")
except MemoryError:
    execfile("socket_client.py")
f.close()
