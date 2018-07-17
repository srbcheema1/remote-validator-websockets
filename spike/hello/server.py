#!/usr/bin/env python3.6

import asyncio
import websockets

async def hello(conn, path):
    name = await conn.recv()
    print(type(name))
    print("got : " , name)

    greeting = "Hello " + name.decode('ascii')
    await conn.send(greeting)

start_server = websockets.serve(hello, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
