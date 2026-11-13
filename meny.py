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
# web-prod-01     192.168.1.10    UP
# db-primary      10.0.0.5        UP
# auth-backup     172.16.0.4      DOWN
#
# Added this from lagring.py as this module
# is the one that shuould be handling user input
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

from kontroller import check_server_status
import lagring as lg

welcome_string = """
#########################
# Server_Inventory_Tool #
#########################
"""


def visa_alla():
    servers = lg.parse_servers_json()
    format_servers(servers)


def qquit(n) -> bool:
    return n.lower().strip() == "q"


def visa_miljo():
    servers = lg.parse_servers_json()

    # I am populating a set of valid
    # miljos so that i do not need to
    # parse the file each time
    possible_miljo = ("dev", "test", "prod")

    while True:
        user_input = input(
            "Skriv miljo du vill kolla upp ('dev', 'test', 'prod' eller 'q' för att avbryta): "
        )
        if qquit(user_input):
            return
        if user_input in possible_miljo:
            break
        print("Miljon finns inte. Forsok igen.")

    miljo_servers = []
    for s in servers:
        if s["miljo"] == user_input:
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
        new_name.lower().strip()

        if qquit(new_name):
            return

        if new_name in existing_names:
            print("Den har servern finns redan!")
            continue

        break

    while True:
        new_miljo = input(
            """Vilken miljo ska den nya servern tillhora till?
    ('dev', 'test', 'prod' eller 'q' for att avbryta): """
        )

        if qquit(new_miljo):
            return

        if new_miljo.lower().strip() not in valid_miljo:
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
        ser_names.append(s["namn"])

    while True:
        to_del = input("Vilken server vill du ta bort? ('q' for att avbryta): ")
        if qquit(to_del):
            return

        to_del = to_del.lower().strip()

        if to_del not in ser_names:
            print(f"{to_del} finns inte!")
            continue

        confirm = input(f'Vill du verkligen ta bort "{to_del}"? (y/N)')

        if confirm.lower().strip() != "y":
            print("Stoppar raderingen.")
            return

        break

    lg.remove_server(to_del)


def kontrollera_en():
    servers = lg.parse_servers_json()

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

    check_server_status(k_server)

    print(f"{'NAMN':<15}{'ADRESS':<15}{'STATUS':<15}")
    print(45 * "-")  # lol
    format_server(lg.get_server(k_server))
    


def kontrollera_alla():
    pass


def exportera_som_csv():
    pass


def avsluta():
    pass


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



def menu_loop():
    """Main menu loop. Handles calling the functions."""
    print(welcome_string)

    while True:
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
