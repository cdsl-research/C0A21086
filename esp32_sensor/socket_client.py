import machine
from machine import Pin
import network
import utime

import socket              
import network

import time
'''
from machine import Pin, I2C
from ina219 import INA219
from logging import INFO

SHUNT_OHMS = 0.1

i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()
'''
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

p2 = Pin(2, Pin.OUT)
SSID_ESP = {'ESP_2A7E89', 'ESP_D374C5'}

def wifiscan():
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode("utf-8") != "":
            wifiAPDict.append(wl[0].decode("utf-8"))
    return wifiAPDict

def connect_esp_wifi(timeout = 10):
    global wifi
    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    wifiName = wifiscan()
    print(wifiName) #羅列が煩わしいので，デバッグ時は#外す
    for wn in wifiName:
        if wn in SSID_ESP:
            print(f"---ESPのWi-Fi[{wn}]に接続します---")
            wifi.connect(wn)
            while True:
                if wifi.ifconfig()[0].split(".")[0] == "192":
                    p2.on()
                    print("---- wifi is connected ----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    return True
                else:
                    utime.sleep(1)

wifiscan()
connect_esp_wifi(timeout = 10)

s = socket.socket() #ソケットの作成
host = wifi.ifconfig()[2] #接続先のipアドレス
port = 80 #ポート指定

s.connect(socket.getaddrinfo(host, port)[0][-1]) #接続確立

#f = open("30KB.txt", "r", encoding="utf-8")
text = "a"
'''
g = open("el.txt", "w", encoding="utf-8")
g.write(" ")
g.close()
'''
if __name__ == '__main__':
    start = time.time()
    #while (True):
    for i in range(489):
        text = "a"*1024
        #print(text)
        #msg = input(text) 
        #end = time.time()
        try:
            s.sendall(text) #入力された文字列を送信
            #g = open("el.txt", "a", encoding="utf-8")
            #g.write("Bus Voltage: %.3f V\n" % ina.voltage())
            #g.write("Current: %.3f mA\n" % ina.current())
            #g.write("Power: %.3f mW\n" % ina.power())
            #g.close()
            #end = time.time_ns()
            #print(end - start)
        except OSError as e:
            #f.close()
            #f = open("time.txt", "w", encoding="utf-8")
            #f.write(str(end - start))
            #f.close()
            end = time.time()
            print(end - start)
    end = time.time()
    print(end - start)