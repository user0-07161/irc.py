import asyncio
import telnetlib3
import re
class Bot:
    def __init__(self,  **kwargs):
        self._events = {}
        self._args = kwargs
        global nickname
        global server
        global channel
        global port
        global prefix
        nickname = self._args["nickname"]
        server = self._args["server"]
        channel = self._args["channel"]
        try:
            port = int(self._args["port"])
        except:
            port = 6667
        try:
            prefix = self._args["prefix"]
        except:
            prefix = "!"
    def send_message(self, message):
        self.writer.write(f"PRIVMSG {channel} :{message}\r\n")
    def send_raw(self, raw):
        self.writer.write(f"{raw}\r\n")
    def event(self, func):
        event_name = func.__name__
        if event_name not in self._events:
            self._events[event_name] = []
        self._events[event_name].append(func)
        print(f"DEBUG: {event_name}")
        return func
    async def callevent(self, event, *args):
        try:
            tasks = []
            for handler in self._events[event]:
                if asyncio.iscoroutinefunction(handler):
                    tasks.append(handler(*args))
                else:
                    handler(*args)
            if tasks:
                await asyncio.gather(*tasks)
        except:
            pass
    def connect(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self._connect())
    async def _connect(self):
        self.reader, self.writer = await telnetlib3.open_connection(
            server, port, encoding='utf-8'
        )
        self.writer.write(f"NICK {nickname}\r\n")
        self.writer.write(f"USER {nickname} 0 * :{nickname}\r\n")
        self.writer.write(f"JOIN {channel}\r\n")
        self.writer.write(f"PRIVMSG {channel} :Logged in.\r\n")
        await self.callevent("ready", nickname, channel)
        while True:
            line = await self.reader.readline()
            if not line:
                break
            await self.handle_line(line.strip())
    async def handle_line(self, line):
        if line.startswith("PING"):
            self.writer.write(f"PONG {line.split()[1]}\r\n")
        elif "PRIVMSG" in line:
           splittedline = line.split('PRIVMSG')[0]
           msg = re.findall(f"(?<={channel} :).*$", line)
           if msg:
               msg = msg[0]
           user = re.findall("(?<=~).*(?=@)", splittedline)
           if user:
               user = user[0]
           if not prefix in line:
               await self.callevent("message_received", msg, user, channel)
           else:
               try:
                   msg_splitted = msg.split(' ')
               except:
                   msg_splitted = msg
               try:
                   cmd = msg_splitted[0].replace(prefix, '')
               except:
                   cmd = msg_splitted
               arguments = []
               for arg in msg_splitted:
                   if prefix in arg:
                       pass
                   else:
                       arguments.append(arg)
               await self.callevent(cmd, arguments, user, channel, msg)
