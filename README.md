# Space-Rocket-Bot
Repository for a telegram bot created with Python

## Libraries used
### python-telegram-bot
I used this library to create the telegram bot. I chose this instead of Bernard because I couldn’t get the bot to work with Bernard. And because python-telegram-bot it’s also a python library for the Telegram Bot API I thought it was a good replacement.

### python-dotenv
I used this library to load and use environment variables in the code. This way the code will have more security and maintainability. 

### requests

I used this library to make calls to the Frame X API.

## Files

### bisector.py

This file contains all the calls to the Frame X API and all of the bisection process. 

### bot.py

This file contains all the code regarding the telegram bot.

**I decided to separate the bot code and the bisection code to have more abstraction and maintainability. This way one can also differentiate where is the bot interface and handlers, and where is the bisection logic.**

### .env

This file stores all environment variables that are loaded using python-dotenv.

### requirements.txt

This file contains the requirements needed to run the bot. 

## How to install and run the bot

### Create a virtual environment 

It’s recommended to create a virtual environment for the bot so we don’t have any problems with dependencies versions.

### Install libraries and dependencies
Install the libraries and dependencies needed for the bot using pip and the requirements.txt file:

```
$ pip install -r PATH_TO_FILE/requirements.txt
```

### Configure environment variables

Modify environment variables in .env file if needed.

### Run bot

Run the bot using the following command:

```
$ python PATH_TO_FILE/bot.py
```
