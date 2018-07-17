#!/usr/bin/env python3.6

import argparse
import asyncio
import websockets

from aioconsole import ainput

from util.defaults import default_ip, default_port, connection_timeout

async def send_input(conn):
    while True:
        try:
            inp = await ainput()
        except:
            await conn.send("bye")
            break
        await conn.send(inp)


async def receive_output(conn):
    async for message in conn:
        if(message == "bye"):
            break
        print(message)

async def start_client(uri):
    async with websockets.connect(uri) as conn:
        await asyncio.wait([
            send_input(conn),
            receive_output(conn)
            ])

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default=default_port, help="PORT number eg:- 12321")
    parser.add_argument("-i", "--ip",default=default_ip, help="IP adress eg:- 127.0.0.1")
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)

    asyncio.get_event_loop().run_until_complete(
            start_client('ws://'+ip+':'+str(port))
        )
