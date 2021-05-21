"""Another Module that implements a joke feature. Posts gifs when requested or timer completes"""
import random


async def post_gif(channel, guild, responses, gifs, ):
    """Takes a channel and posts a random response and gif. Reacts to the response with a hardcoded emoji.
    Eventually should be refactored to accept an emoji instead of guild"""
    await channel.send(responses[random.randint(0, len(responses) - 1)], tts=True)
    await channel.send(gifs[random.randint(0, len(gifs) - 1)])
    await channel.last_message.add_reaction(await guild.fetch_emoji(831103522229190656))


async def reject_gif_request(channel, too_soon):
    """Takes a target channel, and sends a randomly selected message from too_soon. Should eventually be refactored
    to serve a more general case. e.g. send random message"""
    await channel.send(too_soon[random.randint(0, len(too_soon) - 1)])
