"""
Slim Jim's Discord Bot

Implements basic features discussed in the README
Think about implementing commands module from discord.ext

Last Edited: 21/5/2021
"""
# Discord and general imports
import os
import discord
from dotenv import load_dotenv

# Imports for the modules I wrote
from modules import filehandling, gifs, harassment, sheets, timercontroller, linkfinder


class Bot:

    def __init__(self, token, guild):
        # Discord Related setup
        self.token = token
        self.guild = guild
        self.client = discord.Client()
        self.general = None

        # Binds class methods to events (Could maybe be done with iteration?)
        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.event(self.on_raw_reaction_add)

        # Setup for modules I wrote
        self.strings_dict = {}
        self.GIF_PROMPT, self.HELP_TEXT = filehandling.read_commands()
        self.version = filehandling.read_config(self.strings_dict)
        self.t_controller = timercontroller.TimerController()
        self.t_controller.add_timer('gifs', 3)

        # Setup for Google Sheets
        creds = sheets.get_creds()
        self.sheet = sheets.connect_to_sheet(creds)

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
        print('Connected to {}(id: {})\n'.format(guild.name, guild.id))
        print(self.guild.name)
        self.general = self.guild.get_channel(int(os.getenv('GENERAL')))
        if not sheets.changelog_printed(self.sheet, self.version):
            await self.post_changelog()

    # All Currently Available Commands (rly not a good way of handling it)
    async def on_message(self, message):
        if message.author == self.client.user:  # Prevents the bot from responding to itself (prob no longer useful)
            return

        if message.author.name == 'Jog' and message.content.lower().startswith('$kill'):
            await message.channel.send('I don\'t feel so good :(')
            await self.client.close()

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
            link = linkfinder.find_link(message.content.lstrip('$flix '))
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

        if message.content.lower().startswith(self.GIF_PROMPT):
            if self.t_controller.time_has_elapsed('gifs', hours=3):
                await gifs.post_gif(message.channel, self.guild, self.strings_dict['GIFS_PHRASES'], self.strings_dict['GIFS'])
                self.t_controller.reset_timer('gifs')
            else:
                await gifs.reject_gif_request(message.channel, self.strings_dict['GIFS_UNREADY'])
            return

        if message.content.lower().startswith('$'):
            if not message.content[1].isnumeric():
                await message.channel.send('Is that meant to be a command??\nMaybe check $help')
                return

        for botname in ['bot', 'jim']:
            if botname in message.content.lower():
                for thank in self.strings_dict['THANKS']:
                    if thank in message.content.lower():
                        await message.channel.last_message.add_reaction('❤️')
                        await message.channel.send("You're welcome bud")
                        return
        # if message.content for new commands

    # Triggers whenever a message is reacted to
    async def on_raw_reaction_add(self, payload):
        channel = self.guild.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        for reaction in message.reactions:
            if reaction == payload.emoji:
                break

        if reaction.count > 2:  # Should be set in config or something
            await message.add_reaction(reaction)

    async def post_changelog(self):
        await self.general.send(filehandling.get_contents('changelog.txt'))


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    guild = os.getenv('DISCORD_GUILD')
    bot = Bot(token, guild)
    bot.client.run(token)


main()
print('done')