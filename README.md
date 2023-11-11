# UPS_Hat_Display

This repository contains the code for a mini battery status display designed to work with the Geekworm x728 UPS HAT. The display provides a real-time battery level and charging status on a tiny 10mm x 8mm proprietary screen, perfect for discreet integration into Raspberry Pi projects.

## Features

- Real-time battery capacity up to 99 percent
- Indicates whether external power is provided to the HAT
- Battery voltage indicated by color-changing symbol on the display
- Designed to be discreet and integrate seamlessly with Raspberry Pi projects
- Includes reverse engineering details in Display_Info.md.  https://github.com/B-Boone/UPS_Hat_Display/blob/main/Display_Info.md

## Components

- Raspberry Pi (compatible with Pi 3/4/etc.)
- Geekworm x728 UPS HAT
- Proprietary mini LED display (10mm x 8mm) sourced from SMOK SpaceMan 10K PRO
- 5-pin GPIO connection

## Prerequisites

Before you begin, ensure you have the following:

- Your Raspberry Pi is set up with Raspbian or a compatible OS that provides GPIO access
- You have installed Python 3.x on your Raspberry Pi
- The Geekworm x728 UPS HAT is correctly and securely attached to your Raspberry Pi

## Software Requirements

- Raspbian or any compatible Raspberry Pi OS
- Python 3.x

## Installation

1. Clone the repository to your Raspberry Pi:

    ```bash
    git clone https://github.com/B-Boone/UPS_Hat_Display
    ```

2. Navigate to the cloned directory:

    ```bash
    cd UPS_Hat_Display
    ```

3. Modify the permissions of the Python scripts, if necessary:

   ```bash
   chmod +x X728_Server.py X728_Client.py
   ```

4. Configure the scripts to run on startup by adding them to the `crontab` or using the provided systemd .service files and moving them to your systemd/system/ directory (make sure to change the `ExecStart` and `WorkingDirectory` locations if necessary)

## Configuration

- Modify the GPIO pins in the `X728_Client.py` file to match your setup. For example:

```python
pins = {
    'Pin1': 17, 'Pin2': 27, 'Pin3': 22, 'Pin4': 23, 'Pin5': 24,
}
```

## Usage

- No need to use `sudo` permissions to run the Python scripts, only to make the `crontab` entries or move the .service files into the service directory.

- Start the server-side script first (`X728_Server.py`) to read the battery status from the HAT and write to `battery.json`:

    ```bash
    python3 X728_Server.py
    ```

- Start the client-side script next (`X728_Client.py`) to read from the `battery.json` file and update the display:

    ```bash
    python3 X728_Client.py
    ```

## Troubleshooting

- Display flickering:
  - Modify the `REFRESH_RATE` in the `X728_Client.py` script, but be careful as this has already been tuned to provide the smoothest operation between Pi and the display
  - Use a stronger Raspberry Pi
    - Works great with no flicker on 4B model without adjusting `REFRESH_RATE`
    - Older models may produce slightly to moderately noticable flickering on the display due to their limited CPU performance

- Service or `crontab` not starting the scripts automatically:
  - Verify the service files are correctly set up in systemd
  - Check for spelling or directory mistakes
  - Give the Python scripts execute permissions

- Display not showing the proper information, ie: numbers are unrecognizable, or wrong areas of the display are lit up
  - Check your GPIO connections and connections to the display
    - The displays have a tiny `1` on them to mark `Pin1`, and the rest go in order to `Pin5`
    - Ensure you are connected to the proper GPIO pins or have modified the `X728_Client.py` file to use the correct GPIO pins
  - Run the `X728_Client.py` script in a terminal or IDE to read any errors that may be happening, such as unable to read .json file
    - Use `chmod` to give read/write permissions for the `battery.json` file

## License

This project is licensed under the GNU Lesser General Public License v3.0 - see the [LGPL-3.0 License](https://www.gnu.org/licenses/lgpl-3.0.html) for details.

## Acknowledgments

- Thanks to Geekworm for their x728 V2.3 UPS HAT and their prewritten code for checking battery status on the board. It sure made the X728_Server.py file much quicker to to write using the PLD and ASD files as a template.

## ENJOY!
