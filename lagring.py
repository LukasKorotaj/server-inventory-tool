# JSON handling and csv exports
#
# Every server is a dict containing:
# "namn": str,
# "adress": str,
# "miljo": ("dev" OR "test" OR "prod"),
# "roll": str,
# "status": ("UP" OR "DOWN" OR default="UNKNOWN"),
# "senast_kontrollerad": datetime
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
