# see https://fastapi.tiangolo.com/

import uvicorn, json, random, os, logging

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

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.put("/mqtt_broker")
def connect_mqtt_broker(server: str = "127.0.0.1",port:int = 1883,keepalive:int=60, bind_address:str=""):
    global mqtt_connected, my_mqtt_client

    def on_connect(client, userdata, flags, rc):
        global mqtt_connected
        if rc == 0:
            mqtt_connected = True
            logging.info("Connected to MQTT Broker!")
        else:
            logging.info("Failed to connect, return code %d\n", rc)

    if mqtt_connected :
        logging.warning("Already connected to mqtt broker")
    else:
        try:
            my_mqtt_client = mqtt_client.Client(f'miband-service-{random.randint(0, 1000)}')
            my_mqtt_client.on_connect = on_connect
            my_mqtt_client.connect(server,port,keepalive,bind_address)
            my_mqtt_client.loop_start()   
            return
        except BaseException as error:
            raise HTTPException(status_code=400, detail=format(error)) 

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
        return connected
    except BaseException as error:
        raise HTTPException(status_code=400, detail=format(error))

@app.get("/info")
@return_404_if_not_connected
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
def get_step_count():
    return band.get_steps()

@app.get("/battery_info")
@return_404_if_not_connected
def get_info():
    return band.get_battery_info()

@app.get("/current_time")
@return_404_if_not_connected
def get_current_time():
    return band.get_current_time()

@app.get("/heart_rate")
@return_404_if_not_connected
def get_heart_rate():
    return band.get_heart_rate_one_time()
 
@app.post("/message")
@return_404_if_not_connected
def post_message(message: str, title: str = "New Message"):
    return  band.send_custom_alert(5,title,message)

@app.post("/mail")
@return_404_if_not_connected
def post_mail(message: str, title: str = "New Mail"):
    return  band.send_custom_alert(1,title,message)

@app.post("/call")
@return_404_if_not_connected
def post_call(message: str, title: str = "New Call"):
    return  band.send_custom_alert(3,title,message)

@app.post("/missed_call")
@return_404_if_not_connected
def post_message(message: str, title: str = "Missed Call"):
    return  band.send_custom_alert(3,title,message)

@app.post("/music")
@return_404_if_not_connected
def post_music(artist: str = "No Artist", 
               album: str = "No Album",
               title: str = "No Title",
               playing: bool = True,
               volume: int = 50,
               position: int= 50,
               duration: int=100
               ):
    music_state = MUSICSTATE.PLAYED if playing else MUSICSTATE.PAUSED
    return  band.setTrack(music_state,artist,album,title,volume,position,duration)

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

    # start app
    uvicorn.run(app, host=my_api_host, port=my_api_port )

