import datetime
import threading
import time

import flask
import ping3
from tinyflux import Point, TimeQuery, TinyFlux

IP_TO_PING = "192.168.0.1"
PING_INTERVAL_S = 1
DATABASE_FILE = "pingData.tinyflux"

db = TinyFlux(DATABASE_FILE)


def pingThread():
    while True:
        p = Point(
            measurement="Ping time",
            tags={"IP": IP_TO_PING},
            fields={"ping_ms": ping3.ping(IP_TO_PING, unit="ms")},
        )
        db.insert(p)
        # The interval isn't met perfectly with the time taken for the ping,
        # but it is close enough that it won't be worth dealing with here.
        time.sleep(PING_INTERVAL_S)


app = flask.Flask(__name__)


@app.route("/")
def root():
    return f"<p>{len(db)}</p>"


@app.route("/last")
def most_recent():
    q = TimeQuery() > datetime.datetime.now() - datetime.timedelta(minutes=1)
    return f"<p>{db.get(q)}</p>"


@app.route("/lastmin")
def last_minute():
    q = TimeQuery() > datetime.datetime.now() - datetime.timedelta(minutes=1)
    return f"<p>{db.search(q)}</p>"


@app.route("/all")
def all_readings():
    return {point.time.strftime("%m/%d/%Y, %H:%M:%S"): point.fields['ping_ms'] for point in db.all()}


if __name__ == "__main__":
    threading.Thread(target=pingThread, daemon=True).start()
    app.run(debug=True)
