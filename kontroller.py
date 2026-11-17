# Checks server status
#
# Status is checked with `subprocess.run()`
# and the `ping` command.
# Exit code decides the status.
#
# Upon check "status" is updated to "up" or "down"
# "senast_kontrollerad" is updated to the current date and time
# format: "YYYY-MM-DD HH:mm"


import subprocess

import lagring as lg

def check_webserver_status(namn, adress):
    """Check status of a webserver and update INVENTORY_DATAFIL."""

    # Explicit check (LSP crying)
    # Set the check to false because I don't
    # really care about the return object type
    # Also, AI tools force -o /dev/null 
    # while in the man pages, under --output 
    # --out-null is right there.
    #
    # NOTE: I was curious as to 
    # why --out-null wasn't recommended so 
    # I checked when it came out. September 
    # 2025 is the answer. That means 
    # there is a risk that some LTS distros 
    # are not on that version. So I changed 
    # it to -o /dev/null.
    command_output = subprocess.run(
        ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "2", adress],
        check=False,
        capture_output=True,
    )

    # Assigns the last line containing the http exit 
    # code to return_code as an integer.
    return_code = int(command_output.stdout)

    # According to mozilla, anything starting with 
    # 2 is success
    if 200 <= return_code < 300:
        return_status = "up"
    else:
        return_status = "down"

    lg.update_server_status(namn, status=return_status)

    return 0 if return_status == "up" else 1


def check_server_status(namn):
    """Check status of server and update INVENTORY_DATAFIL."""
    server = lg.get_server(namn)
    if server is None:
        return None

    adress = server["adress"]

    if server["roll"] == "webbserver":
        return check_webserver_status(namn, adress)


    # runs: ping -c 3 {server_adress}
    # Explicit check (LSP crying)
    # Set the check to false because I don't
    # really care about the return object type
    # Added timeout of 2 (-W 2) to exit in normal time
    # when packet loss is 100%.
    # Note the 'W' here (upper). lower 'w' can block
    # the last ping giving exit code 1
    command_output = subprocess.run(
        ["ping", "-W", "1", "-c", "2", adress],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    match command_output.returncode:
        case 0:
            return_status = "up"
        case 1 | 2:
            return_status = "down"
        case code:
            raise RuntimeError(f"Unexpected return code: {code}")

    lg.update_server_status(namn, status=return_status)

    return 0 if return_status == "up" else 1

    # NOTE: I was thinking about capturing the final ping time
    # so that the timestamp is extra accurate but since i am only
    # capturing up to the minute it would just be useless code
