"""Another Module that implements a joke feature. Posts gifs when requested or timer completes"""
import random


async def post_gif(channel, guild, responses, gifs, ):
    await channel.send(responses[random.randint(0, len(responses) - 1)], tts=True)
    await channel.send(gifs[random.randint(0, len(gifs) - 1)])
    await channel.last_message.add_reaction(await guild.fetch_emoji(831103522229190656))


async def reject_gif_request(channel, too_soon):
    await channel.send(too_soon[random.randint(0, len(too_soon) - 1)])
