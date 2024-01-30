from machine import Pin, I2C, RTC
from ina219 import INA219
from logging import INFO
from utime import sleep,localtime
import _thread
import os

rtc = RTC()

SHUNT_OHMS = 0.1

i2c = I2C(-1, scl=Pin(22), sda=Pin(21))
ina = INA219(SHUNT_OHMS, i2c, log_level=INFO)
ina.configure()

# f = open('osawa.csv', 'a')
# f.write("start")
# f.write("\n")

def write():
    with open("current.log","a") as f:
        for i in range(100):
            f.write(str(i)+",")
            f.write(str(localtime())+",")
            print(localtime())
            f.write(f"Bus Voltage: {ina.voltage()}V,")
            f.write(f"Current: {ina.current()}mA,")
            f.write(f"Power: {ina.power()}mW\n")
            print(f"Power: {ina.power()}mW\n")
            sleep(1)

def write_csv():
    TIME_INTERVAL = 5
    initial = "begin"
    f = open('current.csv', 'a')
    f.write(initial)
    f.write("\n")
    f.close()
    
    while True:
        text = ""
        volt = ina.voltage()
        current = ina.current()
        power = ina.power()
        sumCurrent2 = 0.0
        count = 0
        # while count < TIME_INTERVAL:
        #     count += 1
        #     current = ina.current()
        #     sumCurrent2 += current
        #     print(f"current : {current} mA, voltage : {volt} V (count : {count})")
        #     utime.sleep(1)

        text = str(rtc.datetime()[5:7]) + "," + str(power)
        print(ina.power())
        f = open('current.csv', 'a') 
        f.write(text)
        f.write("\n")
        f.close()
        #  上のコメントアウトを外す時は下記をコメントアウト
        sleep(1)

def delete():
    _thread.exit()
    os.remove('current_M3.csv')

_thread.start_new_thread(write_csv,())