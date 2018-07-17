#! /usr/bin/env python3.6
import asyncio
import os
import urllib.request
from aioconsole import ainput

async def printer_coroutine(name):
    i = 0
    while ( i < 10 ):
        print (name + str(i))
        i += 1
        await asyncio.sleep(3)
    msg = 'Finished coroutine {name}'.format(name=name)
    return msg

async def read_input():
    while True:
        inp = await ainput()
        print('got ' + inp)


async def main(names):
    # coroutines = [printer_coroutine(name) for name in names]
    coroutines = [printer_coroutine(names[0]),read_input()]
    completed, pending = await asyncio.wait(coroutines)
    for item in completed:
        print(item.result())


if __name__ == '__main__':
    names = ["srb",
            # "a",
            # "b",
            # "c",
            "cheema"
            ]

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(main(names))
    finally:
        event_loop.run_forever()
