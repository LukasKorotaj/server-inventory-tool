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

welcome_string = """
#########################
# Server_Inventory_Tool #
#########################
"""


def visa_alla():
    pass


def visa_miljo():
    pass


def lagg_till():
    pass


def ta_bort():
    pass


def kontrollera_en():
    pass


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


def format_servers(servers):
    print(f"{'NAMN':<15}{'ADRESS':<15}{'STATUS':<15}")
    print(45 * "-")  # lol

    fstring = lambda s: f"{s[:12]}..." if len(s) > 15 else f"{s:<15}"

    for s in servers:
        print(f"{fstring(s['namn'])}{fstring(s['adress'])}{fstring(s['status'])}")


def handle_input():
    """Waits for user input and handles incorrect input.
    Also ties the menu number to its function."""
    while True:
        try:
            user_input = int(input("Skriv kommandonummer: "))
            if 1 <= user_input <= option_function.__len__():
                break
            print("Kommando finns inte")

        except ValueError:
            print("Ogiltig input. Försök igen")

    print(f"Du valde {user_input}.")
    option_function[user_input - 1][1]


def draw_menu():
    print("Meny\n------")

    entry_number = 1
    for option in option_function:
        print(f"{entry_number}. {option[0]}")
