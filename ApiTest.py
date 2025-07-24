""" Example of fetching devices and sensors from Airthings API. """

import sys
import time

from airthings_sdk import Airthings
from anyio import sleep

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print("Please add client id and client secret as parameters.")
        print("Usage:")
        print("python fetch_devices_and_sensors.py <client_id> <client_secret>")
        sys.exit(1)
    client_id = sys.argv[1]
    client_secret = sys.argv[2]

    airthings = Airthings(
        client_id=client_id, client_secret=client_secret, is_metric=True
    )

    while True:
        devices = airthings.update_devices()
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {airthings.devices}")
        sys.stdout.flush()
        time.sleep(300)  # Sleep for 5 minutes before fetching again