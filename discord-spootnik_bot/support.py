import re
import os


def extract(regularE, init, stop, string):
    return re.findall(regularE, string)[0]\
             .replace(init, "")\
             .replace(stop, "")


def get_term_clock_pid():
    ret = os.popen("systemctl status sputnikDriver.service").read()
    return int(extract(r"term_clock .+ PID", "term_clock ", " PID", ret))


def check_alive():
    ret = os.popen("systemctl status sputnikDriver.service").read()
    return "java" in ret
