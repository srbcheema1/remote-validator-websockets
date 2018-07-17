import abc
import asyncio
from d_1_networking.esercizio_soluzione.SOversion.dummydb import DummyDB as DB


class Command(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def run(self, a, b, c):
        raise NotImplementedError()


class XCommand(Command):
    @classmethod
    def run(cls, db, param1=None, param2=None):
        res = db.x()
        if not res:
            return '>>>>>>>>>>> Empty response! <<<<<<<<<<<<<'
        return '\n'.join('{}: {}'.format(col, val) for col, val in res.items())


class YCommand(Command):
    @classmethod
    def run(cls, db, param1=None, param2=None):
        db.y(param1)
        return 'Operation Y OK: {}'.format(param1)


class QuitCommand(Command):
    @classmethod
    def run(cls, rubrica_db, param1=None, param2=None):
        return 'Disconnected...'

class CommandFactory:
    _cmds = {'X': XCommand,
         'Y': YCommand,
         'DISCONNECT': QuitCommand}

    @classmethod
    def get_cmd(cls, cmd):
        tokens = cmd.split(':')
        cmd = tokens[0]
        if len(tokens) == 1:
            nome, numero = None, None
        else:
            nome, numero = (tokens[1], tokens[2]) if len(tokens) == 3 else (tokens[1], None)
        cmd_cls = cls._cmds.get(cmd)
        return cmd_cls, nome, numero

class Server(asyncio.Protocol):
    db_filename = '../data/exercise.db'
    db = DB(db_filename)

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        cmd_cls, param1, param2 = CommandFactory.get_cmd(message)
        res = cmd_cls.run(self.db, param1, param2)
        print('Sending response: {!r}'.format(res))
        self.transport.write(bytes(res, encoding='UTF-8'))

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # Each client connection will create a new protocol instance
    coro = loop.create_server(RubricaServer, '127.0.0.1', 10888)
    server = loop.run_until_complete(coro)

    # Serve requests until Ctrl+C is pressed
    print('Serving on {}'.format(server.sockets[0].getsockname()))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    # Close the server
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
