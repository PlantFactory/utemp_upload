import utime
import os

import machine
from uieee1888 import IEEE1888

def f2(i): return '{:0>2}'.format(i)

def read_temp(i2c):
    address = 0x48
    temp_reg = 0x00

    data = i2c.readfrom_mem(address, temp_reg, 2)
    value = data[0] << 8 | data[1]

    if (value >> 15 & 1):
        value /= -128.0
    else:
        value /= 128.0

    return value

def upload(client, i2c):
    now = utime.localtime(utime.time() + 60*60*9)
    nowStr = "%s-%s-%sT%s:%s:%s" % (str(now[0]), f2(now[1]), f2(now[2]), f2(now[3]), f2(now[4]), f2(now[5]))
    valStr = str(read_temp(i2c))
    print(nowStr)
    print(valStr)
    print(client.write([{ "id": "http://ujyu.net/micropython/Temperature", "time": nowStr, "value": valStr }]))

def main():
    vcc_pin = machine.Pin(5, machine.Pin.OUT)
    vcc_pin.on()

    client = IEEE1888("http://ants.jga.kisarazu.ac.jp/axis2/services/FIAPStorage")
    i2c = machine.I2C(scl=machine.Pin(18), sda=machine.Pin(19))

    epoch = 0
    prev_epoch = 0
    while True:
        epoch = utime.time()
        if epoch != prev_epoch:
            print(epoch)
            if epoch % 60 == 0:
                print("upload")
                upload(client, i2c)
        prev_epoch = epoch

if __name__ == "__main__":
    main()
