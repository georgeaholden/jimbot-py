"""
Slim Jim's Discord Bot

Implements basic features discussed in the README
Think about implementing commands module from discord.ext

Last Edited: 13/06/2021
"""
# Discord and general imports
import asyncio
import os
import re

import discord
EMAIL_REGEX = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

HELP = """I currently know about:
slimjimsthings.com
The Slim Jim Wiki
The Game & Movie sheets
The MC Server IP Address
My Source Code"""

# Imports for the modules I wrote
from modules import filehandling, gifs, harassment, sheets, timercontroller, linkfinder


class Bot:

    def __init__(self, token, guild, config):
        self.version = config['DEV']['version']
        self.ticket = 0

        # Discord Related setup
        self.token = token
        self.guild = guild
        self.client = discord.Client()
        self.general = None
        self.config = config
        self.waitlist = {}
        self.admins = []

        # Binds class methods to events (Could maybe be done with iteration?)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.event(self.on_raw_reaction_add)

        # Setup for Google Sheets
        self.sheet_handler = sheets.SheetHandler()

        # Setup for modules I wrote
        self.GIF_PROMPT = self.sheet_handler.get_value('DB', 'gif_prompt')
        self.HELP_TEXT = self.sheet_handler.get_value('DB', 'help_text')
        self.strings_dict = dict(config['STRINGS'])
        for key, filename in self.strings_dict.items():
            self.strings_dict[key] = filehandling.get_contents_as_list(filename)
        self.t_controller = timercontroller.TimerController()
        self.t_controller.add_timer('gifs', hours=3)



    # On Connection to the Discord server
    async def on_ready(self):
        print('{} has connected to Discord!'.format(self.client.user))
        found = False
        for guild in self.client.guilds:
            if guild.name == self.guild:
                self.guild = guild
                found = True
                break
        if not found:
            raise RuntimeError
        print('Connected to {}(id: {})\n'.format(self.guild.name, self.guild.id))
        print(self.guild.name)
        self.general = self.guild.get_channel(int(os.getenv('GENERAL')))
        if not sheets.changelog_printed(self.sheet, self.version):
            await self.post_changelog()

        admins = self.config['ADMINS']
        for admin in admins.items():
            admin_id = admin[1]
            user = await self.client.fetch_user(admin_id)
            self.admins.append(user)
        print('Finished Setup')

    # All Currently Available Commands (rly not a good way of handling it)
    async def on_message(self, message):
        if message.author == self.client.user:  # Prevents the bot from responding to itself (prob no longer useful)
            return

        # Global Commands
        if message.author.name == 'Jog' and message.content.lower().startswith('$kill'):
            await message.channel.send('I don\'t feel so good :(')
            await self.client.close()
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
            if 'dm' in message.content.lower():
                if isinstance(message.channel, discord.channel.DMChannel):
                    await message.channel.send('dm channels are a safe space for you and me to talk privately'
                                               + '\nThe requests you make in a dm channel are NOT logged, unless they directly trigger an action which')
                    return
            if 'link' in message.content.lower():
                await message.channel.send(HELP)
                return
            await message.channel.send(self.HELP_TEXT)
            return

        if message.content.lower().startswith('$link'):
            link = linkfinder.find_link(message.content.lstrip('$link '))
            await message.channel.send(link)
            return

        if message.content.lower().startswith('$source'):
            link = linkfinder.find_link('source')
            await message.channel.send(link)
            return

        if message.content.lower().startswith('$status'):
            await message.channel.send(
                "I can't really tell, but the MC Server should be up and working\nIf not please dm Jog")
            return

        # #general only
        if message.content.lower().startswith(self.GIF_PROMPT):
            if not isinstance(message.channel, discord.channel.TextChannel):
                await message.channel.send('Cmon man surely in a group channel')
                return
            if self.t_controller.time_has_elapsed('gifs', hours=3):
                self.t_controller.reset_timer('gifs')
                await gifs.post_gif(message.channel, self.guild, self.strings_dict['gifs_phrases'],
                                    self.strings_dict['gifs'])
            else:
                await gifs.reject_gif_request(message.channel, self.strings_dict['gifs_unready'])
            return

        if message.content.lower().startswith('$req'):
            if not isinstance(message.channel, discord.channel.DMChannel):  # TODO: Maybe extract into is_dm(channel)?
                await message.channel.send('Send me reqs in dms instead')
                return
            if 'wiki' in message.content.lower():
                await message.channel.send('Sure, I can add you to the Wiki\nWhat\'s your email address?')
                self.ticket += 1
                counter = self.ticket
                self.waitlist[message.author] = ('wiki', counter)
                await asyncio.sleep(60 * 5)
                if self.waitlist.get(message.author, (0, 0))[1] == counter:
                    self.waitlist.pop(message.author)
                return

        if message.content.lower().startswith('$bug'):
            for admin in self.admins:
                await admin.send('Bug Report from {}\n{}'.format(message.author, message.content.lstrip('$bug')))
            await message.channel.send('Report sent, thank you!')
            return

        if message.content.lower().startswith('$'):
            if not message.content[1].isnumeric():
                await message.channel.send('Is that meant to be a command??\nMaybe check $help')
                return

        if isinstance(message.channel, discord.channel.DMChannel):  # TODO: Extract checking to ticket.is_ticket()
            if message.author in self.waitlist:
                ticket = self.waitlist[message.author]
                if ticket[0] == 'wiki': # TODO: Extract into ticket.resolve(string)
                    if re.search(EMAIL_REGEX, message.content):
                        for admin in self.admins:
                            await admin.send('Can you add {} to the Wiki? Their email is: {}'
                                             .format(message.author.name, message.content))
                        await message.channel.send('Sent a DM to the admins for you :)')
                        self.waitlist.pop(message.author)
                    else:
                        await message.channel.send("That doesn't look like a valid email address, try again?")
                return

        if self.is_thanks(message):
            await message.add_reaction('❤️')
            await message.channel.send("You're welcome bud")
            return
        # if message.content for new commands

    # Triggers whenever a message is reacted to
    async def on_raw_reaction_add(self, payload):  # TODO: Fix in dm channels
        channel = self.guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        for reaction in message.reactions:
            if reaction == payload.emoji:
                break

        if reaction.count > 1:  # Should be set in config or something
            await message.add_reaction(reaction)

    async def post_changelog(self):
        await self.general.send(filehandling.get_contents('changelog.txt'))

    def is_thanks(self, message):
        for thank in self.strings_dict['thanks']:
            if thank in message.content.lower():
                if isinstance(message.channel, discord.channel.DMChannel):
                    return True
                else:
                    for bot_name in ['bot', 'jim']:
                        if bot_name in message.content.lower():
                            return True
        return False
