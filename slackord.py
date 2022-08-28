# Slackord 1.0 by Thomas Loupe

import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import json
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import *
from tkinter import simpledialog

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


def format_time(timestamp):
    """
    Given a timestamp in seconds (potentially fractional) since the epoch,
    format it in a useful human readable manner
    """
    return datetime.fromtimestamp(timestamp).isoformat(sep=' ', timespec='seconds')


def format_message(timestamp, real_name, message):
    """
    Given a timestamp, real name, and message from slack,
    format it into a message to post to discord
    """
    return f"{format_time(timestamp)} {real_name}: {message}"


# Create the popup window to enter the bot's token.
def SpawnTokenWindow():
    botToken = simpledialog.askstring(
        "Enter Token", "Please enter your Discord bot token here")
    if not botToken:
        frameBox.insert(tk.END, 'User cancelled or no token entered.')
        frameBox.yview(tk.END)
    else:
        # TODO: Thread this process with bot.start().
        bot.run(botToken)


def Output():
    filename = tk.filedialog.askopenfilename()
    with open(filename) as f:
        frameBox.insert(
            tk.END, 'Slackord will post the following messages to your desired Discord channel:')
        frameBox.yview(tk.END)
        for message in json.load(f):
            # Print the messages we'll output from Slack JSON file to Discord to GUI window.
            if "user_profile" in message and 'ts' in message and 'text' in message:
                timestamp = float(message['ts'])
                real_name = message['user_profile']['real_name']
                message_text = message['text']
                full_message_text = format_message(timestamp, real_name, message_text)
                frameBox.insert(tk.END, full_message_text)
                frameBox.yview(tk.END)

        # When !slackord is typed in a channel, iterate through the JSON file and post each message.
        @bot.command(pass_context=True)
        async def slackord(ctx):
            frameBox.insert(tk.END, 'Posting messages into Discord!')
            frameBox.yview(tk.END)
            with open(filename) as f:
                for message in json.load(f):
                    if "user_profile" in message and 'ts' in message and 'text' in message:
                        timestamp = float(message['ts'])
                        real_name = message['user_profile']['real_name']
                        message_text = message['text']
                        full_message_text = format_message(timestamp, real_name, message_text)
                        await ctx.send(full_message_text)
                        # Output to the GUI that the message was posted.
                        frameBox.insert(tk.END, 'Message posted!')
                        frameBox.yview(tk.END)


# Begin tkinter setup.
# Create tkinter instance.
window = tk.Tk()
# Set window title.
window.title("Slackord 1.0a by Thomas Loupe")
# Set window size.
window.geometry("500x300")
# Disallow window resizing.
window.resizable(False, False)

# Set up the file browse button.
tk.Button(window, text="Step 1: Select JSON File", command=Output).pack()

# Set up the token button
tk.Button(window, text="Step 2: Enter Bot Token",
          command=SpawnTokenWindow).pack()

# Create an empty text field and scrollbar to print updates and messages to.
frame = Frame(window)
scrollbar = Scrollbar(window)
scrollbar.pack(side=RIGHT, fill=Y)
frameBox = Listbox(window, yscrollcommand=scrollbar.set)
frameBox.pack(fill='both', expand=True)
scrollbar.config(command=frameBox.yview)

# Keep the application running unless closed.
window.mainloop()
