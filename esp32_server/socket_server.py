import socket #モジュールのインポート
import network
import machine
from machine import Pin

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

p2 = Pin(2, Pin.OUT)
SSID_ESP = {'ESP_D49C9D', 'ESP_D374C5'}

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
    #print(wifiName) #羅列が煩わしいので，デバッグ時は#外す
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

wifi.active(True)

def ap_mode():
    global ap
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    p2.on()
    print('enabled ap mode')
    config = ap.ifconfig()
    print(config) 

wifiscan()
connect_esp_wifi(timeout = 10)
ap_mode()

port = 80 #ポート指定
listenSocket = None #初期化



ip = wifi.ifconfig()[0] #自分のipアドレスを取得
listenSocket = socket.socket() #socketを作成
listenSocket.bind((ip, port)) # ソケットを特定のIPアドレスとポートに紐付け
listenSocket.listen(5) # 接続の待受を開始
listenSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,  1) #指定されたソケットオプションの値を設定

while True:
    print("accepting.....") 
    conn, addr = listenSocket.accept() #接続を受信
    print(addr, "connected") #接続した相手のipアドレスを表示　(xxx.xxx.xxx.xxx connected)

    while True:
        data = conn.recv(1024) #一度に受け取るデータのサイズを指定
        if(len(data) == 0):
            print("close socket")
            conn.close() #接続を切断
            break
        print(data)