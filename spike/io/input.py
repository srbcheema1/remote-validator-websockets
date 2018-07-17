#! /usr/bin/python3.6
import asyncio
import os
import urllib.request
import sys
import threading

async def printer_coroutine(name):
    i = 0
    while ( i < 10 ):
        print (name + str(i))
        i += 1
        await asyncio.sleep(3)
    msg = 'Finished coroutine {name}'.format(name=name)
    return msg

def read_input():
    with sys.stdin.buffer as f:
        while True:
            inp = f.read(4)
            print('got ' , inp)


async def main():
    coroutines = [printer_coroutine('hello')]
    threading.Thread(target=read_input, daemon=True).start()
    completed, pending = await asyncio.wait(coroutines)
    for item in completed:
        print(item.result())


event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.run_forever()
