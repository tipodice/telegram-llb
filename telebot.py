import asyncio
import aiohttp
import base64
import time
import json
import logging

from db import Database
from config import BOT_TOKEN, DB_FILE, UPDATE_INTERVAL, LOG_FILE, LOG_LEVEL


# Configure logging with rotating logs and improved formatting
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)


class LocationTracker:
    def __init__(self, bot_token, db_file):
        self.bot_token = bot_token
        self.db = Database(db_file)
        self.session = aiohttp.ClientSession()
        self.update_id = None

    async def generate_b64_token(self, chat_id):
        # Generate a base64-encoded token using the chat_id
        token = base64.b64encode(chat_id.encode()).decode()
        return token
    
    async def fetch_updates(self):
        # Fetch updates from the Telegram API
        offset = f"?offset={self.update_id}" if self.update_id else ""
        url = f"https://api.telegram.org/bot{self.bot_token}/getUpdates{offset}"

        try:
            async with self.session.get(url) as response:
                data = await response.json()
                if data.get("ok"):
                    await self.handle_updates(data.get("result"))
                else:
                    logging.error("Error in response: %s", data)
        except Exception as e:
            logging.error("Error fetching updates: %s", e)

    async def send_message(self, chat_id, text):
        # Send a message to a specific chat using the bot API
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text,
        }

        try:
            async with self.session.get(url, params=params) as response:
                data = await response.json()
                if data.get("ok"):
                    logging.info("Message sent successfully.")
                else:
                    logging.error("Failed to send message: %s", data)
        except Exception as e:
            logging.error("Error sending message: %s", e)

    async def handle_updates(self, updates):
        # Handle incoming updates
        if not updates:
            current_timestamp = int(time.time())
            self.db.remove_expired_records(current_timestamp)
            return

        if not self.update_id:
            self.update_id = updates[-1]["update_id"]
        self.update_id += 1

        for update in updates:
            msg = update.get("message") or update.get("edited_message")
            if not msg:
                continue

            chat_id = msg["chat"]["id"]
            
            try:
                user_message = msg.get("text")
                if user_message:
                    if user_message == "/api":
                        if str(chat_id) in self.db.database:
                            generate_token = await self.generate_b64_token(str(chat_id))
                            await self.send_message(
                                chat_id, f"http://site.com/api/{generate_token}"
                            )
                    else:
                        logging.info(
                            "Message was not sent because the command doesn't exists"
                        )
            except Exception as e:
                logging.error("Error sending message: %s", e)

            if msg.get("location"):
                try:
                    date = msg["date"]
                    edit_date = int(time.time())
                    location = msg.get("location")
                    lat = location.get("latitude")
                    lng = location.get("longitude")
                    live_period = location.get("live_period")
                    if live_period:
                        if (edit_date - date) <= live_period:
                            loc = {
                                "lat": lat,
                                "lng": lng,
                                "date": date,
                                "live_period": live_period
                            }
                            if self.db.add_or_update_record(str(chat_id), loc):
                                logging.info(
                                    "Record with latitude: %s longitude: %s added to DB", lat, lng
                                )
                    if not live_period:
                        self.db.remove_record(str(chat_id)) 
                        logging.info(
                                "Live Location was deactivated by user, chat_id %s record was removed from DB", chat_id)
                        
                except Exception as e:
                    logging.error("Error processing update: %s", e)


async def main():
    tracker = LocationTracker(BOT_TOKEN, DB_FILE)

    while True:
        await tracker.fetch_updates()
        await asyncio.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
