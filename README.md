# AirthingsToChords
Relay data from the Airthings API to CHORDS

This Python application uses the Airthings SDK to fetch data from their servers,
and uses pychords to submit that data to a CHORDS instance.

Authorization for the API is obtained from Airthings.

_An aside:_ The Airthings web dashboard is where you can monitor your system from your browser.
Oddly, I can't find a link on the Airthings account page to my dashboard;
and I actually don't see their dashboard linked anywhere from their home page. You have
to look around to eventually find the [dashboard link](https://dashboard.airthings.com).

## Instructions

### Installation

_Python >= v3.10 is required_

```sh
git clone --recurse https://github.com/sugartechllc/AirthingsToChords.git
 cd  AirthingsToChords
 python3 -m venv ~/venv.airthingstochords
 source ~/venv.airthingstochords/bin/activate
 install airthings-sdk/api/python/
 pip3 install requests attrs
```

### Authorization

[Obtain the client id and client secret](https://help.airthings.com/en/articles/4510990-integrations-airthings-api) from Airthings.

### Configuration

Create a configuration file, based on _config.json_. (Since it contains your auth codes,
don't make it publicly visible.)

### Running

```sh
source ~/venv.airthingstochords/bin/activate
cd AirthingsToChords
python3 AirthingsToChords.py -c <config_file>
```

## Resources

See the [API Reference](https://consumer-api-doc.dev.airthings.com/docs/api/getting-started).

[Step-by-step](https://help.airthings.com/en/articles/4510990-integrations-airthings-api) instructions for
getting authorized.

The formal [API docs](https://consumer-api-doc.airthings.com/api-docs).

The convenient [Airthings SDK](https://github.com/Airthings/airthings-sdk) which provides a python module
for accessing the API.
