
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

### Design

High level structure of this python service

1. Connect to MQTT broker (asynchronous) and also start the MQTT loop
2. Connect to miband device in a separate thread
    1. When connected start the infinite loop (`post_wait_for_notifications()`) to receive asynchronous messages from miband
3. Start the FastAPI loop to handle incoming REST API calls.

### Environment Variables

This services makes use of the following environment variables:

| env | default value | description |
| -- | -- | -- |
| MIBAND5 | False | Should be set if the device is a miband5 device, otherwise the device is considered a miband4 device. |
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
| LOGLEVEL | - | E.g. `INFO`, `DEBUG`, ...|
| TZ | - | The timezone. E.g. `Europe/Paris`, `UTC`, ... |
| SLEEPFOREVER | False | When set to `True` or `1` the python service will just *sleep* forever.  This is only set when the python service is running in a docker container and you want to test the configuration by attaching a shell to the docker container. |

## miband.py

### Fetching Activity data

see also [README.miband4.gatt.md](README.miband4.gatt.md)

Fetching activity data is actually happening by method `start_get_previews_data(start_timestamp)` which triggers the activity retrieval by following write command.

```java
trigger = b'\x01\x01' + ts + utc_offset
self._char_fetch.write(trigger, False)
```

The following notifications are then received from miband:

1. `hnd == self.device._char_fetch.getHandle()` and `data[:3] == b'\x10\x01\x01'`
    1. Log start timestamp. E.g. `miband (DEBUG) >   > Fetch data from 2022-5-3 11:51`
    2. `self.device._char_fetch.write(b'\x02', False)` (I don't know why this is needed)
2. several `hnd == self.device._char_activity.getHandle()`
    1. splits received data in activity records and for each activity record:
       1. call the callback which also logs the activity data. E.g. `miband_api (INFO) > {"timestamp_ms": 1651571460000, "timestamp_local": "2022-05-03 11:51:00", "category": 96, "intensity": 21, "steps": 0, "heart_rate": 255}`
3. Instead of 2 we get sometimes

```text
2022-05-03 13:43:11,692 miband (DEBUG) > _char_fetch.getHandle(): 3 bytes received, processing them ...
2022-05-03 13:43:11,693 miband (DEBUG) >   > [b'\x10\x01\x02'] Trigger more communication
2022-05-03 13:43:12,694 miband (DEBUG) > start_get_previews_data(2022-05-03 13:34:00)...
2022-05-03 13:43:12,695 miband (DEBUG) > _char_fetch.getHandle(): 3 bytes received, processing them ...
2022-05-03 13:43:12,696 miband (DEBUG) >   > [b'\x10\x02\x04'] No more activity fetch possible
2022-05-03 13:43:12,862 miband (DEBUG) > _char_fetch.getHandle(): 3 bytes received, processing them ...
2022-05-03 13:43:12,864 miband (DEBUG) >   > [b'\x10\x01\x02'] Trigger more communication
2022-05-03 13:43:13,865 miband (DEBUG) > start_get_previews_data(2022-05-03 13:34:00)...
2022-05-03 13:43:14,032 miband (DEBUG) > _char_fetch.getHandle(): 3 bytes received, processing them ...
2022-05-03 13:43:14,033 miband (DEBUG) >   > [b'\x10\x01\x02'] Trigger more communication
2022-05-03 13:43:15,034 miband (DEBUG) > start_get_previews_data(2022-05-03 13:34:00)...
2022-05-03 13:43:15,247 miband (DEBUG) > _char_fetch.getHandle(): 3 bytes received, processing them ...
2022-05-03 13:43:15,248 miband (DEBUG) >   > [b'\x10\x01\x02'] Trigger more communication
2022-05-03 13:43:16,249 miband (DEBUG) > start_get_previews_data(2022-05-03 13:34:00)...
2022-05-03 13:43:16,417 miband (DEBUG) > _char_fetch.getHandle(): 3 bytes received, processing them ...
2022-05-03 13:43:16,418 miband (DEBUG) >   > [b'\x10\x01\x02'] Trigger more communication
```

### Comparison of fetching activity by Gadget Bridge

I have compared it with repository [Freeyourgadge/Gadgetbridge](https://github.com/Freeyourgadget/Gadgetbridge).

The java class [FetchActivityOperation.java](https://github.com/Freeyourgadget/Gadgetbridge/blob/2c12b1bf731813ce574adfada47c404dede5b520/app/src/main/java/nodomain/freeyourgadget/gadgetbridge/service/devices/miband/operations/FetchActivityOperation.java) describes the logic of fetching the activity data.

1/ So the retrieval is initiated by `doPerfom()` method which does:

```java
builder.write(getCharacteristic(MiBandService.UUID_CHARACTERISTIC_CONTROL_POINT), fetch)
```

where

* `UUID_CHARACTERISTIC_CONTROL_POINT` = `UUID.fromString(String.format(BASE_UUID, "FF05"))`
* `fetch` = `MiBandService.COMMAND_FETCH_DATA` = `0x6`

2/ The activity data is received by the `onCharacteristicChanged()` method which does:

```java
if (MiBandService.UUID_CHARACTERISTIC_ACTIVITY_DATA.equals(characteristicUUID)) {
            handleActivityNotif(characteristic.getValue());
...
```

where:

* `UUID_CHARACTERISTIC_ACTIVITY_DATA` =  `UUID.fromString(String.format(BASE_UUID, "FF07"))`
  
3/ once the last chunk of activity data is received it writes an acknowledgement

```java
...
if (activityStruct.isBlockFinished()) {
    sendAckDataTransfer(activityStruct.activityDataTimestampToAck, activityStruct.activityDataUntilNextHeader);
            ...
}
```

and `sendAckDataTransfer()` does:

```java
...
byte[] ackChecksum = new byte[]{
    (byte) (bytesTransferred & 0xff),
    (byte) (0xff & (bytesTransferred >> 8))
};
if (prefs.getBoolean(MiBandConst.PREF_MIBAND_DONT_ACK_TRANSFER, false)) {
    ackChecksum = new byte[]{
        (byte) (~bytesTransferred & 0xff),
        (byte) (0xff & (~bytesTransferred >> 8))
    };
}
byte[] ack = new byte[]{
    MiBandService.COMMAND_CONFIRM_ACTIVITY_DATA_TRANSFER_COMPLETE,
    ackTime[0],
    ackTime[1],
    ackTime[2],
    ackTime[3],
    ackTime[4],
    ackTime[5],
    ackChecksum[0],
    ackChecksum[1]
};
try {
    TransactionBuilder builder = performInitialized("send acknowledge");
    builder.write(getCharacteristic(MiBandService.UUID_CHARACTERISTIC_CONTROL_POINT), ack);
    ...
    //The last data chunk sent by the miband has always length 0.
    //When we ack this chunk, the transfer is done.
    if (getDevice().isBusy() && bytesTransferred == 0) {
        /if we are not clearing miband's data, we have to stop the sync
        if (prefs.getBoolean(MiBandConst.PREF_MIBAND_DONT_ACK_TRANSFER, false)) {
            builder = performInitialized("send acknowledge");
            builder.write(getCharacteristic(
                MiBandService.UUID_CHARACTERISTIC_CONTROL_POINT), new byte[]
                {MiBandService.COMMAND_STOP_SYNC_DATA});
```

where

* `COMMAND_CONFIRM_ACTIVITY_DATA_TRANSFER_COMPLETE` = `0xa`
* `PREF_MIBAND_DONT_ACK_TRANSFER` = environment variable ?
* `COMMAND_STOP_SYNC_DATA` = `0x11`

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



