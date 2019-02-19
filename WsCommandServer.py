import asyncio
import json
import inspect
import pyautogui
import websockets


class WsCommandServer:

    async def mouse_press(self, params):
        pyautogui.mouseDown(button=params["button"], x=params["x"], y=params["y"])
        pass

    async def mouse_release(self, params):
        pyautogui.mouseUp(button=params["button"], x=params["x"], y=params["y"])
        pass

    async def keyboard_press(self, params):
        pyautogui.keyDown(params['code'])
        pass

    async def keyboard_release(self, params):
        pyautogui.keyDown(params['code'])
        pass

    async def commands_switch(self, websocket, path):
        async for message in websocket:
            data = json.loads(message)
            class_methods = [i for i in dir(WsCommandServer) if not inspect.isfunction(i) and '__' not in i]
            if data["command"] in class_methods:
                func = getattr(self, data["command"])
                await func(data["params"])
            else:
                print("unrecognizable action!")


def run_ws_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    asyncio.get_event_loop().run_until_complete(
        websockets.serve(WsCommandServer().commands_switch, 'localhost', 1553))
    asyncio.get_event_loop().run_forever()
