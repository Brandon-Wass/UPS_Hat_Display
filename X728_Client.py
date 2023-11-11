import json
import RPi.GPIO as GPIO
from threading import Thread, Event
from time import sleep

class LEDDisplay:
    REFRESH_RATE = 0.0005
    BATTERY_FILE_PATH = 'battery.json'

    def __init__(self):
        self.pins = {
            'Pin1': 17, 'Pin2': 27, 'Pin3': 22, 'Pin4': 23, 'Pin5': 24,
        }
        self.setup_gpio()

        self.left_number = [0]
        self.right_number = [0]
        self.percent_symbol = ['off']
        self.indicator_light = ['off']
        self.stop_event = Event()

        # Define segment control mappings for a multiplexed display
        self.segment_mappings = {
            'left_digit': {
                0: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin5']), (self.pins['Pin1'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin4'])],
                1: [(self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin3'])],
                2: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin1'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin5'])],
                3: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin5'])],
                4: [(self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin4'])],
                5: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin5']), (self.pins['Pin1'], self.pins['Pin4'])],
                6: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin4'])],
                7: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin3'])],
                8: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin5']), (self.pins['Pin1'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin4'])],
                9: [(self.pins['Pin1'], self.pins['Pin2']), (self.pins['Pin2'], self.pins['Pin1']), (self.pins['Pin2'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin3']), (self.pins['Pin1'], self.pins['Pin5']), (self.pins['Pin1'], self.pins['Pin4'])]
            },
            'right_digit': {
                0: [(self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin3'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin2']), (self.pins['Pin3'], self.pins['Pin4']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin4'], self.pins['Pin3'])],
                1: [(self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin4'], self.pins['Pin3'])],
                2: [(self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin5']), (self.pins['Pin3'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin2'])],
                3: [(self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin3']), (self.pins['Pin3'], self.pins['Pin2'])],
                4: [(self.pins['Pin3'], self.pins['Pin4']), (self.pins['Pin3'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin4'], self.pins['Pin3'])],
                5: [(self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin3'], self.pins['Pin4']), (self.pins['Pin3'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin3']), (self.pins['Pin3'], self.pins['Pin2'])],
                6: [(self.pins['Pin3'], self.pins['Pin4']), (self.pins['Pin3'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin2']), (self.pins['Pin4'], self.pins['Pin3']), (self.pins['Pin3'], self.pins['Pin5'])],
                7: [(self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin4'], self.pins['Pin3'])],
                8: [(self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin3'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin2']), (self.pins['Pin3'], self.pins['Pin4']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin4'], self.pins['Pin3']), (self.pins['Pin3'], self.pins['Pin5'])],
                9: [(self.pins['Pin3'], self.pins['Pin4']), (self.pins['Pin2'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin1']), (self.pins['Pin3'], self.pins['Pin5']), (self.pins['Pin4'], self.pins['Pin3'])]
            },
            'percent_symbol': {
                'on': [(self.pins['Pin4'], self.pins['Pin2'])],
                'off': []
            },
            'indicator_light': {
                'green': [(self.pins['Pin5'], self.pins['Pin3'])],
                'orange': [(self.pins['Pin5'], self.pins['Pin3']), (self.pins['Pin5'], self.pins['Pin4'])],
                'red': [(self.pins['Pin5'], self.pins['Pin4'])],
                'off': []
            }
        }

    def setup_gpio(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.IN)

    def set_segment(self, pin_high, pin_low):
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.IN)
        GPIO.setup(pin_high, GPIO.OUT)
        GPIO.setup(pin_low, GPIO.OUT)
        GPIO.output(pin_high, GPIO.HIGH)
        GPIO.output(pin_low, GPIO.LOW)

    def clear_segments(self):
        for pin in self.pins.values():
            GPIO.setup(pin, GPIO.IN)

    def display_segment(self, segments):
        for pin_high, pin_low in segments:
            self.set_segment(pin_high, pin_low)
            sleep(self.REFRESH_RATE)

    def update_display(self):
        while not self.stop_event.is_set():
            self.clear_segments()
            self.display_segment(self.segment_mappings['left_digit'][self.left_number[0]])
            self.display_segment(self.segment_mappings['right_digit'][self.right_number[0]])
            self.display_segment(self.segment_mappings['percent_symbol'][self.percent_symbol[0]])
            self.display_segment(self.segment_mappings['indicator_light'][self.indicator_light[0]])
            sleep(self.REFRESH_RATE)

    def read_battery_file(self):
        while not self.stop_event.is_set():
            try:
                with open(self.BATTERY_FILE_PATH, 'r') as file:
                    data = json.load(file)
                self.left_number[0] = data.get('left', 0)
                self.right_number[0] = data.get('right', 0)
                self.percent_symbol[0] = data.get('percent', 'off')
                self.indicator_light[0] = data.get('indicator', 'off')
            except Exception as e:
                print(f"Error: {e}")
            sleep(0.5)

    def start(self):
        Thread(target=self.update_display, daemon=True).start()
        Thread(target=self.read_battery_file, daemon=True).start()

    def stop(self):
        self.stop_event.set()
        self.clear_segments()
        GPIO.cleanup()

if __name__ == '__main__':
    display = LEDDisplay()
    try:
        display.start()
        while True:
            sleep(1)
    finally:
        display.stop()
