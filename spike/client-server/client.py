import abc
from asyncio import *
from aioconsole import ainput

MENU = '''
---------------------------
A) Command X
B) Command Y (require additional input)
C) Quit program
---------------------------
'''

loop_ = get_event_loop()


class Command(metaclass=abc.ABCMeta):
    asyn = False

    def __init__(self, tcp_client):
        self.client = tcp_client

    @abc.abstractmethod
    def run(self):
        raise NotImplementedError()


class ACommand(Command):
    def run(self):
        # send X command to server
        self.client.send_data_to_tcp('X:')


class BCommand(Command):
    asyn = True
    async def run(self):
        s = await ainput('Insert data for B operation (es. name:43d3HHte3) > ')
        # send Y command to server
        self.client.send_data_to_tcp('Y:' + s)


class QuitCommand(Command):
    def run(self):
        self.client.send_data_to_tcp('DISCONNECT:')
        print('Goodbye!!!')
        self.client.disconnect()
        exit()


class CommandFactory:
    _cmds = {'A': ACommand,
         'B': BCommand,
         'C': QuitCommand}

    @classmethod
    def get_cmd(cls, cmd):
        cmd = cmd.strip()
        cmd_cls = cls._cmds.get(cmd)
        return cmd_cls


class Client(Protocol):
    def __init__(self, loop):
        self.loop = loop
        self.transport = None

    def disconnect(self):
        self.loop.stop()

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print('Data received from server: \n===========\n{}\n===========\n'.format(data.decode()), flush=True)

    def send_data_to_tcp(self, data):
        self.transport.write(data.encode())

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()


def menu():
    print(MENU)


async def main():
    menu()
    while True:
        cmd = await ainput('Insert Command >')
        cmd_cls = CommandFactory.get_cmd(cmd)
        if not cmd_cls:
            print('Unknown: {}'.format(cmd))
        elif cmd_cls.asyn:
            await cmd_cls(client).run()
        else:
            cmd_cls(client).run()


if __name__ == '__main__':
    client = Client(loop_)
    coro = loop_.create_connection(lambda: client, '127.0.0.1', 10888)
    loop_.run_until_complete(coro)
    loop_.run_until_complete(main())
