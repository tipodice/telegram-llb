import asyncio
import aiohttp
import base64
import time
import logging
from db import Database
from config import *


# Configure logging with rotating logs and improved formatting
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()],
)


class LocationTracker:
    def __init__(self, bot_token, db_file):
        self.bot_token = bot_token
        self.db = Database(db_file)
        self.session = aiohttp.ClientSession()
        self.update_id = None

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
                    logging.error("Error in response check for invalid TOKEN: %s", data)
        except Exception as e:
            logging.error("Error fetching updates: %s", e)

    async def handle_updates(self, updates):
        # Handle incoming updates
        if not updates:
            current_timestamp = int(time.time())
            self.db.remove_expired_records(current_timestamp)
            return

        if not self.update_id:
            self.update_id = updates[-1].get("update_id")
        self.update_id += 1

        for update in updates:
            msg = update.get("message") or update.get("edited_message")
            if not msg:
                continue

            chat_id = msg.get("chat").get("id")

            if msg.get("location"):
                try:
                    date = msg.get("date")
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
                                "live_period": live_period,
                            }
                            if self.db.add_or_update_record(str(chat_id), loc):
                                logging.info(
                                    "Record with latitude: %s longitude: %s added to DB",
                                    lat,
                                    lng,
                                )
                    if not live_period:
                        self.db.remove_record(str(chat_id))
                        logging.info(
                            "Live Location was deactivated by user, chat_id %s record was removed from DB",
                            chat_id,
                        )

                except Exception as e:
                    logging.error("Error processing update: %s", e)


async def main():
    tracker = LocationTracker(BOT_TOKEN, DB_FILE)

    while True:
        await tracker.fetch_updates()
        await asyncio.sleep(UPDATE_INTERVAL)


if __name__ == "__main__":
    asyncio.run(main())
