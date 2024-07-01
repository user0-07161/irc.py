import ircpy as irc
import asyncio
bot = irc.Bot(nickname="testingbot", server="irc.libera.chat", channel="#botters-test", prefix="tb?")
@bot.event
def echo(arguments, user, channel, msg, **kwargs):
   print(arguments)
   bot.send_message(' '.join(arguments))
@bot.event
def test(arguments, user, channel, msg, **kwargs):
   bot.send_message(f"You are {user}, in {channel}, and your message was {msg}. I detected the following arguments: {arguments}.")
@bot.event
def ready(nickname, channel):
   print(f"Logged in as {nickname}, in {channel}!")
asyncio.run(bot.connect())
