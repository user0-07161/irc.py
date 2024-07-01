# PyRC

An IRC library for python.

How to use:
```py
import irc.py.irc as irc
import asyncio
bot = irc.Bot(nickname="testingbot", server="irc.libera.chat", channel="##user0", prefix="tb?")
@bot.event
def echo(arguments, user, channel, msg, **kwargs):
   print(arguments)
   bot.send_message(arguments)
@bot.event
def ready(nickname, channel):
   print(f"Logged in as {nickname}, in {channel}!")
asyncio.run(bot.connect())
```
(This is very early-stage currently)
