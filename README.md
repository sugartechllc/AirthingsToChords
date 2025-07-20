# AirthingsToChords
Relay data from Airthings API to CHORDS

Oddly, I can't find a link on the Airthings account page to my dashboard;
and I actually don't see their dashboard linked anywhere from their home page. You have
to look around to find the [dashboard link](https://dashboard.airthings.com).

See the [API Reference](https://consumer-api-doc.dev.airthings.com/docs/api/getting-started).

## Installing

**Python >= v3.10 is required**

Download the Airthings api, and install the airthings-sdk python modules and dependencies.
```sh
cd ~/
git clone git@github.com:Airthings/airthings-sdk.git
pip3 install airthings-sdk/api/python
pip3 install httpx
pip3 install attrs
```

## Google AI gives thse instructions for :

To get consumer data from Airthings using their API, you'll need to register an API client, authorize it, and then use the client credentials to fetch data. The process involves creating a client on the Airthings dashboard, obtaining a client ID and secret, and using these to authenticate and retrieve data.

Here's a more detailed breakdown:

1. Register an API Client:
  - Go to the Airthings dashboard and navigate to the integrations page.
  - Create a new API client, providing a name and description.
  - For the Consumer API, select "Client Credentials" as the flow type, according to the documentation.
  - Enable the client switch and save the configuration.
  - You'll receive a client ID and secret, which are essential for authentication. 

2. Authorize the Client:
  - To authorize, use the client ID and secret to request a token from the Airthings accounts API.
  - The "read:device:current_values" scope is needed to access the data endpoints.
  - The API will return an access token, which is used to authenticate subsequent requests.

3. Fetch Data:
  - Use the access token to make requests to the Airthings Consumer API endpoints.
  - The API provides access to real-time data from your Airthings devices.
  - Refer to the Airthings API documentation for details on available endpoints and data formats. 

***Key Considerations:***

***Rate Limits:***
Be mindful of the rate limits on the Airthings Consumer API, which is 120 requests per hour.

***Data Scope:***
The "read:device:current_values" scope is required for accessing current device data.

***Security:***
Ensure you handle the client secret securely and avoid exposing it in your code. 
