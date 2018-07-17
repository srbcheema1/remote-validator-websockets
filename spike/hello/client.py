#!/usr/bin/env python3.6

import asyncio
import websockets

async def hello():
    async with websockets.connect('ws://localhost:8765') as conn:
        name = input("What's your name? ")
        await conn.send(name.encode('ascii'))
        greeting = await conn.recv()
        print(greeting)

asyncio.get_event_loop().run_until_complete(hello())
