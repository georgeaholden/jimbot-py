"""Implementing a joke with the $hello command. If a user types $hello multiple times, the bot adapts its response and
eventually spams the user with friendly dms.

Response filename has following syntax:
a single integer n, the number of unique response lines
n lines each representing a single response
an arbitrary number of threatening messages
EOF"""


user_hello_count = {}
RESPONSES = []
n = 0


def setup_hello(filename):
    """Reads a list of responses from a simple txt file, so that anyone can update or add to the Bot's responses without
    knowledge of Python"""
    infile = open(filename)
    lines = infile.readlines()
    global n
    n = int(lines[0].strip())
    for line in lines[1:]:
        RESPONSES.append(line.strip())
    infile.close()


async def harass_user(user):
    """Spams a user with threatening dms, defined as the lines after n in responses.txt
    Currently just spams all in a row, but should eventually space them out"""
    for response in RESPONSES[n+1:]:
        await user.send(response)


async def say_hello(message):
    counter = user_hello_count.get(message.author, -1) + 1
    user_hello_count[message.author] = counter

    if counter < n:
        await message.channel.send(RESPONSES[counter])
    elif counter == n:
        await message.channel.send(RESPONSES[n])
        await harass_user(message.author)
    else:
        await message.channel.send(RESPONSES[n])


setup_hello('txts/responses.txt')
