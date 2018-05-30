#!/usr/bin/env python3
# -*- coding : utf-8 -*-

from asyncore import dispatcher
from asynchat import async_chat
import asyncore
import socket

PORT = 5050
NAME = 'MyChat'


class EndSession(Exception):
    pass

class CommandHandler:
    def unknown(self, session, cmd):
        session.push('Unknown command: {}\n'.format(cmd).encode('utf-8'))
    def handle(self, session, data):
        if not data:
            return
        part = data.split(' ', 1)
        cmd = part[0].strip()
        try:
            line = part[1].strip()
        except IndexError:
            line = ''
        meth = getattr(self, 'do_'+cmd, None)
        try:
            meth(session, line)
        except TypeError:
            self.unknown(session, cmd)


class Room(CommandHandler):
    def __init__(self, server):
        self.server = server
        self.sessions = []
    def add(self, session):
        self.sessions.append(session)
    def remove(self, session):
        self.sessions.remove(session)
    def broadcost(self, data):
        for session in self.sessions:
            session.push(data.encode('utf-8'))
    def do_logout(self, session, data):
        raise EndSession

class LoginRoom(Room):
    def add(self, session):
        session.push('Welcome to {}\n'.format(self.server.name).encode('utf-8'))
        super().add(session)

    def unknown(self, session, cmd):
        session.push('Please log in\nUse "login <nick>"\n'.encode('utf-8'))
    def do_login(self, session, data):
        name = data.strip()
        if not name:
            session.push('Please enter a name\n'.encode('utf-8'))
        elif name in self.server.users:
            session.push('The name "{}" has been taken\n'.format(name).encode('utf-8'))
            session.push('Please try again'.encode('utf-8'))
        else:
            session.name = name
            #self.server.users.append(name)
            session.enter(self.server.main_room)

class LogoutRoom(Room):
    def add(self, session):
        try:
            del self.server.users[session.name]
        except KeyError:
            pass

class ChatRoom(Room):
    def add(self, session):
        self.broadcost(session.name + ' has entered the room\n')
        self.server.users[session.name] = session
        super().add(session)
    def remove(self, session):
        super().remove(session)
        self.broadcost(session.name + ' has left the room\n')

    def do_say(self, session, data):
        self.broadcost(session.name + ': ' + data + '\n')
    def do_look(self, session, data):
        for other in self.sessions:
            if other.name != session.name:
                session.push((other.name + '\n').encode('utf-8'))
    def do_who(self, session, data):
        session.push('The following are logged in:\n'.encode('utf-8'))
        for name in self.server.users:
            session.push((name + '\r\n').encode('utf-8'))
class ChatSession(async_chat):
    def __init__(self, server, conn):
        super().__init__(conn)
        self.server = server
        self.set_terminator(b"\r\n")
        self.data = []
        self.name = None
        self.enter(LoginRoom(server))
    def enter(self, room):
        try:
            cur = self.room
        except AttributeError:
            pass
        else:
            cur.remove(self)
        self.room = room
        room.add(self)
    def collect_incoming_data(self, data):
        try:
            self.data.append(data)
        except TypeError as e:
            print(e)
    def found_terminator(self):
        data = b"".join(self.data).decode('utf-8')
        self.data = []
        try:
            self.room.handle(self, data)
        except EndSession:
            self.handle_close()

    def handle_close(self):
        async_chat.handle_close(self)
        self.enter(LogoutRoom(self.server))


class ChatServer(dispatcher):
    def __init__(self, port, name):
        super().__init__()
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind(('', port))
        self.listen(5)

        self.users = {}
        self.name = name
        self.main_room = ChatRoom(self)
    def handle_accept(self):
        conn, addr = self.accept()
        ChatSession(self, conn)


if __name__ == '__main__':
    s = ChatServer(PORT, NAME)
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print()