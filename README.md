# jimBot
### 0.1.5
Source Code for jimBot, a Python based discord bot

Simple desktop application, currently deployed to a virtual machine on the Google
Cloud Platform.

Current Functionality:
 - Reads user messages tagged with $ as commands (should eventually use new built in Discord /commands)
 - Links a few useful URLs when given appropriate prompts
 - Updates Blackmore's Google Request Sheet based on user input using Sheets API
 - Posts randomised gifs with a randomised phrase, given a cooldown timer.
 - Supports thanking
 - Joins in on reacting to a message with emojis, given enough responses

TODO:
 - Refactor hard coded elements out of modules and into .env or similar.
 - Find a better way to handle the version variable
 - Further improve on Sheet update logic by handling deletions,
   dynamically checking range,
   deleting old entries
   and sending requests to OMDB API to verify input
 - Improve Security a touch, maybe add links to .env
 - Implement MC Server Commands (Rollback? Reset? etc)
 - Implement periodic gif posting
 - Prevent users from sending some basic commands in #general. 
   e.g. delete request, post an explanation redirecting them, delete
   explanation after enough time (callback function)


Long Term:
 - Music bot?
 - Reverse image search and contribute to random discussions in #general
 - Improve gif and response messages by detecting time, weather holiday etc


### -- George Holden
#### 18/5/2021