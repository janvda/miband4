# see https://fastapi.tiangolo.com/

import uvicorn, json, random, os, logging, threading, time

from logging.config            import dictConfig
from miband_api_logging_config import LogConfig

from typing    import Optional
from fastapi   import FastAPI, HTTPException
from pydantic  import BaseModel
from miband    import miband
from functools import wraps
from constants import MUSICSTATE
from paho.mqtt import client as mqtt_client

# global variables
band           = None 
connected      = False

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
        logger.info(f"{func.__name__}: acquiring lock ...")
        miband_lock.acquire()
        try:
            rc=func(*args, **kwargs)
        finally:
            miband_lock.release()
            logger.info(f"{func.__name__}:...lock released")
        return rc
    return wrapper

app = FastAPI()

@app.get("/")
def read_root():
    return {"info": "TO DO"}

@app.post("/connect")
def connect(mac_address: str,authentication_key:str):
    global connected, band
    if connected :
        band.disconnect()
    try:
        band = miband(mac_address, 
                      bytes.fromhex(authentication_key), 
                    debug=True)
        connected = band.initialize()    
        # set music callbacks
        band.setMusicCallback(_default_music_play,_default_music_pause, _default_music_forward,
                             _default_music_back,_default_music_vup,_default_music_vdown,
                             _default_music_focus_in,_default_music_focus_out)
        return connected
    except BaseException as error:
        error_str = format(error)
        if "non-hexadecimal number found in fromhex()" in error_str:
            error_str = "Authentication key has not the format of a hexadecimal number !"
        logger.error(error_str)
        raise HTTPException(status_code=400, detail=error_str)

@app.get("/info")
@return_404_if_not_connected
@protect_by_miband_lock
def get_info():
    info = { "Soft revision" : band.get_revision(),
             "Hardware revision" : band.get_hrdw_revision(),
             "Serial" : band.get_serial(),
             "Battery" : band.get_battery_info()['level'],
             "Time" : band.get_current_time()['date'].isoformat()
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

@app.post("/wait_for_notifications")
@return_404_if_not_connected
def post_wait_for_notifications():
    logger.info("Waiting for notifications - infinite loop - never returning !")
    while True:
        miband_lock.acquire()
        try:
            notification_received = band.waitForNotifications(0.5)
        except BaseException as error:
            logger.exception(format(error))
        finally:
            miband_lock.release()
            if not notification_received:
                time.sleep(0.3)
    return "error - this should not happen"

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
    band.setMusicCallback(cb_music_play,     cb_music_pause,    cb_music_forward,
                          cb_music_back,     cb_music_vup,      cb_music_vdown,
                          cb_music_focus_in, cb_music_focus_out)
    logger.info(f"band.setTrack({music_state},{artist},{album},{title},{volume},{position},{duration})")
    band.setTrack(music_state,artist,album,title,volume,position,duration)
    return "ok"

#   -------- TO DELETE ?? ---------------
class Connection_params(BaseModel):
    mac_address: str
    authentication_key: str

@app.post("/connect_old")
def connect_old(connection_params: Connection_params):
    global connected, band
    if connected :
        band.disconnect()
    try:
        band = miband(connection_params.mac_address, 
                      bytes.fromhex(connection_params.authentication_key), 
                    debug=True)
        connected = band.initialize()    
        return connected
    except BaseException as error:
        raise HTTPException(status_code=400, detail=format(error))
#   ----------------------------------------------

# default callbacks        
def cb_music_play():
    logger.info("Play")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","play")
def cb_music_pause():
    logger.info("Pause")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","pause")
def cb_music_forward():
    logger.info("Forward")
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
    logger.info("Music focus in")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","focus in")
def cb_music_focus_out():
    logger.info("Music focus out")
    my_mqtt_client.publish(f"{my_mqtt_topic}/music","focus out")

my_mqtt_client       = None
my_mqtt_client_name  = os.getenv("MQTT_CLIENT_NAME","miband-api-service")
my_mqtt_server       = os.getenv("MQTT_SERVER","127.0.0.1")
my_mqtt_port         = int(os.getenv("MQTT_PORT","1883"))
my_mqtt_alive        = int(os.getenv("MQTT_ALIVE","60"))
my_mqtt_bind_address = os.getenv("MQTT_BIND_ADDRESS","")
my_mqtt_topic        = os.getenv("MQTT_TOPIC","/miband-api")

my_api_host          = os.getenv("API_HOST","0.0.0.0") # Bind socket to this host.
my_api_port          = int(os.getenv("API_PORT","8001"))

if __name__ == "__main__":
    # logging initialization 
    #   see https://stackoverflow.com/questions/63510041/adding-python-logging-to-fastapi-endpoints-hosted-on-docker-doesnt-display-api
    dictConfig(LogConfig().dict())
    logger = logging.getLogger("miband_api")

    # The miband operations are based on the bluepy library which is not threadsafe.  
    # This miband_locak will be used to assure that miband operations are NOT executed in parallel.
    miband_lock = threading.Lock()

    # connect to mqtt broker
    def on_connect(client, userdata, flags, rc):
        global mqtt_connected
        if rc == 0:
            mqtt_connected = True
            logger.info("... connected to MQTT Broker!")
        else:
            logger.error("... failed to connect, return code %d\n", rc)

    mqtt_connected = False
    my_mqtt_client = mqtt_client.Client(my_mqtt_client_name)
    my_mqtt_client.on_connect = on_connect
    try:
        logger.info("Connecting to MQTT broker (%s:%s alive=%s, bind_address=%s)...",
                     my_mqtt_server,my_mqtt_port,my_mqtt_alive,my_mqtt_bind_address)
        my_mqtt_client.connect( my_mqtt_server,my_mqtt_port,my_mqtt_alive,my_mqtt_bind_address)
        my_mqtt_client.loop_start()
    except ConnectionRefusedError:
        logger.error(f"... Connection refused ! We can't connect to the MQTT server at {my_mqtt_server}:{my_mqtt_port}.")
        logger.error(f"Exiting this service as it requires a proper connection to an MQTT server.")
        logger.info(f"Using environment variables (MQTT_SERVER, MQTT_PORT, MQTT_ALIVE, MQTT_BIND_ADDRESS) you can specify the MQTT server to connect to.")
        exit()

    # configure uvicorn logging
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s [%(levelname)s] %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s [%(levelname)s] %(message)s"
    # start app
    uvicorn.run(app, host=my_api_host, port=my_api_port )
