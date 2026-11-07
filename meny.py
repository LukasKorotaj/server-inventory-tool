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
