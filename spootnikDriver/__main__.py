import logging
import config
import datetime
import multiprocessing as mp
import os
from dotenv import load_dotenv

from MinecraftServer import MinecraftServer

load_dotenv()
LOG_PATH = os.getenv("LOG_PATH")


def main():
    mp.set_start_method("fork")
    logging.basicConfig(filename=LOG_PATH +
                        str(datetime.datetime.today()),
                        level=logging.DEBUG,
                        format="%(levelname)s:%(message)s")

    logging.info("sputnikDriver started.")
    print("__main__ {} PID".format(str(os.getpid())))

    # Shutdown at 1:35 by default
    """
    shutdown_mins = (24 - datetime.datetime.today().hour) * 60
    shutdown_mins += 90 - datetime.datetime.today().minute + 5
    os.system("shutdown +{}".format(shutdown_mins))
    logging.info("Set shutdown time in {} hours".format(shutdown_mins / 60))
    """
    logging.info("Starting MinecraftServer")
    mcServer = MinecraftServer()
    if not mcServer.startServer():
        print("Some error ocurred")
        return 0
    """
    term_clock = mp.Process(target=mcServer.term_clock)
    term_clock.start()
    print("term_clock {} PID".format(str(term_clock.pid)))
    
    serverInputs = mp.Process(target=mcServer.serverInputs, args=(term_clock.pid,))
    serverInputs.start()
    print("serverInputs {} PID".format(str(serverInputs.pid)))
    """
    return 0


if __name__ == "__main__":
    main()
