"""Another Module that implements a joke feature. Posts gifs when requested or timer completes"""
import random


async def post_gif(channel, guild, RESPONSES, GIFS, ):
    await channel.send(RESPONSES[random.randint(0, len(RESPONSES) - 1)])
    await channel.send(GIFS[random.randint(0, len(GIFS) - 1)])
    await channel.last_message.add_reaction(await guild.fetch_emoji(831103522229190656))


async def reject_gif_request(channel, TOO_SOON):
    await channel.send(TOO_SOON[random.randint(0, len(TOO_SOON) - 1)])
