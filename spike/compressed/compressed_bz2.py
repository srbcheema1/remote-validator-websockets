#! /usr/bin/env python3.6
import bz2
import sys
import asyncio



file_ = sys.stdin.buffer
data = sys.stdin.buffer.read(4)
print(data)
sys.stdin.seek(0)


async def print_num():
    i = 1
    while True:
        print(i)
        i += 1
        await asyncio.sleep(1)

async def print_file():
    with sys.stdin as f:
        # await for line in f:
        for line in f:
            print(line,end='')
            await asyncio.sleep(1)

async def print_bz2_file():
    with bz2.open(file_,'r') as f:
        for line in f:
            print(line.decode('UTF-8'),end = '')
            await asyncio.sleep(1)

async def process():
        await asyncio.wait([
            print_file(),
            print_num()
            ])

if (__name__ == "__main__"):
    asyncio.get_event_loop().run_until_complete(process())
