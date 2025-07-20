from operator import add
import json
import argparse
import os

from airthings_sdk import Airthings
import time

def load_config():

    config = {}

    parser = argparse.ArgumentParser(
        description="Airthings API Client",
        epilog="Command line arguments will override values in the JSON configuration file."
    )
    parser.add_argument(
        "-c", "--config", type=str, required=True,
        help="Path to JSON configuration file"
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true",
        default=False,
        help="Enable verbose output"
    )
    args = parser.parse_args()
    config["verbose"] = args.verbose

    if not os.path.isfile(args.config):
        raise FileNotFoundError(f"Configuration file {args.config} not found.")

    with open(args.config, "r") as f:
        file_config = json.load(f)
        for key, value in file_config.items():
            if key not in config:
                config[key] = value

    return config

config = load_config()
client_id = config["airthings"]["client_id"]
client_secret = config["airthings"]["client_secret"]


if __name__ == "__main__":

    airthings = Airthings(
        client_id=client_id, client_secret=client_secret, is_metric=True
    )

    last_time = None

    while True:
        devices = airthings.update_devices()
        for device_id, device_info in devices.items():
            obs_time = device_info.recorded
            data = {}
            if config["verbose"]:
                print(f"Device ID: {device_id}")
                print(f"Device Name: {device_info.name}")
                print(f"Device Type: {device_info.type}")
                print(f"Device Serial: {device_info.serial_number}")
                print(f"Device Recorded: {device_info.recorded}")
            for sensor in device_info.sensors:
                if config["verbose"]:
                    print(f"Sensor Type: {sensor.sensor_type}")
                    print(f"Sensor Value: {sensor.value}")
                    print(f"Unit: {sensor.unit}")
                if sensor.sensor_type in config["chords"]["chords_short_name"]:
                    data['at'] = device_info.recorded
                    short_name = config["chords"]["chords_short_name"][sensor.sensor_type]
                    data[short_name] = sensor.value
            if obs_time != last_time:
                # Only save data when there is a new observation time
                last_time = obs_time
                print(f"{data}")
        time.sleep(config["query_interval_secs"])
