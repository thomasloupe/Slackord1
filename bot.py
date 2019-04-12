import discord
import json

from discord.ext import commands

TOKEN = ''

bot = commands.Bot(command_prefix = '!')

with open('test.json') as json_file:
    data = json.load(json_file)
    for message in data:
        print(message["real_name"])
        print(message["datetime"])
        print(message["text"])
        print (' ')

@bot.event
async def on_ready():
    print('Bot ready for parsing JSON!')

@bot.command(pass_context=True)
async def mergeslack(ctx):
    for message in data:
        await ctx.send(message["real_name"])
        await ctx.send(message["datetime"])
        await ctx.send(message["text"])

bot.run(TOKEN)