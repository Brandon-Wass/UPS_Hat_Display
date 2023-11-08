#!/usr/bin/env python

import json
import logging
import RPi.GPIO as GPIO
import smbus
import struct
import sys
from time import sleep

##########

BATTERY_FILE_PATH = 'battery.json'  # Path to write to battery.json file
CHARGING_STATUS_PORT = 6
I2C_ADDR=0x36 # Address of the I2C battery fuel gauging chip on x728 V-2.3 UPS hat
bus = smbus.SMBus(1)  # 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

##########

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(CHARGING_STATUS_PORT, GPIO.IN)

##########

# Function to read voltage from the fuel gauge
def readVoltage(bus):
    address = I2C_ADDR
    read = bus.read_word_data(address, 2)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    voltage = swapped * 1.25 /1000/16
    return voltage

# Function to read capacity from the fuel gauge
def readCapacity(bus):
    address = I2C_ADDR
    read = bus.read_word_data(address, 4)
    swapped = struct.unpack("<H", struct.pack(">H", read))[0]
    capacity = swapped / 256
    if capacity > 99:
        capacity = 99
    return int(capacity)

# Function to prepare capacity reading for display
def prepare_readCapacity(bus):
    capacity = readCapacity(bus)
    left_number = capacity // 10
    right_number = capacity % 10
    return left_number, right_number

# Function to prepare voltage reading for display
def prepare_readVoltage(bus):
    voltage = readVoltage(bus)
    if voltage > 3.80:
        return 'green'
    elif 3.40 <= voltage <= 3.80:
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
    try:
        while True:
            try:
                left_number, right_number = prepare_readCapacity(bus)
                percent_symbol = check_charge()
                indicator_light = prepare_readVoltage(bus)
                send_status(left_number, right_number, percent_symbol, indicator_light)
                sleep(5)  # Read and send new data to battery.json file every 5 seconds
            except Exception as e:
                logging.error("An error occurred: %s", e)
                sleep(1)  # Wait a bit before retrying to prevent a spam of error messages
    finally:
        GPIO.cleanup()
        logging.info("GPIO cleanup complete.")

if __name__ == '__main__':
    main()
