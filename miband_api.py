# see https://fastapi.tiangolo.com/
import uvicorn, json, random, os, logging, threading, time, json

from typing    import Optional
from fastapi   import FastAPI, HTTPException
from fastapi.responses   import HTMLResponse
from pydantic  import BaseModel
from miband    import miband
from functools import wraps
from constants import MUSICSTATE
from paho.mqtt import client as mqtt_client
from datetime  import datetime, timedelta
from bluepy    import btle

# logging initialization 
logging.basicConfig(format='%(asctime)-15s %(name)s (%(levelname)s) > %(message)s',
                    level=os.environ.get('LOGLEVEL', 'INFO').upper())
logger = logging.getLogger("miband_api")

if not (os.getenv("SLEEP_FOREVER","False") in [ "0", "False", "false", "FALSE" ]) : 
    logger.warning("Environment variable SLEEP_FOREVER is set, so this service will sleep forever.")
    while True:
        logger.info("Zzzz....")
        time.sleep(3600)

# create decorator function as specified by https://stackoverflow.com/a/64656733/6762442
def return_404_if_not_connected(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global connected
        if connected:
            return func(*args, **kwargs)
        else:
            raise HTTPException(status_code=404, detail="Not connected to miband device - you need to (re)connect first before using this operation.")
    return wrapper

# decorator function to protect function by miband_lock
def protect_by_miband_lock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global miband_lock
        logger.debug(f"{func.__name__}(): acquiring lock ...")
        miband_lock.acquire()
        try:
            logger.info(f"Calling {func.__name__}() ...")
            rc=func(*args, **kwargs)
        finally:
            miband_lock.release()
            logger.debug(f"{func.__name__}():...lock released")
        return rc
    return wrapper

app = FastAPI()

@app.get("/",response_class=HTMLResponse)
def read_root():
    return """
<!DOCTYPE html>
<html>
<body>
<h1>Miband API</h1>
<ul>
<li>github project <a href="https://github.com/janvda/miband4">janvda/miband4</a></li>
<li><a href="./docs">./docs</a> : FastAPI specification (allows to test it as well)</li>
<li><a href="./redoc">./redoc</a> : FastAPI specification powered by ReDoc</li>
</ul>
</body>
</html>
"""

# callbacks        
def cb_music_play():
    logger.info("play")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","play")
    band.setMusicPauseIcon()
def cb_music_pause():
    logger.info("pause")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","pause")
    band.setMusicPlayIcon()
def cb_music_forward():
    logger.info("forward")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","forward")
def cb_music_back():
    logger.info("backward")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","backward")
def cb_music_vup():
    logger.info("volume up")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","volume up")
def cb_music_vdown():
    logger.info("volume down")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","volume down")
def cb_music_focus_in():
    logger.info("music focus in")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","focus in")
def cb_music_focus_out():
    logger.info("music focus out")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","focus out")

def cb_lost_device():
    logger.info("lost device")
    my_mqtt_client.publish(f"{my_mqtt_topic}","lost device")
def cb_found_device():
    logger.info("found device")
    my_mqtt_client.publish(f"{my_mqtt_topic}","found device")

def cb_activity_log(timestamp,c,i,s,h):
    activity_log = { "timestamp_ms" : int(timestamp.timestamp() * 1000), "timestamp_local" : timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                     "category" : c, "intensity" : i, "steps" : s, "heart_rate" : h }
    logger.info(json.dumps(activity_log))
    my_mqtt_client.publish(f"{my_mqtt_topic}/activity",json.dumps(activity_log))

def cb_heart_rate(data):
    logger.info(f"Realtime heart BPM: {data}")
    my_mqtt_client.publish(f"{my_mqtt_topic}/heart_rate",data)

#@app.post("/connect")
def connect(mac_address: str,authentication_key:str):
    global connected, band
    if connected :
        error_str = "Trying to connect while already connected."
        logger.error(error_str)
        raise HTTPException(status_code=400,detail=error_str)
    while not connected:
        try:
            band = miband(mac_address, 
                        bytes.fromhex(authentication_key),
                        miband5 = os.getenv("MIBAND5","False") in [ "0", "False", "false", "FALSE" ])
            connected = band.initialize()    
            # set callbacks
            band.setMusicCallback(cb_music_play,     cb_music_pause,    cb_music_forward,
                                cb_music_back,     cb_music_vup,      cb_music_vdown,
                                cb_music_focus_in, cb_music_focus_out)
            band.setLostDeviceCallback(cb_lost_device, cb_found_device)
        except btle.BTLEDisconnectError as error:
            logger.info("BTLEDisconnectError - retrying")
        except BaseException as error:
            error_str = format(error)
            if "non-hexadecimal number found in fromhex()" in error_str:
                error_str = "Authentication key has not the format of a hexadecimal number !"
            logger.exception(error_str)
            raise HTTPException(status_code=400, detail=error_str)
    return connected

#@app.post("/wait_for_notifications")
@return_404_if_not_connected
def post_wait_for_notifications():
    logger.info("Waiting for notifications:")
    try:
        while True:
            miband_lock.acquire()
            try:
                notification_received = band.waitForNotifications(0.5)
            #except BaseException as error:
            #    logger.exception(format(error))
            finally:
                miband_lock.release()
            if not notification_received:
                time.sleep(0.3)
    except btle.BTLEDisconnectError as error:
        logger.warning(f"BTLEDisconnectError: {error} (miband went out of range ?)")
        global connected
        connected = False
    return "BTLEDisconnectError"

@app.get("/info")
@return_404_if_not_connected
@protect_by_miband_lock
def get_info():
    info = { "software_version" : band.get_revision(),
             "hardware_version" : band.get_hrdw_revision(),
             "serial_number" : band.get_serial(),
             "battery_level" : band.get_battery_info()['level'],
             "time" : band.get_current_time()['date'].isoformat()
            }
    return info

@app.get("/step_count")
@return_404_if_not_connected
@protect_by_miband_lock
def get_step_count():
    return band.get_steps()

@app.get("/battery_info")
@return_404_if_not_connected
@protect_by_miband_lock
def get_battery_info():
    return band.get_battery_info()

@app.get("/current_time")
@return_404_if_not_connected
@protect_by_miband_lock
def get_current_time():
    return band.get_current_time()

@app.get("/heart_rate")
@return_404_if_not_connected
@protect_by_miband_lock
def get_heart_rate():
    return band.get_heart_rate_one_time()
 
@app.post("/message")
@return_404_if_not_connected
@protect_by_miband_lock
def post_message(message: str, title: str = "New Message"):
    return  band.send_custom_alert(5,title,message)

@app.post("/mail")
@return_404_if_not_connected
@protect_by_miband_lock
def post_mail(message: str, title: str = "New Mail"):
    return  band.send_custom_alert(1,title,message)

@app.post("/call")
@return_404_if_not_connected
def post_call(message: str, title: str = "New Call"):
    return  band.send_custom_alert(3,title,message)

@app.post("/missed_call")
@return_404_if_not_connected
@protect_by_miband_lock
def post_message(message: str, title: str = "Missed Call"):
    return  band.send_custom_alert(3,title,message)

@app.post("/music")
@return_404_if_not_connected
@protect_by_miband_lock
def post_music(artist: str = "No Artist", 
               album: str = "No Album",
               title: str = "No Title",
               playing: bool = True,
               volume: int = 50,
               position: int= 50,
               duration: int=100
               ):
    music_state = MUSICSTATE.PLAYED if playing else MUSICSTATE.PAUSED
    logger.info(f"band.setTrack({music_state},{artist},{album},{title},{volume},{position},{duration})")
    band.setTrack(music_state,artist,album,title,volume,position,duration)
    return "ok"

@app.post("/retrieve_activity")
@return_404_if_not_connected
@protect_by_miband_lock
# start and end time specified in milliseconds since epoch
# default start time is today
# default end time is 2035-01-01
def retrieve_activity(start_time_ms:int = -1, end_time_ms:int = -1):
    if (start_time_ms == -1 ):
        start_time = datetime.now() - timedelta(hours = 24)
    else:
        start_time = datetime.fromtimestamp(start_time_ms/1000.0)
    if (end_time_ms == -1 ):
        end_time = datetime.now() + timedelta(minutes = 1)
    else:
        end_time=datetime.fromtimestamp(end_time_ms/1000.0)
    logger.info(f"retrieving activity between {start_time} and {end_time}")
    return band.get_activity_betwn_intervals(start_time,end_time,cb_activity_log)

@app.post("/retrieve_last_activity")
@return_404_if_not_connected
#don't add @protect_by_miband_lock as this happens when calling retrieve_activity.
def retrieve_last_activity(minutes_ago:int = 10):
    start_time_ms = int( ( datetime.now() - timedelta(minutes = minutes_ago) ).timestamp()*1000 )
    return retrieve_activity(start_time_ms,-1)

@app.post("/start_heart_rate_monitor")
@return_404_if_not_connected
@protect_by_miband_lock
def start_heart_rate_monitor(measure_minute_interval: int=1):
    return band.set_heart_monitor_sleep_support(True,measure_minute_interval)

@app.post("/stop_heart_rate_monitor")
@return_404_if_not_connected
@protect_by_miband_lock
def stop_heart_rate_monitor():
    return band.set_heart_monitor_sleep_support(False)

@app.post("/start_heart_rate_realtime")
@return_404_if_not_connected
@protect_by_miband_lock
def start_heart_rate_realtime():
    return band.start_heart_rate_realtime(heart_measure_callback=cb_heart_rate)

@app.post("/stop_heart_rate_realtime")
@return_404_if_not_connected
#@protect_by_miband_lock
def stop_heart_rate_realtime():
    return band.stop_realtime()


#----- Setting configuration parameters based on environment variables
miband_mac           = os.getenv("MIBAND_MAC")
miband_key           = os.getenv("MIBAND_AUTH_KEY")

my_mqtt_client       = None
my_mqtt_client_name  = os.getenv("MQTT_CLIENT_NAME","miband-api-service")
my_mqtt_server       = os.getenv("MQTT_SERVER","127.0.0.1")
my_mqtt_port         = int(os.getenv("MQTT_PORT","1883"))
my_mqtt_alive        = int(os.getenv("MQTT_ALIVE","60"))
my_mqtt_bind_address = os.getenv("MQTT_BIND_ADDRESS","")
my_mqtt_topic        = os.getenv("MQTT_TOPIC","/miband-api")

my_api_host          = os.getenv("API_HOST","0.0.0.0") # Bind socket to this host.
my_api_port          = int(os.getenv("API_PORT","8001"))

# The miband operations are based on the bluepy library which is not threadsafe.  
# This miband_locak will be used to assure that miband operations are NOT executed in parallel.
miband_lock = threading.Lock()

# global variables
band           = None 
connected      = False

# ---------  MQTT setup -------------------------
# connect to mqtt broker
def on_connect(client, userdata, flags, rc):
    global mqtt_connected
    if rc == 0:
        mqtt_connected = True
        logger.info("... connected to MQTT Broker!")
    else:
        logger.error("... failed to connect, return code %d\n", rc)
        exit()

mqtt_connected = False
my_mqtt_client = mqtt_client.Client(my_mqtt_client_name)
my_mqtt_client.on_connect = on_connect
try:
    logger.info("Connecting to MQTT broker (%s:%s alive=%s, bind_address=%s)...",
                    my_mqtt_server,my_mqtt_port,my_mqtt_alive,my_mqtt_bind_address)
    my_mqtt_client.connect( my_mqtt_server,my_mqtt_port,my_mqtt_alive,my_mqtt_bind_address)
    my_mqtt_client.loop_start()
    my_mqtt_client.publish(f"{my_mqtt_topic}","service started")
except ConnectionRefusedError:
    logger.error(f"... Connection refused ! We can't connect to the MQTT server at {my_mqtt_server}:{my_mqtt_port}.")
    logger.error(f"Exiting this service as it requires a proper connection to an MQTT server.")
    logger.info(f"Using environment variables (MQTT_SERVER, MQTT_PORT, MQTT_ALIVE, MQTT_BIND_ADDRESS) you can specify the MQTT server to connect to.")
    exit()

# ---------  connected to miband device -------------------------
def connect_to_miband_device():
    global mqtt_connected
    while not mqtt_connected:
        logger.info("Waiting for MQTT connect")
        time.sleep(1.5)
    logger.info("Infinite loop (re)connecting to miband device")
    while True:
        connect(miband_mac,miband_key)
        logger.info("Connected to miband device")
        my_mqtt_client.publish(f"{my_mqtt_topic}","connected")
        if connected:
            post_wait_for_notifications()
            logger.info("Disconnected to miband device")
            my_mqtt_client.publish(f"{my_mqtt_topic}","disconnected")
    return

# run connect_to_miband_device() in a separate thread.
import concurrent.futures
executor=concurrent.futures.ThreadPoolExecutor()
future = executor.submit(connect_to_miband_device)

logger.info("Starting FastAPI")
#-------------- Start FastAPI ----------------------
# configure uvicorn logging
log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = '%(asctime)-15s %(name)s (%(levelname)s) > %(message)s'
log_config["formatters"]["default"]["fmt"] = '%(asctime)-15s %(name)s (%(levelname)s) > %(message)s'
log_config["loggers"]["uvicorn"]["propagate"] = False
#log_config["loggers"]["uvicorn.error"]["propagate"] = False
# start api
uvicorn.run(app, host=my_api_host, port=my_api_port )
