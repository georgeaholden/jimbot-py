SHOP = ['shop', 'store', 'things']
MC = ['mine', 'craft', 'mc']
HELP = """I currently know about:
slimjimsthings.com
The jims movie sheet
The jimDev Doc
The jims game sheet
The MC Server Address"""
def linkfinder(query):
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
            return 'The Current MC Server is Running on: 34.71.253.85'