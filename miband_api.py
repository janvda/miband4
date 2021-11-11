# see https://fastapi.tiangolo.com/

import uvicorn

from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from miband import miband

# global variables
band = None 
connected = False

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/connect/")
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

@app.get("/step_count")
def get_step_count():
    if connected:
        return band.get_steps()
    else:
        raise HTTPException(status_code=404, detail="Not connected to miband device - you need to (re)connect first before using this operation.")

@app.get("/battery_info")
def get_info():
    if connected:
        return band.get_battery_info()
    else:
        raise HTTPException(status_code=404, detail="Not connected to miband device - you need to (re)connect first before using this operation.")

@app.get("/current_time")
def get_current_time():
    if connected:
        return band.get_current_time()
    else:
        raise HTTPException(status_code=404, detail="Not connected to miband device - you need to (re)connect first before using this operation.")

@app.post("/message")
def post_message(message: str, title: str = "New Message"):
    if connected:
        return  band.send_custom_alert(5,title,message)
    else:
        raise HTTPException(status_code=404, detail="Not connected to miband device - you need to (re)connect first before using this operation.")

class Connection_params(BaseModel):
    mac_address: str
    authentication_key: str

@app.post("/connect_old/")
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)

