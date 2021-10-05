from requests import get
from support import extract
import re

URL = "http://randomfactgenerator.net/"

def random_fact():
    response = get(URL)
    fact = extract(r"<div id=\\'z\\'>.+?<br/>",
                   "<div id=\\'z\\'>",
                   "<br/>",
                   str(response.content))

    fact_updated = fact.replace(".", "?", 1)
    if fact_updated == fact:
        fact = fact[:-1] + "?"
    else:
        fact = fact_updated
    if fact[0] == " ":
        fact = fact[1:]
    fact = fact[0].lower() + fact[1:]
    return fact
