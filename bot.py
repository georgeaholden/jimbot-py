"""
Slim Jim's Discord Bot

Implements basic features discussed in the README
Think about implementing commands module from discord.ext

Last Edited: 18/5/2021
"""
# Discord and general imports
import os
import discord
import datetime
from discord.ext import commands
from dotenv import load_dotenv

# Imports for the modules I wrote
import sheets
from linkfinder import linkfinder
import harassment
import gifs
import filehandling


class Bot:

    def __init__(self, token, guild):
        self.token = token
        self.guild = guild
        self.client = discord.Client()
        self.response_dict = {}
        self.GIF_PROMPT, self.HELP_TEXT = filehandling.read_commands()
        filehandling.setup_responses(self.response_dict)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)

        creds = sheets.get_creds()
        self.sheet = sheets.connect_to_sheet(creds)
        self.timers = self.setup_timers()


    def setup_timers(self):
        result = {}
        result['gif'] = datetime.datetime.now() - datetime.timedelta(hours=3)
        return result

    # On Startup Basically
    async def on_ready(self):
        print('{} has connected to Discord!'.format(self.client.user))
        found = False
        for guild in self.client.guilds:
            if guild.name == self.guild:
                self.guild = guild
                found = True
                break
        if not found:
            raise ValueError
        print('Connected to {}(id: {})\n'.format(guild.name, guild.id))

    # All Currently Available Commands (rly not a good way of handling it)
    # Case sensitive
    async def on_message(self, message):
        if message.author == self.client.user:  # Prevents the bot from responding to itself (prob no longer useful)
            return

        if message.content.lower().startswith('$hello'):
            await harassment.say_hello(message)
            return

        if message.content.lower().startswith('$flix'):
            title = message.content.lstrip('$flix ')
            await message.channel.send('Attempted to add {} to GibbonFlix Requests Doc'.format(title))
            if sheets.add_request(self.sheet, title, str(message.author)):
                await message.channel.send('Successfully added to the list of requests :)')
            return

        if message.content.lower().startswith('$help'):
            await message.channel.send(self.HELP_TEXT)
            return

        if message.content.lower().startswith('$link'):
            link = linkfinder(message.content.lstrip('$flix '))
            await message.channel.send(link)
            return

        if message.content.lower().startswith('$source'):
            link = linkfinder('source')
            await message.channel.send(link)
            return

        if message.content.lower().startswith('$status'):
            await message.channel.send(
                "I can't really tell, but the MC Server should be up and working\nIf not please dm Jog")
            return

        if message.content.lower().startswith(self.GIF_PROMPT):
            if (datetime.datetime.now() - self.timers['gif']) > datetime.timedelta(hours=3):
                await gifs.post_gif(message.channel, self.guild, self.response_dict['PHRASES'], self.response_dict['GIFS'])
            else:
                await gifs.reject_gif_request(message.channel, self.response_dict['GIFS_UNREADY'])
            return

        if message.content.lower().startswith('$'):
            await message.channel.send('Is that meant to be a command??\nMaybe check $help')
            return

        for thank in ['ty', 'thank', 'arigatou', 'gracias', 'cheers', 'chur', 'merci', 'onya', 'grazie', 'ta', 'shot']:
            if thank in message.content.lower():
                for botname in ['bot', 'jim']:
                    if botname in message.content.lower():
                        await message.channel.last_message.add_reaction('❤️')
                        await message.channel.send("You're welcome bud")
                        return

        # if message.content for new commands


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    guild = os.getenv('DISCORD_GUILD')
    bot = Bot(token, guild)
    bot.client.run(token)


main()
