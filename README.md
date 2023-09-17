# telegram-llb
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue.svg)

Script track and manage location updates from users on Telegram. It processes these updates by capturing location data and storing it in a JSON database. Below, you'll find detailed instructions on how to set up and operate this bot.

# Installation
Before you can run the bot, you need to install the required dependencies. To do this, navigate to the project directory and run the following command:
```
pip install -r requirements.txt
```

# Configuration
Open the config.py file in the project directory.
Replace YOUR_BOT_TOKEN_HERE with your Telegram bot token. You can obtain a token by talking to the [BotFather](https://t.me/botfather) on Telegram.
Configure other settings like the database file, update interval, log file, and log level as needed.

# Running the Bot

To run the bot directly using Python 3, execute the following command in your terminal:
```
python3 telegram-llb.py
```
Make sure that you've configured the config.py file with your bot token and other settings as mentioned in the Configuration section.

You can also import the bot into your own. Here's an example of how to do that:

```
import asyncio
from telegram-llb import LocationTracker


BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
DB_FILE = "locations.json"


async def main():
    tracker = LocationTracker(BOT_TOKEN, DB_FILE)

    while True:
        await tracker.fetch_updates()
        await asyncio.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
```

# Usage
Once the Telegram bot is active and running, users can interact with it.
The bot's operation centers on storing real-time location data provided by users who engage with it. This shared live location information is then stored in a JSON database local to the system. You can change database name in `config.py` file.

# Contributing
If you'd like to contribute to this project or report issues, please visit the GitHub repository: [GitHub Repository](https://github.com/tipodice/telegram-llb)
