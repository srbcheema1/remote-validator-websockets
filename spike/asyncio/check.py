#!/usr/bin/env python3.6

'''
works fine as ./check.py
but breaks if ./check.py < file.txt
'''
import asyncio
from aioconsole import ainput

async def read_input():
    while True:
        inp = await ainput()
        print('got ' + inp)

if (__name__ == "__main__"):
    asyncio.get_event_loop().run_until_complete(read_input())
