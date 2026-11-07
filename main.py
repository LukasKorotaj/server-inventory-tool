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


if __name__ == "__main__":
    pass
