SSID_NAME = "FIAPCourse"
SSID_PASS = "FIAPCourse"

import utime
import ntptime
import network

def ntp_sync():
    ntptime.settime()

def connect_wifi(ssid, passkey, timeout=10):
    wifi= network.WLAN(network.STA_IF)
    if wifi.isconnected() :
        print('already Connected.    connect skip')
        return wifi
    else :
        wifi.active(True)
        wifi.connect(ssid, passkey)
        while not wifi.isconnected() and timeout > 0:
            print('.')
            utime.sleep(1)
            timeout -= 1

    if wifi.isconnected():
        print('Connected')
        return wifi
    else:
        print('Connection failed!')
        return null

def disconnect_wifi():
    network.WLAN(network.STA_IF).active(False)

if __name__ == "__main__":
    wifi = connect_wifi(SSID_NAME, SSID_PASS)
    if wifi :
        ntp_sync()
    else:
        sys.exit(0)
