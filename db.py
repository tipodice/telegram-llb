import json


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.database = self.initialize_database()

    def initialize_database(self):
        # Initialize the database by reading from a JSON file
        try:
            with open(self.db_file, "r") as file:
                return json.load(file)
        except Exception as e:
            return {}

    def save_database(self):
        # Save the database to a JSON file
        with open(self.db_file, "w") as file:
            json.dump(self.database, file)

    def add_or_update_record(self, key, value):
        # Add or update a record in the database
        if value not in self.database.values():
            self.database[key] = value
            self.save_database()
            return True

    def remove_record(self, key):
        # Remove a record from the database
        if key in self.database:
            del self.database[key]
            self.save_database()

    def remove_expired_records(self, current_timestamp):
        # Remove records with expired live periods from the database
        for key, value in list(self.database.items()):
            if (current_timestamp - value["date"]) >= value["live_period"]:
                self.remove_record(key)