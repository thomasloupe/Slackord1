from discord.ext import commands
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import simpledialog
from tkinter import *
import asyncio
import discord
import json
import time

bot = commands.Bot(command_prefix='!')


def ParseAndPost():
    filename = tk.filedialog.askopenfilename()
    with open(filename) as json_file:
        data = json.load(json_file)
    for message in data:
        # Print the messages we'll output from Slack JSON file to Discord to GUI window.
        if "real_name" in message.keys() and "datetime" in message.keys(
        ) and "text" in message.keys():
            frameBox.insert((tk.END, message["datetime"]) + (': ') + (message["real_name"]) + (
                ': ') + (message["text"]))
            frameBox.yview(tk.END)
            frameBox.insert(tk.END, ' ')
            frameBox.yview(tk.END)
        elif "bot_message" in message.keys() and "text" in message.keys():
            frameBox.insert(tk.END, "%s BOT MESSAGE" % (message["bot_message"]) + (
                ': ') + (message["text"]))
    # Notify user that the bot is ready to post messages to Discord once JSON file has been read.
    @bot.event
    async def on_ready():
        frameBox.insert(
            tk.END, '-------------------------------------------------------------')
        frameBox.yview(tk.END)
        frameBox.insert(tk.END, 'Slackord is connected to Discord!')
        frameBox.yview(tk.END)
        frameBox.insert(
            tk.END, 'Load a JSON file then type !mergeslack in the Discord channel you wish to post messages to.')
        frameBox.yview(tk.END)
        frameBox.insert(
            tk.END, '-------------------------------------------------------------')
        frameBox.yview(tk.END)
    # When !mergeslack is typed in a channel, iterate through the JSON file and post each message.
    @bot.command(pass_context=True)
    async def mergeslack(ctx):
        with open(filename) as json_file:
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


# Create the popup window to enter the bot's token.
def EnterToken():
    botToken = simpledialog.askstring(
        "Enter Token", "Please enter your Discord bot token here")
    if not botToken:
        frameBox.insert(tk.END, 'User cancelled or no token.')
        frameBox.yview(tk.END)
    else:
        bot.run(botToken)


# Begin tkinter setup.

# Create tkinter instance.
window = tk.Tk()
# Set window title.
window.title("Slackord")
# Set window size.
window.geometry("500x500")
# Disallow window resizing.
window.resizable(False, False)

# Set up the token button
tk.Button(window, text="Enter Token", command=EnterToken).pack()

# Set up the browse button.
tk.Button(window, text="Select JSON File", command=ParseAndPost).pack()

# Create an empty text field and scrollbar to print updates and messages to.
frame = Frame(window)
scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)
frameBox = Listbox(window, yscrollcommand=scrollbar.set)
frameBox.pack(fill='both', expand=True)
scrollbar.config(command=frameBox.yview)

# Keep the application running unless closed.
window.mainloop()
