#!/usr/bin/env python

# This is originally based on Slackord, by Thomas Loupe
# Enough chaanges led to a hard fork, it is now slack2discord, by Rich Fromm

import asyncio
from datetime import datetime
import discord
from discord.ext import commands
import json
import logging
from pprint import pprint
from sys import argv, exit
import time


logger = logging.getLogger('slack2discord')


# XXX bot needs to be scoped at the top level to use the `@bot.command` annotation
#     so this can *not* move to with start_bot()
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
    # if the message spans multiple lines, output it starting on a separate line from the header
    if message.find('\n') != -1:
        message_sep = '\n'
    else:
        message_sep = ' '

    if real_name:
        return f"`{format_time(timestamp)}` **{real_name}**{message_sep}{message}"
    else:
        return f"`{format_time(timestamp)}{message_sep}{message}"


def start_bot(token):
    # TODO: Thread this process with bot.start().
    # XXX the bot is functional, but the script waits indefinitely after entering the token and doesn't just exit
    #     which is somewhat intentional and the nature of the bot
    #     but maybe a bot isn't the best match for a CLI script to do a single import
    #
    # Normally this sets up logging automatically.
    # But we have already set up logging manually, so disable that here.
    bot.run(token, log_handler=None)


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
                    if thread_timestamp not in parsed_messages:
                        # can't find the root of the thread to which this message belongs
                        # ideally this shouldn't happen
                        # but it could if you have a long enough message history not captured in the exported file
                        logger.warning(f"Can't find thread with timestamp {thread_timestamp} for message with timestamp {timestamp},"
                                       " creating synthetic thread")
                        fake_message_text = format_message(
                            thread_timestamp, None, '_Unable to find start of exported thread_')
                        parsed_messages[thread_timestamp] = (fake_message_text, dict())

                    # add to the dict either for the existing thread
                    # or the fake thread that we created above
                    parsed_messages[thread_timestamp][1][timestamp] = full_message_text
                else:
                    # this is not associated with a thread at all
                    parsed_messages[timestamp] = (full_message_text, None)
    return parsed_messages


def output_messages(parsed_messages, verbose):
    """
    Output the parsed messages to stdout
    """
    verbose_substr = " the following" if verbose else " "
    logger.info(f"Slackord will post{verbose_substr}{len(parsed_messages)} messages"
                " (plus thread contents if applicable) to your desired Discord channel"
                " when you type \'!slackord\' in that channel")
    if not verbose:
        return

    for timestamp in sorted(parsed_messages.keys()):
        (message, thread) = parsed_messages[timestamp]
        logger.info(message)
        if thread:
            for timestamp_in_thread in sorted(thread.keys()):
                thread_message = thread[timestamp_in_thread]
                logger.info(f"\t{thread_message}")


@bot.command(pass_context=True)
async def slackord(ctx):
    """
    When !slackord is typed in a channel, iterate through the results of previously parsing the
    JSON file and post each message. Threading is preserved.
    """
    # XXX somehow this function has access to parsed_messages and verbose, I'm not quite sure how
    logger.info('Posting messages into Discord!')
    if verbose:
        pprint(parsed_messages)
    for timestamp in sorted(parsed_messages.keys()):
        (message, thread) = parsed_messages[timestamp]
        sent_message = await ctx.send(message)
        logger.info(f"Message posted: {timestamp}")

        if thread:
            created_thread = await sent_message.create_thread(name=f"thread{timestamp}")
            for timestamp_in_thread in sorted(thread.keys()):
                thread_message = thread[timestamp_in_thread]
                await created_thread.send(thread_message)
                logger.info(f"Message in thread posted: {timestamp_in_thread}")

    # XXXX at this point the bot will just wait
    # but as a CLI script, that's not really the best model, as we really are done
    # and if we want to do another import, we'd re-run the script
    logger.info("Done posting messages")
    logger.info("Ctrl-C to quit")


if __name__ == '__main__':
    # Normally logging gets set up automatically when discord.Client.run() is called.
    # But we want to use logging before then, with the same config.
    # So set it up manually.
    discord.utils.setup_logging(root=True)

    # XXX eventually do real arg parsing
    if len(argv) != 3:
        print(f"Usage {argv[0]} <token> <filename>")
        exit(1)

    token = argv[1]
    filename = argv[2]
    # XXX this should be an arg, for now just edit here
    verbose = False

    parsed_messages = parse_json_slack_export(filename)
    output_messages(parsed_messages, verbose)

    logger.info("Messages from Slack export successfully parsed.")
    logger.info("Type \'!slackord\' into a Discord channel to import.")
    start_bot(token)

    # XXX we will only get here via Ctrl-C
    #     but we do *not* get a KeyboardInterrupt b/c it is caught by the run() loop in the discord client
    logger.info("Discord import successful.")
    exit(0)
