import sys

sys.path.append("")

from micropython import const

import uasyncio as asyncio
import aioble
import bluetooth

import random
import struct

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
# org.bluetooth.service.environmental_sensing
_ENV_SENSE_UUID = bluetooth.UUID(0x181A)
# org.bluetooth.characteristic.temperature
_ENV_SENSE_TEMP_UUID = bluetooth.UUID(0x2A6E)
# org.bluetooth.characteristic.gap.appearance.xml
_ADV_APPEARANCE_GENERIC_THERMOMETER = const(768)

# How frequently to send advertising beacons.
_ADV_INTERVAL_MS = 250_000


# Register GATT server.
temp_service = aioble.Service(_ENV_SENSE_UUID)
temp_characteristic = aioble.Characteristic(
    temp_service, _ENV_SENSE_TEMP_UUID, read=True, notify=True
)
aioble.register_services(temp_service)


# Helper to encode the temperature characteristic encoding (sint16, hundredths of a degree).
def _encode_temperature(temp_deg_c):
    return struct.pack("<20s", str(temp_deg_c))


# This would be periodically polling a hardware sensor.
async def sensor_task():
    #f = open("30KB.txt", "r", encoding="utf-8")
    text = "a"
    start = time.time()
    #while (text != ""):
    #while (True):
    for i in range(25000):
        #text = f.read(20)
        text = "a"*20
        temp_characteristic.write(_encode_temperature(text))
        #end = time.time()
        #print(end - start)
        await asyncio.sleep_ms(1)
        text = " "*20
    #f.close()
    text = " "*20
    end = time.time()
    print(end - start)

# Serially wait for connections. Don't advertise while a central is
# connected.
async def peripheral_task():
    while True:
        async with await aioble.advertise(
            _ADV_INTERVAL_MS,
            name="mpy-temp",
            services=[_ENV_SENSE_UUID],
            appearance=_ADV_APPEARANCE_GENERIC_THERMOMETER,
        ) as connection:
            print("Connection from", connection.device)
            await connection.disconnected()
'''
async def elec():
    g = open("elec.txt", "w", encoding="utf-8")
    g.write(" ")
    g.close()
    
    while True:
        g = open("elec.txt", "a", encoding="utf-8")
        g.write("Bus Voltage: %.3f V\n" % ina.voltage())
        g.write("Current: %.3f mA\n" % ina.current())
        g.write("Power: %.3f mW\n" % ina.power())
        g.close()
'''

# Run both tasks.
async def main():
    t1 = asyncio.create_task(sensor_task())
    t2 = asyncio.create_task(peripheral_task())
    #t3 = asyncio.create_task(elec())
    await asyncio.gather(t1, t2)
    #await asyncio.gather(t1, t2, t3)
    

asyncio.run(main())