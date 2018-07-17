#!/usr/bin/env python3.6

import argparse
import asyncio
import queue
import sys
import threading
import time
import websockets
from asyncio import subprocess as sp, create_subprocess_exec as create_sp
import subprocess as sp

from aioconsole import ainput
from concurrent import futures
from select import select
from random import randint

from util.enc_dec import enc, dec
from util.string_constants import vcf_path, end_of_report_neg, end_of_report
from util.defaults import default_port, default_ip
from util.files import get_files_in_dir, clean_folder, del_folder, verify_file
from util.version import check_version


class Remote_Validator:
    def __init__(self, ip='127.0.0.1', port=12321):
        self.event_loop = asyncio.get_event_loop()
        self.ip = ip
        self.port = port
        self.output_dir = "./bin/out/"
        self.validator = None

    def start(self):
        self.event_loop.run_until_complete(websockets.serve(self.echo, self.ip, self.port))
        self.event_loop.run_forever()

    def endl(self,data):
        if (type(data) is str):
            data = enc(data)

        if (len(data) == 0):
            return data

        if(data[-1] == enc('\n')):
            return data
        else:
            return data + enc('\n')

    def make_reply(self, reply):
        if (type(reply) is not str):
            reply = dec(reply)

        if(len(reply) == 0):
            return reply

        if(reply[-1]=='\n'):
            return reply[:-1]


    async def send_output(self, conn):
        while (self.validator == None): # yet not started
            await asyncio.sleep(0.1)

        while (len(get_files_in_dir(self.output_dir)) == 0):
            await asyncio.sleep(0.01)
            output_file = get_files_in_dir(self.output_dir)

        output_file = get_files_in_dir(self.output_dir)[0]
        output_file_path = self.output_dir + output_file

        output_vcf = await create_sp("tail", "-n", "999999", "-f",output_file_path, stdout=sp.PIPE)

        while (True): # validator alive or dead we will continue
            reply = await output_vcf.stdout.readline()
            reply = self.make_reply(reply)
            await conn.send(reply)
            if(reply == end_of_report or reply == end_of_report_neg):
                break

        print("Result completes :)")
        clean_folder(self.output_dir)
        del_folder(self.output_dir)
        reply = "bye"
        await conn.send(reply)

    def enqueue_output(self, out, queue):
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()

    async def receive_input(self, conn):
        clean_folder(self.output_dir)
        self.validator = await create_sp(vcf_path,"-r","text","-o",self.output_dir, stdin=sp.PIPE)

        async for message in conn:
            if(message == "bye"):
                print('EOF to validator')
                self.validator.stdin.close()
                break
            print(':>> ' + message)
            self.validator.stdin.write(self.endl(message))


    async def echo(self, conn, path):
        await asyncio.wait([
            self.send_output(conn),
            self.receive_input(conn)
            ])


if (__name__ == "__main__"):
    if(check_version() != "3.6"):
        print("use python3.6")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port",default=default_port, help="PORT number eg:- 12321")
    parser.add_argument("-i", "--ip",default=default_ip, help="IP adress eg:- 127.0.0.1")
    args = parser.parse_args()

    ip = args.ip
    port = int(args.port)

    validator = Remote_Validator(ip, port)
    validator.start()
