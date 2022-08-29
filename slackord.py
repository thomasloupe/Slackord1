# Slackord 1.0 by Thomas Loupe

import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import json
# from pprint import pprint
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
        # XXX the bot is functional, but the GUI hangs after entering the token and never returns
        bot.run(botToken)


def parse_json_slack_export(filename):
    """
    Parse a JSON file that contains the exported messages from a slack channel

    Return a dict where:
    - the keys are the timestamps of the slack messages
    - the values are tuples of length 2
      - the first item is the formatted string of a message ready to post to discord
      - the second item is a dict if this message has a thread, otherwise None.
        - the keys are the timestamps of the messages within the thread
        - the values are the formatted strings of the messages within the thread
    """
    parsed_messages = dict()
    with open(filename) as f:
        for message in json.load(f):
            if 'user_profile' in message and 'ts' in message and 'text' in message:
                timestamp = float(message['ts'])
                real_name = message['user_profile']['real_name']
                message_text = message['text']
                full_message_text = format_message(timestamp, real_name, message_text)

                if 'replies' in message:
                    # this is the head of a thread
                    parsed_messages[timestamp] = (full_message_text, dict())
                elif 'thread_ts' in message:
                    # this is within a thread
                    thread_timestamp = float(message['thread_ts'])
                    if thread_timestamp in parsed_messages:
                        # add to the dict for the existing thread
                        parsed_messages[thread_timestamp][1][timestamp] = full_message_text
                    else:
                        # this shouldn't happen
                        warn(f"Can't find thread with timestamp {thread_timestamp} for message with timestamp {timestamp},"
                             " treating as out of thread")
                        parsed_messages[timestamp] = (full_message_text, None)
                else:
                    # this is not associated with a thread at all                                               
                    parsed_messages[timestamp] = (full_message_text, None)
    return parsed_messages


def Output():
    filename = tk.filedialog.askopenfilename()
    parsed_messages = parse_json_slack_export(filename)
    frameBox.insert(tk.END,
                    f"Slackord will post the following {len(parsed_messages)} messages"
                    " (plus thread contents if applicable) to your desired Discord channel:")
    frameBox.yview(tk.END)
    for timestamp in sorted(parsed_messages.keys()):
        (message, thread) = parsed_messages[timestamp]
        frameBox.insert(tk.END, message)
        if thread:
            for timestamp_in_thread in sorted(thread.keys()):
                thread_message = thread[timestamp_in_thread]
                frameBox.insert(tk.END, f"\t{thread_message}")
        frameBox.yview(tk.END)

    # When !slackord is typed in a channel, iterate through the results of previously parsing the
    # JSON file and post each message. Threading is preserved.
    @bot.command(pass_context=True)
    async def slackord(ctx):
        # Note that this function has access to local variables set in Output() above
        # That is, we have access to the previously parsed messages
        #
        # XXX none of the Tk output here is visible
        #     possibly related to bot.run() vs. bot.start() above
        frameBox.insert(tk.END, 'Posting messages into Discord!')
        frameBox.yview(tk.END)
        # pprint(parsed_messages)
        for timestamp in sorted(parsed_messages.keys()):
            (message, thread) = parsed_messages[timestamp]
            sent_message = await ctx.send(message)
            # Output to the GUI that the message was posted.
            frameBox.insert(tk.END, f"Message posted: {timestamp}")
            frameBox.yview(tk.END)
            # XXX add bare print statements for now since GUI output during command execution is broken
            print(f"Message posted: {timestamp}")

            if thread:
                created_thread = await sent_message.create_thread(name=f"thread{timestamp}")
                for timestamp_in_thread in sorted(thread.keys()):
                    thread_message = thread[timestamp_in_thread]
                    await created_thread.send(thread_message)
                    # Output to the GUI that the message in the thread was posted.
                    frameBox.insert(tk.END, f"Message in thread posted: {timestamp_in_thread}")
                    frameBox.yview(tk.END)
                    # XXX add bare print statements for now since GUI output during command execution is broken
                    print(f"Message in thread posted: {timestamp_in_thread}")

        frameBox.insert(tk.END, 'Done posting messages')
        print("Done posting messages")


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
