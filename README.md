# jimBot
### 0.1.1
Source Code for jimBot, a Python based discord bot

Simple desktop application, currently deployed to a virtual machine on the Google
Cloud Platform.

Current Functionality:
 - Reads user messages tagged with $ as commands (should eventually use new built in Discord /commands)
 - Links a few useful URLs when given appropriate prompts
 - Updates Blackmore's Google Request Sheet based on user input using Sheets API
 - Posts randomised gifs with a randomised phrase, given a cooldown timer.
 - Supports thanking

TODO:
 - Implement "bandwagoning", where the bot adds a reaction if enough people
 react to a given message
 - Further improve on Sheet update logic by handling deletions,
   dynamically checking range,
   deleting old entries
   and sending requests to OMDB API to verify input
 - Improve Security a touch, maybe add links to .env
 - Implement MC Server Commands (Rollback? Reset? etc)
 - Implement periodic gif posting
 - Improve code style, extrapolate all check strings to .txts


Long Term:
 - Music bot?
 - Reverse image search and contribute to random discussions in #general



### -- George Holden
#### 18/5/2021
