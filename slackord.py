import asyncio
import discord
import json
import time

from discord.ext import commands

bot = commands.Bot(command_prefix='!')

# Change the JSON file name in the quoted field below.
with open('test.json') as json_file:
    data = json.load(json_file)
    for message in data:
        # Print the messages we'll output to Discord
        # from the Slack JSON file into console for the user to see.
        if "real_name" in message.keys() and "datetime" in message.keys(
        ) and "text" in message.keys():
            print((message["datetime"]) + (': ') + (message["real_name"]) + (
                ': ') + (message["text"]))
            print (' ')
        elif "bot_message" in message.keys() and "text" in message.keys():
            print ("%s BOT MESSAGE" % (message["bot_message"]) + (
                ': ') + (message["text"]))


@bot.event
async def on_ready():
    print('Slackord is now ready to send messages to Discord!')
    print('Type !mergeslack in the channel you wish to send messages to.')
    print(' ')


# When !mergeslack is typed in a channel, iterate
# through the JSON file and post the message.
@bot.command(pass_context=True)
async def mergeslack(ctx):
    with open('test.json') as json_file:
        data = json.load(json_file)
        for message in data:
            if "real_name" in message.keys() and "datetime" in message.keys(
            ) and "text" in message.keys():
                messageToSend = ((message["datetime"]) + (': ') + (
                    message["real_name"]) + (': ') + (message["text"]))
                await ctx.send(messageToSend)
            elif "bot_message" in message.keys() and "text" in message.keys():
                messageToSend = ("%s BOT MESSAGE" % (
                    message["bot_message"]) + (': ') + (message["text"]))
                await ctx.send(messageToSend)


# Insert the Discord bot token into the quoted section below
bot.run(TOKENHERE)
