#! /usr/bin/python3.6
import asyncio
import aiofiles
import aioconsole

# works fine on compressed files but platform dependent
# we can use sys.stdin.fileno() in place of /dev/stdin
async def read_using_aiofile():
    async with aiofiles.open('/dev/stdin', mode='rb') as f:
        while True:
            inp = await f.read(4)
            if not inp: break
            print('got :' , inp)

# fails on compresed file
async def read_using_aioconsole():
    stdin, _ = await aioconsole.get_standard_streams()
    while True:
        line = await stdin.read(4)
        if not line: break
        print('got',line)

async def main():
    # await asyncio.wait([read_using_aioconsole()])
    await asyncio.wait([read_using_aiofile()])

event_loop = asyncio.get_event_loop()
event_loop.run_until_complete(main())
event_loop.run_forever()
