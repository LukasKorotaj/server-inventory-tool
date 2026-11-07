# Checks server status
#
# Status is checked with `subprocess.run()`
# and the `ping` command.
# Exit code decides the status.
#
# Upon check "status" is updated to "UP" or "DOWN"
# "senast_kontrollerad" is updated to the current date and time
# format: "YYYY-MM-DD HH:mm"
