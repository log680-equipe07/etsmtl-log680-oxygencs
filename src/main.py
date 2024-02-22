from signalrcore.hub_connection_builder import HubConnectionBuilder
from dotenv import load_dotenv
import logging
import requests
import json
import time
import psycopg2
import os

class App:
    
    load_dotenv()
    
    def __init__(self):
        self._hub_connection = None
        self.TICKS = 10

        # To be configured by your team
        self.HOST = os.getenv('HOST')  # Setup your host here
        self.TOKEN = os.getenv('TOKEN')  # Setup your token here
        self.T_MAX = os.getenv('T_MAX')  # Setup your max temperature here
        self.T_MIN = os.getenv('T_MIN')  # Setup your min temperature here
        self.DATABASE_URL = os.getenv('DATABASE_URL')  # Setup your database here

    def __del__(self):
        if self._hub_connection != None:
            self._hub_connection.stop()

    def start(self):
        """Start Oxygen CS."""
        self.setup_sensor_hub()
        self._hub_connection.start()
        print("Press CTRL+C to exit.")
        while True:
            time.sleep(2)

    def setup_sensor_hub(self):
        """Configure hub connection and subscribe to sensor data events."""
        self._hub_connection = (
            HubConnectionBuilder()
            .with_url(f"{self.HOST}/SensorHub?token={self.TOKEN}")
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
            print(data[0]["date"] + " --> " + data[0]["data"], flush=True)
            timestamp = data[0]["date"]
            temperature = float(data[0]["data"])
            action = self.take_action(temperature)
            self.save_event_to_database(timestamp, temperature, action)
        except Exception as err:
            print(err)

    def take_action(self, temperature):
        """Take action to HVAC depending on current temperature."""
        if float(temperature) >= float(self.T_MAX):
            self.send_action_to_hvac("TurnOnAc")
            return 'TurnOnAc'
        elif float(temperature) <= float(self.T_MIN):
            self.send_action_to_hvac("TurnOnHeater")
            return 'TurnOnHeater'
            
    def send_action_to_hvac(self, action):
        """Send action query to the HVAC service."""
        r = requests.get(f"{self.HOST}/api/hvac/{self.TOKEN}/{action}/{self.TICKS}")
        details = json.loads(r.text)
        print(details, flush=True)

    def save_event_to_database(self, timestamp, temperature, action):
        """Save sensor data into database."""
        try:                        
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cur = conn.cursor()
            
            cur.execute('INSERT INTO "OxygenCS_SensorData" ("timestamp", "temperature", "action") VALUES (%s, %s, %s)', (timestamp, temperature, str(action)))
            conn.commit()
            
            print("Data saved successfully")
        except psycopg2.Error as e:
            print(f"Failed to save event to database: {e}")
        finally:
            if cur:
                cur.close()
            if conn:
                conn.close()

if __name__ == "__main__":
    app = App()
    app.start()
