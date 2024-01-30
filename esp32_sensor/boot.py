import os
import network
import machine
from machine import Pin, SoftI2C
import utime
import webrepl

# Wi-FiおよびWebREPLの設定

lab_wifi_pass = "11n-ky56$HDxgp"
webrepl_pass = "cdsl"
SSID_NAME_LAB = ['CDSL-A910-11n']


# Wi-Fiスキャンを実行し、利用可能なWi-Fiネットワークのリストを取得する関数
def wifiscan(): 
    global wifi
    wifiList = wifi.scan()
    wifiAPDict = []
    for wl in wifiList:
        if wl[0].decode('utf-8') != '':
            wifiAPDict.append(wl[0].decode('utf-8'))
    return wifiAPDict

# 研究室Wi-Fiに接続する関数
def connect_lab_wifi(timeout = 10):
    global wifi
    if wifi.ifconfig()[0].split(".")[0] == "192":
        wifi.disconnect()
    else:
        pass
    
    endFlag = False
    wifiName = wifiscan()
    print(wifiName)
    # Wi-Fiネットワークのリストを走査し、指定されたSSIDに接続する
    for wn in wifiName:
        if wn in SSID_NAME_LAB:
            print(f"[{wn}]に接続します")
            wifi.connect(wn, lab_wifi_pass)
            while True:
                # Wi-Fi接続が完了するまで待機
                if wifi.ifconfig()[0].split(".")[0] == "192":
                    #p2.on()
                    endFlag = True
                    print("----  wifi is connected -----")
                    print(f"----[{wifi.ifconfig()[0]}]に接続----")
                    webrepl.start(password = webrepl_pass)#WebREPLを有効にする
                    break
                else:
                    utime.sleep(1)
            if endFlag == True:
                break
        if endFlag == True:
            break

machine.freq(240000000)

ap = None
# Wi-Fiステータスの初期化とWi-Fiインターフェースの有効化
wifiStatus = True
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print('boot is ok')
utime.sleep(1)
#execfile('main.py')# 'main.py'スクリプトを実行]
#connect_lab_wifi()
#execfile("current.py")
#execfile("temp_sensor.py")
#execfile("socket_client.py")
'''
f = open('test.txt', 'r')
try:
    data = f.read()
    size = len(data)
    #print(size)
    if size < 5:
        execfile("temp_sensor.py")
    else:
        execfile("socket_client.py")
except MemoryError:
    execfile("socket_client.py")
f.close()
'''