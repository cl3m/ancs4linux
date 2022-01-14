import logging
from typing import Dict, List
from time import sleep
import math
import typer
from ancs4linux.common.apis import ObserverAPI, ShowNotificationData
from ancs4linux.common.dbus import EventLoop, ObjPath, Str, Variant
from ancs4linux.common.external_apis import BluezRootAPI
import unicornhat as unicorn

#setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(1.0)
#get the width and height of the hardware
width, height = unicorn.get_shape()

log = logging.getLogger(__name__)
app = typer.Typer()
connected = False
observer_api: ObserverAPI

def new_notification(json: str) -> None:
    data = ShowNotificationData.parse(json)
    log.info(f"Notification from {data.app_name}")
    unicorn_on(0,255,0)
    

def dismiss_notification(id: int) -> None:
    log.info("Notification dismissed")
    unicorn_off()

def process_object(path: ObjPath, services: Dict[Str, Dict[Str, Variant]]
    ) -> None:
    global connected
    if connected is False:
        log.info("Device connected")
        unicorn_on(0,0,255)
        sleep(2.0)
        unicorn_off()
        connected = True

def remove_observers(path: ObjPath, services: List[Str]) -> None:
    global connected
    log.info("Device disconnected")
    unicorn_on(255,0,0)
    sleep(2.0)
    unicorn_off()
    connected = False

def unicorn_on(r: int, g: int, b: int) -> None:
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x,y,r,g,b)
            unicorn.show()

def unicorn_off() -> None:
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x,y,0,0,0)
            unicorn.show()

def unicorn_rainbow() -> None:
    i = 0.0
    offset = 30
    while i < 250:
            i = i + 0.5
            for y in range(height):
                    for x in range(width):
                            r = 0
                            g = 0
                            r = (math.cos((x+i)/2.0) + math.cos((y+i)/2.0)) * 64.0 + 128.0
                            g = (math.sin((x+i)/1.5) + math.sin((y+i)/2.0)) * 64.0 + 128.0
                            b = (math.sin((x+i)/2.0) + math.cos((y+i)/1.5)) * 64.0 + 128.0
                            r = max(0, min(255, r + offset))
                            g = max(0, min(255, g + offset))
                            b = max(0, min(255, b + offset))
                            unicorn.set_pixel(x,y,int(r),int(g),int(b))
            unicorn.show()
            sleep(0.01)
    unicorn_off()

@app.command()
def main(
    observer_dbus: str = typer.Option(
        "ancs4linux.Observer", help="Observer service path"
    ),
) -> None:
    logging.basicConfig(
        filename='/var/log/ancs4linux/unicorn.log',
        level=logging.DEBUG,
        format='%(asctime)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    loop = EventLoop()

    global observer_api
    observer_api = ObserverAPI.connect(observer_dbus)
    observer_api.ShowNotification.connect(new_notification)
    observer_api.DismissNotification.connect(dismiss_notification)

    global root_api
    root_api = BluezRootAPI.connect()
    root_api.InterfacesAdded.connect(process_object)
    root_api.InterfacesRemoved.connect(remove_observers)

    log.info("Rainbow time ...")
    unicorn_rainbow()
    log.info("Listening to notifications...")
    loop.run()

if __name__ == "__main__":
    app()