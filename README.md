# telegram-llb
telegram-llb track and handle location updates from users. It responds to specific commands and stores location data in a simple json database. Below, you'll find instructions on how to set up and run the bot.

# Installation
Before you can run the bot, you need to install the required dependencies. To do this, navigate to the project directory and run the following command:
```
pip install -r requirements.txt
```

# Configuration
Open the config.py file in the project directory.
Replace YOUR_BOT_TOKEN_HERE with your Telegram bot token. You can obtain a token by talking to the BotFather on Telegram.
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
The bot functionality revolves around storing live location data shared by users who interact with it. The shared live location information is saved into a local JSON database. You can easily customize the database name by modifying the config.py file.

# Contributing
If you'd like to contribute to this project or report issues, please visit the GitHub repository: [GitHub Repository](https://github.com/tipodice/telegram-llb)
