#! /usr/bin/python3.6
import asyncio
import aiofiles

async def read_input():
    async with aiofiles.open('hello.txt', mode='rb') as f:
        while True:
            inp = await f.read(4)
            if not inp: break
            print('got :' , inp)

async def read_stdin():
    async with aiofiles.open('/dev/stdin', mode='rb') as f:
        while True:
            inp = await f.read(4)
            if not inp: break
            print('got :' , inp)

async def main():
    await asyncio.wait([read_stdin()])

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.run_forever()
