import datetime
import config
import time
import os
import subprocess
import sys
import threading
import logging
from dotenv import load_dotenv()

from signal import signal, SIGINT, SIGALRM, SIGTERM, SIGUSR1, SIGUSR2
load_dotenv()
MC_PATH = os.getenv("MC_PATH")
class MinecraftServer:
    """
    Class MinecraftServer

    Objects of this class can open a Minecraft Server and control it with its methods.
    """

    def __init__(self):
        """
            Return: Object MinecraftServer initiated
        
        Constructor of class MinecraftServer. Initializes proc variable to None.
        """
        self.proc = None


    def startServer(self, verbose=False):
        """
            verbose (Boolean): If True, catch in log the server output. Defaults to False.

            return (Boolean): True if all went well;
                              False in other case.
        
        Starts the server immediately and stores the process in proc for later use.
        Path to Java executable and command read from config.py.
        """

        # Check if process already up
        if self.proc is not None:
            logging.error("startServer called when server is already up!")
            return False

        else:
            logging.info("Starting Minecraft server")
            try:
                self.proc = subprocess.Popen(config.MC_EXEC,
                                             stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.STDOUT,
                                             cwd=MC_PATH)
                self.wait_for_string(["Done"], stream=self.proc.stdout, verbose=verbose)
                logging.info("Server started!")
                print("Server started!")

            except OSError as e:
                logging.error("Exception OSError occurred: ")
                logging.error(str(e))
                return False
            
            return True


    def serverInputs(self, pid: int):
        # Set signal to exit gracefully in case SIGINT is issued
        signal(SIGINT, self.exit_proc)

        # List of actual server inputs:
        inputs = ["/stop", "--extend"]

        if not self.proc:
            logging.error("serverInputs called when server wasn't up!")
            return None

        logging.info("serverInputs: Initiated. Starting to listen")

        while True:
            line = self.wait_for_string(inputs, stream=self.proc.stdout)

            # Behaviour of server commands/inputs
            # a.
            if line == "/stop":
                os.kill(pid, SIGINT)
                sys.exit()
            
            # Extend server time.
            elif line == "--extend":
                os.kill(pid, SIGUSR1)


    def term_clock(self):
        """
            seconds (float): Number of seconds until shutdown the server. Defaults to 0, but in this
                             case the time is calculated as shown below (not killed instantly).

        Initiates the term clock and sleeps (BLOCKS) the process until time of term.
        If SIGUSR1 sent, terms in 30 minutes. Can be sent multiple times to extend time.
        If SIGTERM sent, terms instantly.
        If SIGINT sent, exits without terminating the server.
        """

        # Handler for SIGUSR1 signal
        def extend(signal, frame):
            """
                signal: Signal recieved.
                frame: No idea (header required).
            
            Called when there is 30 minutes left to term or when extend is requested.
            In both cases, sets the timer to 30 minutes and sleeps to that timer.
            Then terminates the server after a countdown. Can be stopped with another
            SIGUSR1 signal.
            """
            self.termSec = 30 * 60
            if signal is not None:
                # It was the signal what called the method. Send feedback of the command.
                self.cmd("say Vuestras plegarias han sido escuchadas. "
                         "Cerrando servidor en {} minutos".format(str(int(self.termSec / 60))))
                os.system("shutdown -c")
                os.system("shutdown +35")
            logging.info("term_clock: extend called. Closing in {} seconds".format(str(self.termSec)))

            # Start a sequence to warn when 5 and 1 minutes are left. Sleep till then.
            time.sleep(self.termSec - 5 * 60)
            
            self.cmd("say Cerrando servidor en 5 minutos.")
            time.sleep(4 * 60)

            self.cmd("say Cerrando servidor en 1 minuto.")
            time.sleep(55)

            self.cmd("say Cerrando en 5...")
            time.sleep(1)
            self.cmd("say Cerrando en 4...")
            time.sleep(1)
            self.cmd("say Cerrando en 3...")
            time.sleep(1)
            self.cmd("say Cerrando en 2...")
            time.sleep(1)
            self.cmd("say Cerrando en 1...")
            time.sleep(1)
            self.cmd("say PAPOPEPOPARAPAPAPAPA")
            time.sleep(1)
            term(None, None)

        # Handler for SIGTERM signal
        def term(signal, frame):
            """
                signal: Signal recieved.
                frame: No idea (header required).
            
            Terminates the server and then exits this process
            """
            logging.info("term_clock: Terminating server.")
            self.kill_server()
            sys.exit()

        # Set the signals
        signal(SIGUSR1, extend)
        signal(SIGTERM, term)
        signal(SIGINT, self.exit_proc)

        # Terminate at 01:30
        self.termSec = (24 - datetime.datetime.today().hour) * 60 * 60
        self.termSec += (90 - datetime.datetime.today().minute) * 60

        # Sleep for the time being
        logging.info("term_clock: Initiated. Sleeping {} hours until shutdown".format(str(self.termSec / 3600)))

        # Sleep for the time minus 30 minutes and send a warning
        time.sleep(self.termSec - 30 * 60)
        self.cmd("say Cerrando servidor en 30 minutos.")

        # We can now safely call "extend" to save coding
        extend(None, None)

        # This is here for safety purposes
        term(None, None)


    def kill_server(self):
        """
        Stops the server, if exists. Sets the proc variable to None when success.
        """
        if self.proc is not None:
            # Issue stop command and wait
            self.cmd("stop")
            self.proc.wait()
            self.proc = None
        
        else:
            logging.info("kill_server: Tried to kill the server, but its not started!")


    def wait_for_string(self, strings, stream, verbose=False):
        """
        Waits for an occurance of str_ in stream. May never return! Using a
        timeout would only work if the stream is non-blocking, and that
        means extra work to buffer in case the str_ gets split up

        Copyright ojrac at https://gist.github.com/ojrac/1237524 (2011)
        Modified by Ivanska
        """

        # Set handler to exit gracefully in case SIGINT is issued
        signal(SIGINT, self.exit_proc)

        while True:
            line = stream.readline()
            if verbose:
                logging.info("wait_for_string: Read -> " + str(line))

            for str_ in strings:
                if str_ in str(line):
                    logging.info("wait_for_string: Recognized command {}".format(str_))
                    return str_


    def cmd(self, cmd: str):
        """
            cmd (str): Complete string with all the text sent to Minecraft's console.
        
            return (Boolean): True if command issued without problems;
                              False in other case (proc is None)

        Writes to Minecraft's stdin the command passed in cmd.
        """
        if self.proc is None:
            logging.error("cmd called when server wasn't up!")
            return False

        else:
            logging.info("Issuing command: " + cmd)
            self.proc.stdin.write(bytes(cmd + "\r\n", "ascii"))
            self.proc.stdin.flush()
            return True


    # Handler for SIGINT signals
    def exit_proc(self, signal, frame):
        """
            signal: Signal recieved.
            frame: No idea (header required).
            
        Exits this process without doing anything.
        """
        logging.info("Recieved SIGINT; exiting")
        sys.exit()
