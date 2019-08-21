# Slackord
A Discord bot that moves Slack-exported JSON chat history to Discord channels.

Please download the 0.5 release from https://github.com/thomasloupe/Slackord/releases/tag/0.5
The 1.0 release is in alpha and may be broken.

Instructions:

# Step 1:
Install Python 3.7: https://www.python.org/downloads/release/python-373/

# Step 2:
Install pip.

"python get-pip.py"
or
"py get-pip.py"

# Step 3:
Open a terminal or command prompt and use the appropriate command per your OS to install discord.py.

Linux/OS X
"python3 -m pip install -U discord.py"

Windows
"py -3 -m pip install -U discord.py"

# Step 4:
Set up a Discord bot with the permissions of "bot", and "Administrator", or 
"bot" and give the bot "Read" + "Write" message privileges here: https://discordapp.com/developers/applications/.

# Step 5:
Generate a secret token for the bot. Copy it to clipboard.

# Step 6:
Insert the bot's token into the "bot.run(TOKEN)" field.

# Step 7:
Change the location/name of the json file where "test.json" is on the line with "with open('test.json') as json_file:"

# Step 8:
Invite the bot to your Discord server.

# Step 9:
Open console and run:

"py slackord.py"
or
"python slackord.py"

The bot will now parse all the messages from your Slack message json file.

# Step 10:
Enter the channel you wish to import messages to and type "!mergeslack"

Messages should now start appearing in the Discord channel you typed the command into.
