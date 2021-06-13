"""
Slim Jim's Discord Bot

Implements basic features discussed in the README
Think about implementing commands module from discord.ext

Last Edited: 9/6/2021
"""
# Discord and general imports
import os
import configparser
from dotenv import load_dotenv
from bot import Bot


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    guild = os.getenv('DISCORD_GUILD')
    config = configparser.ConfigParser()
    config.read("config.ini")
    bot = Bot(token, guild, config)
    bot.client.run(token)


main()
print('done')
