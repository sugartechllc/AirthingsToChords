from operator import add
import json
import argparse
import os
import time

from airthings_sdk import Airthings
import pychords.tochords as tochords

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
    parser.add_argument(
        "-t", "--test", action="store_true",
        default=False,
        help="Run in test mode (no data sent to CHORDS)"
    )

    args = parser.parse_args()
    config["verbose"] = args.verbose
    config["test"] = args.test

    if not os.path.isfile(args.config):
        raise FileNotFoundError(f"Configuration file {args.config} not found.")

    with open(args.config, "r") as f:
        file_config = json.load(f)
        for key, value in file_config.items():
            if key not in config:
                config[key] = value

    return config

def radon_units_correction(value):
    """
    Convert radon units from Bq/m3 to pCi/L.
    1 Bq/m3 = 0.027 pCi/L
    """
    return f"{float(value) * 0.027027:.4g}"

if __name__ == "__main__":

    print("Starting Airthings to CHORDS data transfer...")

    config = load_config()
    client_id = config["airthings"]["client_id"]
    client_secret = config["airthings"]["client_secret"]

    # Start the CHORDS sender thread
    tochords.startSender()

    # Initialize the Airthings client
    airthings = Airthings(client_id=client_id, client_secret=client_secret, is_metric=True)

    last_time = None
    sleep_time = config["query_interval_secs"]
    while True:
        try:
            devices = airthings.update_devices()
            if config["verbose"]:
                print(f"{devices}")
            for device_id, device_info in devices.items():
                obs_time = device_info.recorded
                device_sn = device_info.serial_number
                if device_sn in config["chords"]["devices"] and config["chords"]["devices"][device_sn]["enabled"]:

                    # Only save data when there is a new observation time
                    if obs_time != last_time:
                        last_time = obs_time

                        # Prepare the tokens to send to CHORDS
                        chords_tokens = {
                            "api_key": config["chords"]["api_key"],
                            "api_email": config["chords"]["api_email"],
                            "host": config["chords"]["host"],
                            "inst_id": config["chords"]["devices"][device_sn]["inst_id"],
                            "vars": {}
                        }

                        chords_tokens['vars']['at'] = obs_time

                        # Iterate through sensors and map to CHORDS variables
                        for sensor in device_info.sensors:
                            if sensor.sensor_type in config["chords"]["chords_short_name"]:
                                short_name = config["chords"]["chords_short_name"][sensor.sensor_type]
                                chords_tokens['vars'][short_name] = sensor.value
                        if 'radon' in chords_tokens['vars']:
                            # Convert radon units from Bq/m3 to pCi/L
                            chords_tokens['vars']['radon'] = radon_units_correction(chords_tokens['vars']['radon']) 

                        # Send data to CHORDS
                        uri = tochords.buildURI(config['chords']['host'], chords_tokens)
                        if config["test"]:
                            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Test mode: would send URI: {uri}")
                        else:
                            tochords.submitURI(uri, 10*24*6)

                        # Check again after the normal sleep time
                        sleep_time = config["query_interval_secs"]
                    else:
                        # Not a new observation so check again in a minute
                        print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} No new data for device {device_sn} (last data time: {obs_time}), sleeping for 60 seconds.")
                        sleep_time = 60

        except Exception as e:
            print(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())} Exception: {e}")
            print("I can't go on, I'm exiting now.")
            break

        time.sleep(sleep_time)
