# Please note: Slackord 2 is out! 
You can get it here: https://github.com/thomasloupe/Slackord2

# Slackord 1.0 by Thomas Loupe

A Discord bot that imports Slack-exported JSON chat history to a Discord channel.
Download the latest executable here: https://github.com/thomasloupe/Slackord/releases/.

Alternatively, you can download the slackord.py script here and run it directly in Python: https://github.com/thomasloupe/Slackord/blob/master/slackord.py.

# Instructions:

1. Export your Slack data as JSON.  Note that only public channels are
   included if you have the Free or Pro version. You need a Business+
   or Enterprise Grid plan to export private channels and direct
   messages (DMs).
   https://slack.com/help/articles/201658943-Export-your-workspace-data
1. Set up Discord bot and create a token here https://discordapp.com/developers/applications/.
1. Clone this repo or download the python file. `git clone `
1. Make sure you've installed Python3 from https://www.python.org/downloads/.
1. Install the Discord python wrapper and Tkinter (if using Tkinter version):

Ubuntu:
```
sudo apt-get install python3-pip
python -m pip install discord.py
sudo apt-get install python-tk
```

Mac:
```
sudo curl https://bootstrap.pypa.io/get-pip.py | python3
pip3 install discord.py
```
or if using Homebrew:
```
brew install python-tk.
```

Windows:
```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip install discord.py
```

5. Run the Slackord executable file, or run Python script by with `python3 slackord.py`, or `py slackord.py`.
6. Click "Import JSON File", browse and select the Slack chat file you wish to import to Discord.
7. Click "Enter Bot Token" and paste your bot's token into the field and press enter.
8. Enter any Discord channel and type !slackord. Messages will now post to that channel.
