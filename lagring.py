# JSON handling and csv exports
#
# Every server is a dict containing:
# "namn": str,
# "adress": str,
# "miljo": ("dev" OR "test" OR "prod"),
# "roll": str,
# "status": ("UP" OR "DOWN" OR default="UNKNOWN"),
# "senast_kontrollerad": str(datetime)
#
# If users imputs invalid "miljo" or "namn" already exists
# the program should prompt the user again.
#
# JSON server file is to be loaded at the start
# and should be updated after every change
#
# INVENTORY_DATAFIL="./servrar.json" keeps track of the
# server file. If the file does not exist the program should
# start with an empty list (I assume we need to create it)
# instead of crashing
#
# CSV exports go to "./rapporter/" with the format:
# "inventering_YYYY-MM-DD_HHmm.csv". The directory
# shall be made if one does not exist. I'm pretty sure
# that the default behaviour is overwrite so lets just keep that.


import json
import os
from datetime import datetime
from pathlib import Path


def get_file():
    """Returns the .json file path and creates it if it
    doesn't exist.
    """
    file_path = Path(os.environ.get("INVENTORY_DATAFIL", "./servrar.json"))

    if not file_path.exists():
        # I assume here that the directories exist
        file_path.write_text("", encoding="utf-8")

    return file_path


def parse_servers_json() -> list:
    """Parses the server .json file as a dict."""
    server_data = []

    file_path = get_file()

    with open(file_path, mode="r", encoding="utf-8") as src:
        server_data = src.read()

    # Returns the json file as a list of key value pairs
    return json.loads(server_data)


def get_current_time():
    """Returns string of the current date and time in
    the right format. Accepts a `datetime` argument, but
    this is mostly for testing purposes.
    """
    current_time = datetime.now()
    # Hard to test, so I did it in ipython
    return current_time.strftime("%d-%m-%Y %H:%M")


def add_server(namn: str, adress: str, miljo: str, roll: str):
    """Adds server to the .json server file.
    Function does not check for input validity."""
    server = {
        "namn": namn,
        "adress": adress,
        "miljo": miljo,
        "roll": roll,
        "status": "Unknown",
        "senast_kontrollerad": "",
    }

    file_path = get_file()

    with open(file_path, mode="w", encoding="utf-8") as target:
        json.dump(server, target)


def get_server(namn, servers: list | None = None) -> dict:
    # Find the server
    # NOTE: I was playing around with
    # server indexes before but it seems
    # that its not necessary
    if servers is None:
        servers = parse_servers_json()

    for server in servers:
        if server.get("namn") == namn:
            return server

    # Raises RuntimeError as this should not be possible
    raise RuntimeError("Unreachable state.")

def update_server_status(namn, status):
    """Updates server status. Function does not check
    for input validity."""
    servers = parse_servers_json()

    target_server = get_server(namn, servers)

    target_server["status"] = status
    target_server["senast_kontrollerad"] = get_current_time()

    with open(file=get_file(), mode="w", encoding="utf-8") as target:
        json.dump(servers, target)
