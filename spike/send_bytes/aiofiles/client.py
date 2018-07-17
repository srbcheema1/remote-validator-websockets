#!/usr/bin/python3.6
import asyncio
import websockets
import threading
import sys
from aioconsole import ainput
import aiofiles

def send_input_binary(conn):
    with sys.stdin.buffer as f:
        while True:
            inp = f.read(4)
            print(type(inp))
            conn.send(inp)
            print('sent ' , inp)

# works fine
async def send_input_binary_async(conn):
    async with aiofiles.open('hello.txt', mode='rb') as f:
        while True:
            inp = await f.read(4)
            if not inp:
                break
            await conn.send(inp)
            print('sent ' , inp)

# works fine
async def send_input_string_async(conn):
    while True:
        inp = await ainput()
        await conn.send(inp)
        print('sent ' , inp)

async def start_client(uri):
    async with websockets.connect(uri) as conn:
        inp_type = "binary"
        inp_type = "binary_async"
        if (inp_type == "binary"):
            t = threading.Thread(target=send_input_binary, args=[conn], daemon=True)
            t.start()
            t.join()
        elif (inp_type == "binary_async"):
            await asyncio.wait([ send_input_binary_async(conn)])
        else:
            await asyncio.wait([ send_input_string_async(conn)])

asyncio.get_event_loop().run_until_complete(start_client('ws://127.0.0.1:12321'))
