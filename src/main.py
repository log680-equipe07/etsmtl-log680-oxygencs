"""Module imports"""

import logging
import json
import time
import os
from signalrcore.hub_connection_builder import HubConnectionBuilder
from dotenv import load_dotenv
import requests
import psycopg2


class App:
    """Class representing the application"""

    load_dotenv()

    def __init__(self):
        self._hub_connection = None
        self._db_connection = None
        self.ticks = 10
        self.config = {
            "host": os.getenv("HOST"),
            "token": os.getenv("TOKEN"),
            "t_max": os.getenv("T_MAX"),
            "t_min": os.getenv("T_MIN"),
            "database_url": os.getenv("DATABASE_URL"),
        }

    def __del__(self):
        if self._hub_connection is not None:
            self._hub_connection.stop()
        if self._db_connection is not None:
            self._db_connection.close()

    def start(self):
        """Start Oxygen CS"""
        self.setup_sensor_hub()
        self._hub_connection.start()
        self.setup_db_connection()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.config['host']}/SensorHub?token={self.config['token']}")
            .configure_logging(logging.INFO)
            .with_automatic_reconnect(
                {
                    "type": "raw",
                    "keep_alive_interval": 10,
                    "reconnect_interval": 5,
                    "max_attempts": 999,
                }
            )
            .build()
        )
        self._hub_connection.on("ReceiveSensorData", self.on_sensor_data_received)
        self._hub_connection.on_open(lambda: print("||| Connection opened."))
        self._hub_connection.on_close(lambda: print("||| Connection closed."))
        self._hub_connection.on_error(
            lambda data: print(f"||| An exception was thrown closed: {data.error}")
        )

    def on_sensor_data_received(self, data):
        """Callback method to handle sensor data on reception."""
        try:
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            action = self.take_action(temperature)
            print(data[0]["date"] + " --> " + data[0]["data"] + ": " + action, flush=True)
            self.save_event_to_database(timestamp, temperature, action)
        except (IndexError, ValueError) as err:
            print(err)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.config["t_max"]):
            self.send_action_to_hvac("TurnOnAc")
            return "TurnOnAc"
        if float(temperature) <= float(self.config["t_min"]):
            self.send_action_to_hvac("TurnOnHeater")
            return "TurnOnHeater"
        return "Aucune Action"

    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(
            f"{self.config['host']}/api/hvac/{self.config['token']}/{action}/{self.ticks}",
            timeout=10,
        )
        details = json.loads(r.text)
        print(details, flush=True)

    def setup_db_connection(self):
        """Setup the database connection."""
        if self._db_connection is None:
            self._db_connection = psycopg2.connect(self.config["database_url"])

    def save_event_to_database(self, timestamp, temperature, action):
        """Save sensor data into database."""
        cur = None
        try:
            if self._db_connection is None:
                raise ValueError("Database connection is not set up.")
            cur = self._db_connection.cursor()
            cur.execute(
                'INSERT INTO "OxygenCS_SensorData" '
                '("timestamp", "temperature", "action") '
                "VALUES (%s, %s, %s)",
                (timestamp, temperature, str(action)),
            )

            self._db_connection.commit()
            print("Data saved successfully")
        except psycopg2.Error as e:
            print(f"Failed to save event to database: {e}")
        finally:
            if cur:
                cur.close()


if __name__ == "__main__":
    app = App()
    app.start()
