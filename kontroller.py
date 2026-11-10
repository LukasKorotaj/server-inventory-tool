# Checks server status
#
# Status is checked with `subprocess.run()`
# and the `ping` command.
# Exit code decides the status.
#
# Upon check "status" is updated to "UP" or "DOWN"
# "senast_kontrollerad" is updated to the current date and time
# format: "YYYY-MM-DD HH:mm"


import subprocess

import lagring as lg


def get_server_adress(namn):
    return lg.get_server(namn)["adress"]


def check_server_status(namn):
    """Check status of server and update INVENTORY_DATAFIL."""
    adress = get_server_adress(namn)

    # runs: ping -c 3 {server_adress}
    # Explicit check (LSP crying)
    # Set the check to false because I don't
    # really care about the return object type
    # Added timeout of 2 (-W 2) to exit in normal time
    # when packet loss is 100%.
    # Note the 'W' here (upper). lower 'w' can block
    # the last ping giving exit code 1
    command_output = subprocess.run(["ping", "-W", "1", "-c", "2", adress], check=False)

    match command_output.returncode:
        case 0:
            return_status = "UP"
        case 1 | 2:
            return_status = "DOWN"
        case code:
            raise RuntimeError(f"Unexpected return code: {code}")

    lg.update_server_status(namn, status=return_status)

    # NOTE: I was thinking about capturing the final ping time
    # so that the timestamp is extra accurate but since i am only
    # capturing up to the minute it would just be useless code
