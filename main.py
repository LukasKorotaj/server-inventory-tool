# Starting point, reads arguments with argparse
#
# Arguments are parsed with argparse. Possible arguments
# (copied from the instructions):
# python main.py 	Textmenyn startar.
# python main.py --lista 	Alla servrar skrivs ut och programmet avslutas.
# python main.py --lista --miljo prod 	Bara servrar i miljön prod skrivs ut.
# python main.py --kontrollera web01 	Servern web01 kontrolleras.
# python main.py --kontrollera-alla 	Alla servrar kontrolleras.
# python main.py --export 	En CSV-rapport skapas.
#
# Also add --help just for fun.
#
# Program returns 0 when all went good. (--kontrollera) if server
# does not exist or at least one server is down return 1. Use sys.exit().


import argparse
import sys

import meny as men
from lagring import export_csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Server Checking CLI")

    parser.add_argument("--lista", action="store_true", help="Lista alla servrar")
    parser.add_argument("--miljo", metavar="MILJO", choices=["dev", "test", "prod"])
    parser.add_argument(
        "--kontrollera",
        help="Kontrollera en server",
    )
    parser.add_argument(
        "--kontrollera-alla", action="store_true", help="Kontrollera alla servrar"
    )
    parser.add_argument(
        "--export", action="store_true", help="Export servers to csv file"
    )

    # Start menu if no arguments
    if len(sys.argv) == 1:
        men.menu_loop()

    args = parser.parse_args()

    if args.miljo is not None and not args.lista:
        print("Kan inte anvanda --miljo utan --lista")
        sys.exit(2)

    if args.miljo is None and args.lista:
        sys.exit(men.visa_alla())

    if args.miljo is not None and args.lista:
        sys.exit(men.visa_miljo(args.miljo))

    if args.kontrollera_alla:
        sys.exit(men.kontrollera_alla())

    if args.kontrollera is not None:
        sys.exit(men.kontrollera_en(args.kontrollera))

    if args.export:
        sys.exit(export_csv())
