import machine
from machine import Pin
import network
import utime

import socket              
import network

import time

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

f = open("data.txt", "r", encoding="utf-8")
text = "a"

if __name__ == '__main__':
    start = time.time()
    while (text != ""):    
        text = f.read(1024)
        msg = input(text) 
        try:
            s.sendall(text) #入力された文字列を送信
        except OSError as e:
            f.close()
