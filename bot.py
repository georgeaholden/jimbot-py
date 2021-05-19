"""
Slim Jim's Discord Bot

Implements basic features discussed in the README
Think about implementing commands module from discord.ext

Last Edited: 18/5/2021
"""
# Discord and general imports
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Imports for the modules I wrote
import sheets
from linkfinder import linkfinder
import harassment
import gifs

infile = open('txts/commands.txt')
lines = infile.readlines()
GIF_PROMPT = lines[0].strip()
HELP_TEXT = ''
for line in lines[1:]:
    HELP_TEXT += line
HELP_TEXT = HELP_TEXT.strip()
infile.close()

# Getting Environment Variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Discord Logic Setup
bot = commands.Bot(command_prefix='$')  # Currently Redundant
client = discord.Client()


# On Startup Basically
@client.event
async def on_ready():
    print('{} has connected to Discord!'.format(client.user))
    global guild
    for gild in client.guilds:
        if gild.name == GUILD:
            guild = gild
            break

    print('{} is connected to the following guild:\n'.format(client.user))
    print('{}(id: {})\n'.format(guild.name, guild.id))

    members = '\n - '.join([member.name for member in guild.members])  # No idea why this was in the quickstart
    print('Guild Members:\n - {}'.format(members))

    creds = sheets.get_creds()
    global sheet # ew, but idk how to pass between these async functions. Maybe try on_ready(sheet) or await?
    sheet = sheets.connect_to_sheet(creds)


# All Currently Available Commands (rly not a good way of handling it)
# Case sensitive
@client.event
async def on_message(message):
    if message.author == client.user:  # Prevents the bot from responding to itself (prob no longer useful)
        return

    if message.content.startswith('$hello'):
        await harassment.say_hello(message)
        return

    if message.content.startswith('$flix'):
        title = message.content.lstrip('$flix ')
        await message.channel.send('Attempted to add {} to GibbonFlix Requests Doc'.format(title))
        if sheets.add_request(sheet, title, str(message.author)):
            await message.channel.send('Successfully added to the list of requests :)')
        return

    if message.content.startswith('$help'):
        await message.channel.send(HELP_TEXT)
        return

    if message.content.startswith('$link'):
        link = linkfinder(message.content.lstrip('$flix '))
        await message.channel.send(link)
        return

    if message.content.startswith('$source'):
        link = linkfinder('source')
        await message.channel.send(link)
        return

    if message.content.startswith('$status'):
        await message.channel.send("I can't really tell, but the MC Server should be up and working\nIf not please dm Jog")
        return

    if message.content.startswith(GIF_PROMPT):
        await gifs.post_gif(message.channel, guild)
        return

    if message.content.startswith('$'):
        await message.channel.send('Is that meant to be a command??\nMaybe check $help')
        return

    # if message.content for new commands


# Gets All the discord shit running ig, like a call to main()
client.run(TOKEN)
