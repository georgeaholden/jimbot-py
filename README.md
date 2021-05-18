# jimBot
Source Code for jimBot, a Python based discord bot

Simple desktop application, will eventually
be deployed to Google Cloud Platform. (Probably on same VM as the MC Server)

Current Functionality:
 - Reads user messages tagged with $ as commands (should eventually use new built in Discord /commands)
 - Links a few useful URLs when given appropriate prompts
 - Updates Blackmore's Google Request Sheet based on user input using Sheets API
 
TODO:
 - Further improve on Sheet update logic by handling deletions, 
   dynamically checking range, 
   deleting old entries 
   and sending requests to OMDB API to verify input
 - Improve Security a touch, maybe add links to .env
 - Deploy on Google Cloud Platform
 - Implement MC Server Commands (Rollback? Reset? etc)


### -- George Holden 
#### 18/5/2021
