#!/usr/bin/python3.6
import asyncio
import websockets
import threading
import sys
from aioconsole import ainput

def send_input_binary(conn):
    with sys.stdin.buffer as f:
        while True:
            inp = f.read(4)
            conn.send(inp)
            print('sent ' , inp)

async def send_input_async(conn):
    while True:
        inp = await ainput()
        await conn.send(inp)
        print('sent ' , inp)

async def start_client(uri):
    async with websockets.connect(uri) as conn:
        inp_type = "binary"
        if (inp_type == "binary"):
            t = threading.Thread(target=send_input_binary, args=[conn], daemon=True)
            t.start()
            t.join()
        else:
            await asyncio.wait([ send_input_async(conn)])

asyncio.get_event_loop().run_until_complete(start_client('ws://127.0.0.1:12321'))
