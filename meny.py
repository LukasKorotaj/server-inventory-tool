# Should only handle the meny and its functions
#
# When the program is started it should show a menu.
# Menu entries should (at least) have this:
# * Visa alla
# * Visa miljo
# * Lagg till
# * Ta bort
# * Kontrollera en
# * Kontrollera alla
# * Exportera som CSV
# * Avsluta
#
# The program should handle wrong inputs without crashing.
# "Ta bort" action should ask for confirmation.
# When printing all servers the output should look something like this (:<15):
#
# Namn            Adress          Status
# ---------------------------------------------
# web-prod-01     192.168.1.10    up
# db-primary      10.0.0.5        up
# auth-backup     172.16.0.4      down
#
# Added this from lagring.py as this module
# is the one that shuould be handling user input
# Every server is a dict containing:
# "namn": str,
# "adress": str,
# "miljo": ("dev" OR "test" OR "prod"),
# "roll": str,
# "status": ("up" OR "down" OR default="UNKNOWN"),
# "senast_kontrollerad": str(datetime)
#
# If users imputs invalid "miljo" or "namn" already exists
# the program should prompt the user again.

import sys

import lagring as lg
from kontroller import check_server_status

welcome_string = """
#########################
# Server_Inventory_Tool #
#########################
"""


def visa_alla():
    servers = lg.parse_servers_json()
    format_servers(servers)
    return 0


def qquit(n) -> bool:
    return n.lower().strip() == "q"


def visa_miljo(env=None):
    servers = lg.parse_servers_json()

    # I am populating a set of valid
    # miljos so that i do not need to
    # parse the file each time
    possible_miljo = ("dev", "test", "prod")

    if env is None:
        while True:
            env = input(
                "Skriv miljo du vill kolla upp ('dev', 'test', 'prod' eller 'q' för att avbryta): "
            )
            if qquit(env):
                return
            if env in possible_miljo:
                break
            print("Miljon finns inte. Forsok igen.")

    miljo_servers = []
    for s in servers:
        if s["miljo"] == env:
            miljo_servers.append(s)

    format_servers(miljo_servers)


def lagg_till():
    servers = lg.parse_servers_json()

    existing_names = []
    for s in servers:
        existing_names.append(s["namn"])

    valid_miljo = ("dev", "test", "prod")

    # Added this just so that i don't have to write it all the time

    while True:
        new_name = input("Skriv namn till den nya servern ('q' for att avbryta): ")
        # I don't want any problems
        new_name = new_name.lower().strip()

        if qquit(new_name):
            return

        if new_name in existing_names:
            print("Den har servern finns redan!")
            continue

        break

    while True:
        new_miljo = (
            input(
                """Vilken miljo ska den nya servern tillhora till?
    ('dev', 'test', 'prod' eller 'q' for att avbryta): """
            )
            .lower()
            .strip()
        )

        if qquit(new_miljo):
            return

        if new_miljo not in valid_miljo:
            print("Felaktig miljo!")
            continue

        break

    new_adress = input("Skriv adressen: ('q' for att avbryta): ").lower().strip()
    if qquit(new_adress):
        return

    new_roll = input("Skriv rollen: ('q' for att avbryta): ").lower().strip()
    if qquit(new_roll):
        return

    lg.add_server(new_name, new_adress, new_miljo, new_roll)


def ta_bort():
    servers = lg.parse_servers_json()

    ser_names = []
    for s in servers:
        ser_names.append((s["namn"], s["miljo"]))

    while True:
        to_del = input("Vilken server vill du ta bort? ('q' for att avbryta): ")
        if qquit(to_del):
            return

        to_del = to_del.lower().strip()

        if to_del not in ser_names[0]:
            print(f"{to_del} finns inte!")
            continue

        # Checks if to_del is "prod" in
        # which case asks for confirmatin
        if (to_del, "prod") in ser_names:
            confirm = input(f'Vill du verkligen ta bort "{to_del}"? (y/N)')

            if confirm.lower().strip() != "y":
                print("Stoppar raderingen.")
                return

        break

    lg.remove_server(to_del)


def kontrollera_en(k_server=None):
    servers = lg.parse_servers_json()

    if k_server is None:
        ser_names = []
        for s in servers:
            ser_names.append(s["namn"])

        while True:
            k_server = input("Vilken server vill du kontrollera? ('q' avbryt): ")
            if qquit(k_server):
                return

            k_server = k_server.lower().strip()

            if k_server not in ser_names:
                print(f"{k_server} finns inte!")
                continue

            break

    exit_code = check_server_status(k_server)
    if exit_code is None:
        print("Servern finns inte.")
        return 1

    print("\n\n\n")  # A little space
    print(f"{'NAMN':<15}{'ADRESS':<15}{'STATUS':<15}")
    print(45 * "-")  # lol
    format_server(lg.get_server(k_server))

    return exit_code


def kontrollera_alla():
    return_codes = set()
    servers = lg.parse_servers_json()
    for s in servers:
        return_codes.add(check_server_status(s["namn"]))

    # It updated
    servers = lg.parse_servers_json()

    print("\n\n\n")
    format_servers(servers)

    # & operator makes an intersection
    # This works because all non empty
    # sets evaluate to True and all empty
    # to False. Which is funny but i guess
    # it makes sense.
    if return_codes & {1, 2}:
        return 1

    return 0


def exportera_som_csv():
    lg.export_csv()


def avsluta():
    sys.exit(0)


option_function = [
    ["Visa alla", visa_alla],
    ["Visa miljo", visa_miljo],
    ["Lagg till", lagg_till],
    ["Ta bort", ta_bort],
    ["Kontrollera en", kontrollera_en],
    ["Kontrollera alla", kontrollera_alla],
    ["Exportera som CSV", exportera_som_csv],
    ["Avsluta", avsluta],
]


def format_server(s):
    fstring = lambda s: f"{s[:12]}..." if len(s) > 15 else f"{s:<15}"

    print(f"{fstring(s['namn'])}{fstring(s['adress'])}{fstring(s['status'])}")


def format_servers(servers):
    print(f"{'NAMN':<15}{'ADRESS':<15}{'STATUS':<15}")
    print(45 * "-")  # lol

    for s in servers:
        format_server(s)

    return 0


def menu_loop():
    """Main menu loop. Handles calling the functions."""
    print(welcome_string)

    while True:
        print("\n\n\n")  # Put this to make it a bit easier to see
        draw_menu()
        try:
            user_input = input("Skriv kommandonummer: ")
            if qquit(user_input):
                return
            else:
                user_input = int(user_input)

            if (user_input < 1) or (user_input > len(option_function)):
                print("Kommando finns inte")
                continue

            print(f"Du valde {user_input}.")
            # I need to call it like this. Now I know.
            option_function[user_input - 1][1]()

        except ValueError:
            print("Ogiltig input. Forsok igen")


def draw_menu():
    print("Meny\n------")

    entry_number = 1
    for option in option_function:
        print(f"{entry_number}. {option[0]}")
        entry_number += 1

    print("\n")
