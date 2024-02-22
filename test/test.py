## To Implement
## python -m unittest test.test to run the tests

import unittest
from unittest.mock import patch, MagicMock
from src.main import App

class TestApp(unittest.TestCase):
        
    '''
    This tests checks the take_action method when the temperature is above the T_MAX
    
    It validates that the print message has the right content.
    It validates that the return action is 'TurnOnAC'
    '''
    @patch('src.main.requests.get')
    @patch('src.main.print')
    def test_take_action_turn_on_ac(self, mocked_print, mocked_requests_get):
        mocked_requests_get.return_value.text = '{"Response": "Activating AC for 10 ticks"}'
        app = App()
        action = app.take_action(float(app.T_MAX) + 1)
        self.assertEqual(action, 'TurnOnAc')
        mocked_print.assert_called_with({'Response': 'Activating AC for 10 ticks'}, flush=True)

    '''
    This tests checks the take_action method when the temperature is below the T_MIN
    
    It validates that the print message has the right content.
    It validates that the return action is 'TurnOnHeater'
    '''
    @patch('src.main.requests.get')
    @patch('src.main.print')
    def test_take_action_turn_on_heater(self, mocked_print, mocked_requests_get):
        mocked_requests_get.return_value.text = '{"Response": "Activating Heater for 10 ticks"}'
        app = App()
        action = app.take_action(float(app.T_MIN) - 1)
        self.assertEqual(action, 'TurnOnHeater')
        mocked_print.assert_called_with({'Response': 'Activating Heater for 10 ticks'}, flush=True)


    '''
    This tests checks the save_event_to_database method
    
    It validates that the print message has the right content ("Data saved successfully").
    It also validates that the connection to the database was successful
    '''    
    @patch('src.main.psycopg2.connect')
    @patch('src.main.print')
    def test_save_event_to_database(self, mocked_print, mock_connect):
        # Mock the cursor and its execute method
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        # Create an instance of App
        app = App()

        # Call save_event_to_database
        app.save_event_to_database('2024-02-22T08:00:00', 20.0, 'TurnOnHeater')

        # Assert that cursor.execute was called with the expected query and values
        mock_cursor.execute.assert_called_once_with('INSERT INTO "OxygenCS_SensorData" ("timestamp", "temperature", "action") VALUES (%s, %s, %s)', ('2024-02-22T08:00:00', 20.0, 'TurnOnHeater'))

        # Assert that conn.commit was called
        mock_connect.return_value.commit.assert_called_once()
        mocked_print.assert_called_with("Data saved successfully")


if __name__ == '__main__':
    unittest.main()
