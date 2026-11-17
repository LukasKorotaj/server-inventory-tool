# JSON handling and csv exports
#
# Every server is a dict containing:
# "namn": str,
# "adress": str,
# "miljo": ("dev" OR "test" OR "prod"),
# "roll": str,
# "status": ("up" OR "down" OR default="unknown"),
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


import csv
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
        file_path.write_text("[]", encoding="utf-8")

    return file_path


def parse_servers_json() -> list:
    """Parses the server .json file as a dict."""
    server_data = []

    file_path = get_file()

    with open(file_path, mode="r", encoding="utf-8") as src:
        server_data = src.read()

    # Returns the json file as a list of key value pairs
    return json.loads(server_data)


def get_current_time(csv_format: bool = False):
    """Returns string of the current date and time
    formatted for the json server file (default) or csv export.
    """
    current_time = datetime.now()
    # Hard to test, so I did it in ipython
    if csv_format:
        return current_time.strftime("%Y-%m-%d_%H%M")
    else:
        return current_time.strftime("%Y-%m-%d %H:%M")


def add_server(namn: str, adress: str, miljo: str, roll: str):
    """Adds server to the .json server file.
    Function does not check for input validity."""
    servers = parse_servers_json()

    server = {
        "namn": namn,
        "adress": adress,
        "miljo": miljo,
        "roll": roll,
        "status": "unknown",
        "senast_kontrollerad": "",
    }

    servers.append(server)

    file_path = get_file()

    with open(file_path, mode="w", encoding="utf-8") as target:
        json.dump(servers, target)


def get_server(namn, servers: list | None = None) -> dict | None:
    # Find the server
    # NOTE: I was playing around with
    # server indexes before but it seems
    # that its not necessary
    if servers is None:
        servers = parse_servers_json()

    for server in servers:
        if server.get("namn") == namn:
            return server

    return None


def update_server_status(namn, status):
    """Updates server status. Function does not check
    for input validity."""
    servers = parse_servers_json()

    target_server = get_server(namn, servers)
    if target_server is None:
        raise ValueError(f"Servern {namn} finns inte")

    target_server["status"] = status
    target_server["senast_kontrollerad"] = get_current_time()

    with open(file=get_file(), mode="w", encoding="utf-8") as target:
        json.dump(servers, target)


def export_csv():
    servers = parse_servers_json()
    file_name = f"inventering_{get_current_time(csv_format=True)}.csv"

    # Mkdir only makes the dir if it does not exist and does nothing if
    # it does.
    try:
        Path("./rapporter").mkdir(exist_ok=True)
    except FileExistsError:
        print(
            "Rapporter exists as a file. This is not allowed. Move or delete the file."
        )
        return 2

    with open(f"./rapporter/{file_name}", mode="w", encoding="utf-8") as target:
        writer = csv.DictWriter(
            target,
            fieldnames=[
                "namn",
                "adress",
                "miljo",
                "roll",
                "status",
                "senast_kontrollerad",
            ],
        )
        writer.writeheader()
        writer.writerows(servers)

    print("\n\n\n")
    print(f"Rapporten finns i ./rapporter/{file_name}")

    return 0

def txt_summary(servers: list | None = None):
    """Makes a string that can be exported alongside csv file. (Or by itself)"""

    if servers is None:
        servers = parse_servers_json()

    str_list = []
    af = lambda s: str_list.append(s + "\n")

    af(f"{'MILJO':<8}{'UP':<8}{'DOWN':<8}{'UNKNOWN':<8}")
    af(32 * "-")

    dev = {"up": 0, "down": 0, "unknown": 0}
    test = {"up": 0, "down": 0, "unknown": 0}
    prod = {"up": 0, "down": 0, "unknown": 0}

    for s in servers:
        target = {}
        match s["miljo"]:
            case "test":
                target = test
            case "dev":
                target = dev
            case "prod":
                target = prod
            case what:
                raise RuntimeError(f"Server has illegal miljo: {what}")

        match s["status"]:
            case "up":
                target["up"] += 1
            case "down":
                target["down"] += 1
            case "unknown":
                target["unknown"] += 1
            case what:
                raise RuntimeError(f"Server has illegal status: {what}")

    af(f"{'dev':<8}{dev['up']:<8}{dev['down']:<8}{dev['unknown']:<8}")
    af(f"{'test':<8}{test['up']:<8}{test['down']:<8}{test['unknown']:<8}")
    af(f"{'prod':<8}{prod['up']:<8}{prod['down']:<8}{prod['unknown']:<8}")


    af(32 * "-")

    total = {"up": 0, "down": 0, "unknown": 0}
    for k in (dev, test, prod):
        total["up"] += k["up"]
        total["down"] += k["down"]
        total["unknown"] += k["unknown"]

    af(f"{'TOTAL':<8}{total['up']:<8}{total['down']:<8}{total['unknown']:<8}")

    final_string = "".join(str_list)

    return final_string



def remove_server(to_del):
    servers = parse_servers_json()
    server_to_del = get_server(to_del)

    servers.remove(server_to_del)

    with open(file=get_file(), mode="w", encoding="utf-8") as target:
        json.dump(servers, target)
