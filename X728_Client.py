import json
import RPi.GPIO as GPIO
import sys
from threading import Thread, Event
from time import sleep

# Constants
REFRESH_RATE = 0.001  # Refresh rate for display update
BATTERY_FILE_PATH = 'battery.json'  # Path to read and parse battery.json file

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pins = {
    'Pin1': 17, 'Pin2': 27, 'Pin3': 22, 'Pin4': 23, 'Pin5': 24,
}

# Define set_segment function to control the segments
def set_segment(pin_high, pin_low):
    # Set all pins to input (high-impedance) first
    for pin in pins.values():
        GPIO.setup(pin, GPIO.IN)

    # Now, only set the two pins we're interested in to output
    GPIO.setup(pin_high, GPIO.OUT)
    GPIO.setup(pin_low, GPIO.OUT)

    # Drive the selected segment
    GPIO.output(pin_high, GPIO.HIGH)
    GPIO.output(pin_low, GPIO.LOW)

# Define clear_segments function
def clear_segments():
    # This function now sets all pins to input mode to 'turn off' all segments.
    for pin in pins.values():
        GPIO.setup(pin, GPIO.IN)

# Segment control functions for the left side
def Left_Top():
    set_segment(pins['Pin1'], pins['Pin2'])

def Left_Top_Left():
    set_segment(pins['Pin1'], pins['Pin4'])

def Left_Top_Right():
    set_segment(pins['Pin2'], pins['Pin1'])

def Left_Middle():
    set_segment(pins['Pin2'], pins['Pin4'])

def Left_Bottom_Left():
    set_segment(pins['Pin1'], pins['Pin3'])

def Left_Bottom_Right():
    set_segment(pins['Pin2'], pins['Pin3'])

def Left_Bottom():
    set_segment(pins['Pin1'], pins['Pin5'])

# Segment control functions for the right side
def Right_Top():
    set_segment(pins['Pin2'], pins['Pin5'])

def Right_Top_Left():
    set_segment(pins['Pin3'], pins['Pin4'])

def Right_Top_Right():
    set_segment(pins['Pin4'], pins['Pin3'])

def Right_Middle():
    set_segment(pins['Pin3'], pins['Pin5'])

def Right_Bottom_Left():
    set_segment(pins['Pin3'], pins['Pin1'])

def Right_Bottom_Right():
    set_segment(pins['Pin4'], pins['Pin1'])

def Right_Bottom():
    set_segment(pins['Pin3'], pins['Pin2'])

def Percent_Symbol_On():
    set_segment(pins['Pin4'], pins['Pin2'])

def Percent_Symbol_Off():
    GPIO.setup(pins['Pin4'], GPIO.IN)
    GPIO.setup(pins['Pin2'], GPIO.IN)

def Green_Light_On():
    set_segment(pins['Pin5'], pins['Pin3'])

def Orange_Light_On():
    set_segment(pins['Pin5'], pins['Pin3'])
    sleep(0.001)
    set_segment(pins['Pin5'], pins['Pin4'])
    sleep(0.009)

def Red_Light_On():
    set_segment(pins['Pin5'], pins['Pin4'])

def Light_Off():
    GPIO.setup(pins['Pin5'], GPIO.IN)
    GPIO.setup(pins['Pin3'], GPIO.IN)
    GPIO.setup(pins['Pin4'], GPIO.IN)

# Define mapping for the segments of each number
left_number_segments = {
    0: [Left_Top, Left_Top_Left, Left_Bottom_Left, Left_Bottom, Left_Bottom_Right, Left_Top_Right],
    1: [Left_Top_Right, Left_Bottom_Right],
    2: [Left_Top, Left_Top_Right, Left_Middle, Left_Bottom_Left, Left_Bottom],
    3: [Left_Top, Left_Top_Right, Left_Middle, Left_Bottom_Right, Left_Bottom],
    4: [Left_Top_Left, Left_Middle, Left_Top_Right, Left_Bottom_Right],
    5: [Left_Top, Left_Top_Left, Left_Middle, Left_Bottom_Right, Left_Bottom],
    6: [Left_Top_Left, Left_Bottom_Left, Left_Bottom, Left_Bottom_Right, Left_Middle],
    7: [Left_Top, Left_Top_Right, Left_Bottom_Right],
    8: [Left_Top, Left_Top_Right, Left_Middle, Left_Bottom_Right, Left_Bottom, Left_Bottom_Left, Left_Top_Left],
    9: [Left_Top_Left, Left_Top, Left_Top_Right, Left_Middle, Left_Bottom_Right]
}

right_number_segments = {
    0: [Right_Top, Right_Top_Left, Right_Bottom_Left, Right_Bottom, Right_Bottom_Right, Right_Top_Right],
    1: [Right_Top_Right, Right_Bottom_Right],
    2: [Right_Top, Right_Top_Right, Right_Middle, Right_Bottom_Left, Right_Bottom],
    3: [Right_Top, Right_Top_Right, Right_Middle, Right_Bottom_Right, Right_Bottom],
    4: [Right_Top_Left, Right_Middle, Right_Top_Right, Right_Bottom_Right],
    5: [Right_Top, Right_Top_Left, Right_Middle, Right_Bottom_Right, Right_Bottom],
    6: [Right_Top_Left, Right_Bottom_Left, Right_Bottom, Right_Bottom_Right, Right_Middle],
    7: [Right_Top, Right_Top_Right, Right_Bottom_Right],
    8: [Right_Top, Right_Top_Right, Right_Middle, Right_Bottom_Right, Right_Bottom, Right_Bottom_Left, Right_Top_Left],
    9: [Right_Top_Left, Right_Top, Right_Top_Right, Right_Middle, Right_Bottom_Right]
}

percent_symbol_segments = {
    'on': [Percent_Symbol_On],
    'off': [Percent_Symbol_Off]
}

indicator_light_segments = {
    'green': [Green_Light_On],
    'orange': [Orange_Light_On],
    'red': [Red_Light_On],
    'off': [Light_Off]
}

# Functions to display numbers, percent symbol, and light
def display_number(number, segment_mapping):
    for segment in segment_mapping.get(number, []):
        segment()
        sleep(REFRESH_RATE)

def display_percent(symbol, segment_mapping):
    for segment in segment_mapping.get(symbol, []):
        segment()
        sleep(REFRESH_RATE)

def display_indicator(indicator, segment_mapping):
    for segment in segment_mapping.get(indicator, []):
        segment()
        sleep(REFRESH_RATE)

# This event will be used to stop the thread when the program is exiting
stop_event = Event()

# This function will run in a separate thread to update the display
def update_display(left_number, right_number, percent_symbol, indicator_light):
    while not stop_event.is_set():
        clear_segments()
        display_number(left_number[0], left_number_segments)
        display_number(right_number[0], right_number_segments)
        display_percent(percent_symbol[0], percent_symbol_segments)
        display_indicator(indicator_light[0], indicator_light_segments)
        sleep(REFRESH_RATE)

# This function reads the battery.json file and updates the display values
def read_battery_file(left_number, right_number, percent_symbol, indicator_light, file_path=BATTERY_FILE_PATH):
    while not stop_event.is_set():
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Log the data to verify its correctness
                print(f"Data read from battery.json: {data}")

                # Check if all keys are in the JSON data
                if all(key in data for key in ['left', 'right', 'percent', 'indicator']):
                    left_number[0] = data['left']
                    right_number[0] = data['right']
                    percent_symbol[0] = data['percent']
                    indicator_light[0] = data['indicator']
                else:
                    print("Error: One or more keys are missing in the battery.json file.")
        except IOError as e:
            print(f"Error reading {file_path}: {e}")
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from {file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        sleep(0.5)  # Check for new data every second or adjust as needed

# Main program loop
def main():
    # Initialize with default values
    left_number = [0]
    right_number = [0]
    percent_symbol = ['off']
    indicator_light = ['off']

    # Start the display thread
    display_thread = Thread(target=update_display, args=(left_number, right_number, percent_symbol, indicator_light), daemon=True)
    display_thread.start()

    # Start the battery file reading thread
    battery_thread = Thread(target=read_battery_file, args=(left_number, right_number, percent_symbol, indicator_light), daemon=True)
    battery_thread.start()

    try:
        # This loop now just waits for the threads to be stopped
        while True:
            sleep(1)  # Main thread does nothing, just sleeps
    finally:
        stop_event.set()  # Signal the threads to stop
        display_thread.join()
        battery_thread.join()
        clear_segments()
        GPIO.cleanup()
        print("\nCleanup complete. Program exited gracefully.")

if __name__ == '__main__':
    main()
