""" Super basic module I wrote in like 10 mins to link various URLs to a user
The way that queries are matched to the appropriate URL is super ugly, I wonder if there's a package I could use instead?
Currently just checks if any commonly used phrases are contained in the input.
"""

SHOP = ['shop', 'store', 'things']
MC = ['mine', 'craft', 'mc']
CODE = ['source', 'code', 'git']

HELP = """I currently know about:
slimjimsthings.com
The jims movie sheet
The jimDev Doc
The jims game sheet
The MC Server IP Address
My Source Code"""


def find_link(query):
    """Finds and returns str links based on str query"""
    query = query.strip().lower()
    if 'help' in query:
        return HELP
    for phrase in SHOP:
        if phrase in query:
            return "https://slimjimsthings.com/"
    if 'movie' in query:
        return "https://docs.google.com/document/d/1fKXEQ2yVU_y_A9jowsXQH0r8pQ4zREiu-Rj7hRCqNQw/edit?usp=sharing"
    if 'dev' in query:
        return "https://docs.google.com/document/d/1d-6VmkRiD2zlFNqHNVP43PP9EQ9KVP8zwdfOeTiN4Lo/edit?usp=sharing"
    if 'game' in query:
        return "https://docs.google.com/spreadsheets/d/12ILuG2T99PL1-gjGyGUCf1GMb7N-uvG66wf5OGYv4mM/edit?usp=sharing"
    for phrase in MC:
        if phrase in query:
            return 'The Current MC Server is Running on a NEW IP Address: 34.151.89.121'
    for phrase in CODE:
        if phrase in query:
            return 'My Source Code is publicly available at: https://github.com/georgeaholden/jimBot'
    return "I'm not quite sure what you mean...\nMaybe look at $link help?"
