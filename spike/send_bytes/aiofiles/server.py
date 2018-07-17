#!/usr/bin/env python3.6
import asyncio
import websockets

async def echo(conn, path):
    async for message in conn:
        print('got ',message)

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(websockets.serve(echo, '127.0.0.1', 12321))
event_loop.run_forever()
