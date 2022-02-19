import os
import pathlib
import time
import logging
import datetime
from dotenv import load_dotenv
import pandas as pd
import requests


load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
IVANSKA_ID = os.getenv("IVANSKA_ID")
NARA_ID = os.getenv("NARA_ID")
LOC1 = os.getenv("LOC1")
LOC2 = os.getenv("LOC2")
LOCC = os.getenv("LOCC")
MAXLAT = os.getenv("MAXLAT")
MINLAT = os.getenv("MINLAT")
MAXLONG = os.getenv("MAXLONG")
MINLONG = os.getenv("MINLONG")

URL = "https://www.komparing.com/es/gasolina/include/process-xml_maxLat{}_minLat{}_maxLong-{}_minLong-{}_zoomMapa-11_order-gsAs_gsA" \
    .format(MAXLAT, MINLAT, MAXLONG, MINLONG)
TELEGRAM_API = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&parse_mode=Markdown&text={}"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def fetch_prices():
    r = requests.get(URL)
    df = pd.read_xml(r.text)

    col_filters = ["localidad", "direcc", "rotulo",
                   "gasolina_95", "gasoleo_A_normal"]
    loc_filters = (
        (df.localidad == LOC1) |
        (df.localidad == LOC2)
    )

    df = df[col_filters]
    df = df[loc_filters]
    df = df[(df.gasolina_95 != 0) &
            (df.gasoleo_A_normal != 0)]
    df = df.sort_values(by="gasolina_95").head(3)

    prices_df = pd.read_csv(os.path.join(
        pathlib.Path(__file__).parent.resolve(), "prices.csv"))
    prices_df.loc[len(prices_df)] = df.head(1).values[0]
    prices_df.to_csv("prices.csv", index_label=False)

    return df.values


def get_msg():
    prices = fetch_prices()
    ret = "¡Buenos días! Hoy los combustibles más baratos están en:\n\n"
    for p in prices:
        if p[0] == LOC1:
            p[0] = LOCC
        ret += "{}, en {}. ({})\n".format(
            p[2], p[1], p[0]
        )
        ret += "Gasóleo: {} €/L\nGasolina: {} €/L\n\n".format(
            p[4], p[3]
        )
    return ret


if __name__ == "__main__":
    H = 8
    M = 0
    # "Half-ass" solution made by:
    # https://stackoverflow.com/questions/2031111/in-python-how-can-i-put-a-thread-to-sleep-until-a-specific-time

    for _ in range(0, 365):
        t = datetime.datetime.today()
        future = datetime.datetime(t.year, t.month, t.day, H, M)
        if t.hour >= H:
            future += datetime.timedelta(days=1)

        logger.info("Time sleep: {} seconds.".format((future-t).total_seconds()))
        logger.info("Today: {}.".format(t))
        logger.info("Future: {}.".format(future))

        time.sleep((future-t).total_seconds())

        requests.get(TELEGRAM_API.format(
            TOKEN, IVANSKA_ID, get_msg()
        ))
        requests.get(TELEGRAM_API.format(
                    TOKEN, NARA_ID, get_msg()
                ))
