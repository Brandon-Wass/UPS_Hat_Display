#!/usr/bin/env python

import json
import logging
import RPi.GPIO as GPIO
import smbus
import struct
import sys
from time import sleep

BATTERY_FILE_PATH = 'battery.json'
CHARGING_STATUS_PORT = 6
I2C_ADDR = 0x36

class BatteryMonitor:
    def __init__(self, bus_number=1, address=0x36):
        self.bus = smbus.SMBus(bus_number)
        self.address = address

    def readVoltage(self):
        try:
            read = self.bus.read_word_data(self.address, 2)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            return swapped * 1.25 / 1000 / 16
        except Exception as e:
            logging.error("Error reading voltage: %s", e)
            return None

    def readCapacity(self):
        try:
            read = self.bus.read_word_data(self.address, 4)
            swapped = struct.unpack("<H", struct.pack(">H", read))[0]
            capacity = min(swapped / 256, 99)
            return int(capacity)
        except Exception as e:
            logging.error("Error reading capacity: %s", e)
            return None

# Function to prepare capacity reading for display
def prepare_readCapacity(battery_monitor):
    capacity = battery_monitor.readCapacity()
    left_number = capacity // 10
    right_number = capacity % 10
    return left_number, right_number

# Function to prepare voltage reading for display
def prepare_readVoltage(battery_monitor):
    voltage = battery_monitor.readVoltage()
    if voltage > 3.70:
        return 'green'
    elif 3.40 <= voltage <= 3.70:
        return 'orange'
    elif voltage < 3.40:
        return 'red'

# Function to check charging status
def check_charge():
    charging_status = GPIO.input(CHARGING_STATUS_PORT)
    return 'on' if charging_status == 0 else 'off'

# Function to send status to JSON file
def send_status(left_number, right_number, percent_symbol, indicator_light):
    data = {
        'left': left_number,
        'right': right_number,
        'percent': percent_symbol,
        'indicator': indicator_light
    }
    with open(BATTERY_FILE_PATH, 'w') as f:
        json.dump(data, f)

##########

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHARGING_STATUS_PORT, GPIO.IN)

    battery_monitor = BatteryMonitor()

    try:
        while True:
            try:
                left_number, right_number = prepare_readCapacity(battery_monitor)
                percent_symbol = check_charge()
                indicator_light = prepare_readVoltage(battery_monitor)
                send_status(left_number, right_number, percent_symbol, indicator_light)
                sleep(5)
            except Exception as e:
                logging.error("An error occurred in the main loop: %s", e)
                sleep(1)
    finally:
        GPIO.cleanup()
        logging.info("GPIO cleanup complete.")

if __name__ == '__main__':
    main()

