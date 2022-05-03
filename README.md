
![Requirements](https://img.shields.io/badge/Python-3.6-lightgrey)
![Commit](https://img.shields.io/github/last-commit/janvda/miband4)
![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)

# MIBAND 4 & 5 - Python Service

This repository is a modified and extended version of the [satcar77/miband4 repository](https://github.com/satcar77/miband4/blob/master/README.md).  It provides following extensions with respect to this repository:

1. better support for MiBand5
2. provides an API service ([miband_api.py](https://github.com/janvda/miband4/blob/master/miband_api.py) - this service doesn't exist in parent repository) which allows to interact with the miband

## miband-api.py

This python program provides an API service that allows to interact with a specific [Xiaomi Mi Smart Band 4](https://en.wikipedia.org/wiki/Xiaomi_Mi_Smart_Band_4) or [Xiaomi Mi Smart Band 5](https://en.wikipedia.org/wiki/Xiaomi_Mi_Smart_Band_5) device.

It uses the [FastAPI](https://fastapi.tiangolo.com/) framework to wrap the methods specified in [miband.py](https://github.com/janvda/miband4/blob/master/miband.py).  These API methods are exposed at URL `http://<exposed api host>:<API_PORT>` (see Environment Variables).  This API also provides its documentation at same URL (e.g. [http://nuc1:8200](http://nuc1:8200) - assuming the API is exposed at host `nuc1` and `API_PORT` = `8200` ).  More precisely the documentation can be found at following subfolders of this URL:

* `/docs` which besides the API specification also allows to test the API
* `/redoc` provides FastAPI specification powered by ReDoc.

The asynchronous feedback coming from the miband device is send to a configurable MQTT broker.

### Environment Variables

This services makes use of the following environment variables:

| env | default value | description |
| -- | -- | -- |
| MIBAND_MAC | - | Bluetooth mac address of the miband device we want to interact with. |
| MIBAND_AUTH_KEY  | - | The authentication key (see below) that is needed for most interactions. |
| API_HOST | `0.0.0.0`  | listening socket for the REST API will be bound to this host. |
| API_PORT | `8001` | Port for the REST API. |
| MQTT_CLIENT_NAME | `miband-api-service` |  |
| MQTT_SERVER | `127.0.0.1` | hostname of the MQTT broker|
| MQTT_PORT | `1883`| port of the MQTT broker |
| MQTT_ALIVE | `60` | |
| MQTT_BIND_ADDRESS | - | |
| MQTT_TOPIC | `/miband-api` | MQTT topic prefix used by API for publishing messages. |
| LOGLEVEL | - | E.g. `INFO`|
| TZ | - | The timezone. E.g. `Europe/Paris`, `UTC`, ... |

# Documentation below needs to be cleaned up

![demo](screen/1.png)

## Updates(3/1/2021)

- Alarm functionality. 

## Updates(10/27/2020)
- (New Feature) Custom watchface files(.bin) support. 
- Firmware restore/update fixes.

## Contributors 

 MiBand 4 provides superset of services provided by MiBand 2/3. For the services that were similar for both devices, the bluetooth characteristics, UUIDs  and request/response byte sequence were the same. Therefore,  I utilized some of the informations already uncovered by [Freeyourgadget team](https://github.com/Freeyourgadget/Gadgetbridge) and made use of the code by [Andrey Nikishaev](https://github.com/creotiv) for MiBand2. I reverse engineered snooped ACL packets to fill in the pieces of the puzzle. 



## AuthKey
MiBand 4 with updated firmware requires server based pairing. This means, that you absolutely must use MiFit app to make the initial pairing, retrieve the pairing key and then use this key to pair with this library. Only some of the features of this library work without AuthKey of the band. Read [Server based pairing](https://github.com/Freeyourgadget/Gadgetbridge/wiki/Huami-Server-Pairing) for further details.

There are several ways to obtain the key.

#### Obtaining unique Authkey
On **rooted phone** you may grab the key from MiFit database which means that you must:

- install MiFit
- create an account
- pair the band/watch
- Then, execute the following command in a root shell terminal:
```
sqlite3 /data/data/com.xiaomi.hm.health/databases/origin_db_[YOURDBNAMEHERE] "select AUTHKEY from DEVICE"
```
On a **non rooted phone** you may consider using https://www.freemyband.com/ 

**NOTICE**: Every time you hard reset the band/watch, the Bluetooth MAC Address will be changed and you must grab a new key! Also, anytime you unpair your band/watch from MiFit, the pairing key will be invalidated and you must make new pairing in MiFit app.

### Features that work without authkey
- Sending Calls
- Sending alerts
- Sending Missed call notifications
- Retrieving device info
- Sending music title and music state(Playing/Paused)
- Recieve music control events (Play/Pause/Forward/Backward/Volume Up/Volume Down/Enter Music app/ Exit Music app) through callbacks
### Features that needs authkey
- Updating watchface of the band
- Retrieving heart rate (Realtime and Single time)
- Firmware update/restore (This feature has the potential to brick your Mi Band 4. Do it at your own risk)
- Retrieving steps count, calories count and fat burnt
- Setting date and time
- Fetching fitness data within certain past intervals.


# Setup and demo


- Clone this repo to your local machine using `https://github.com/satcar77/miband4.git`



1.  Install the dependencies. Libglib2 is required for bluepy. 

    ```
    sudo apt-get install libglib2.0-dev
    pip3 install -r requirements.txt
    ```
2. (**Optional**) Find AuthKey for your device and put it to `auth_key.txt` file in the current directory with the script. 

3.  Turn off your Bluetooth on your mobile device paired with MIBand 4

4.  Find out your MiBand4 MAC address using hcitool

    ```
    sudo hcitool lescan
    // if you are having trouble
    sudo hciconfig hci0 reset 
	```
5.  Run the miband4_console

    ```
    python3 miband4_console.py -m MAC_ADDRESS 
	```





## Contributing



#### Step 1

- **Option 1**
    - 🍴 Fork this repo!

- **Option 2**
    - 👯 Clone this repo to your local machine

#### Step 2

- **HACK AWAY!** 🔨🔨🔨

#### Step 3

- 🔃 Create a new pull request



