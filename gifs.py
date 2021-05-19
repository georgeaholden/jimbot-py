"""Another Module that implements a joke feature. Posts gifs when requested or timer completes"""
import random
import datetime

RESPONSES = []
GIFS = []
TOO_SOON = []
last = []
last.append(datetime.datetime.now() - datetime.timedelta(hours=3))


def setup():
    populate_list('txts/phrases.txt', RESPONSES)
    populate_list('txts/gifs.txt', GIFS)
    populate_list('txts/unready.txt', TOO_SOON)


def populate_list(filename, target):
    infile = open(filename)
    lines = infile.readlines()
    for line in lines:
        target.append(line.strip())
    infile.close()


async def post_gif(channel, guild):
    if (datetime.datetime.now() - last[0]) > datetime.timedelta(hours=3):
        last[0] = datetime.datetime.now()
        await channel.send(RESPONSES[random.randint(0, len(RESPONSES) - 1)])
        await channel.send(GIFS[random.randint(0, len(GIFS) - 1)])
        await channel.last_message.add_reaction(await guild.fetch_emoji(831103522229190656))
    else:
        await channel.send(TOO_SOON[random.randint(0, len(TOO_SOON) - 1)])


setup()
