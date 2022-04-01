import sqlite3

import config
from os import mkdir, path, remove


def _print(message):
    """Prints a message to the console with the start characters from the config added"""
    print(config.console_msg_startwith + message)


async def setup(db):
    """Performs all the checks and setup requirements as the API starts."""
    passed = True

    # Create data folder if not exists
    if not path.isdir(config.data_folder):
        _print("Data folder not found. Creating. ")
        mkdir(config.data_folder)

    # Create db file and run the setup script if not exists
    if not path.exists(config.sqlite_db_file):
        try:
            with open(config.sql_setup_file, 'r') as file:
                script = file.read()
        except FileNotFoundError:
            _print("ERROR: Setup script not found. The API will not work as intended.")
            remove(config.sqlite_db_file)  # Remove the file so the program will try to create it again next time
            passed = False
        else:
            try:
                await db.execute_script(script)
            except sqlite3.Error:
                _print("ERROR: SQL setup file failed to execute. The API will not work as intended.")
                remove(config.sqlite_db_file)
                passed = False
            else:
                _print("Created DB file and executed setup script.")

    if passed:
        _print("All checks have been passed.")
    return passed