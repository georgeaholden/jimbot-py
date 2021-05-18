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

HELP_TEXT = """I'm a WIP
Current Commands: 
$help - Shows this text
$flix - Adds to Blackmore's Gibbonflix request doc
$hello - Please stop
$link - Ill link anything I know about (type $link help for info)"""


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
    for guild in client.guilds:
        if guild.name == GUILD:
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
        await message.channel.send('Hello!')

    if message.content.startswith('$flix'):
        title = message.content.lstrip('$flix ')
        await message.channel.send('Attempted to add {} to GibbonFlix Requests Doc'.format(title))
        if sheets.add_request(sheet, title, str(message.author)):
            await message.channel.send('Successfully added to the list of requests :)')

    if message.content.startswith('$help'):
        await message.channel.send(HELP_TEXT)

    if message.content.startswith('$link'):
        link = linkfinder(message.content.lstrip('$flix '))
        await message.channel.send(link)

    # if message.content for new commands


# Gets All the discord shit running ig, like a call to main()
client.run(TOKEN)
