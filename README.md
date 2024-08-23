# IRC.PY

An IRC library for python.
Example code can be found in "example-bot.py".

### Keep in mind that when using the following functions to keep the correct variable order:
async def message_received(message, user, channel, **kwargs) for message_received;
async def commandname(arguments, user, channel, msg, **kwargs) for commands;
async def ready(nickname, channel) for ready.

When running your bot, keep in mind that Bot.connect() is non-asynchronous while Bot._connect() is.
