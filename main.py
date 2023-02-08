import datetime
import flask
import ping3
import threading
import time
from tinyflux import TinyFlux, Point

IP_TO_PING = '192.168.0.1'
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

@app.route('/')
def root():
    return f'<p>{len(db)}</p>'


if __name__ == "__main__":
    threading.Thread(target=pingThread, daemon=True).start()
    app.run(debug=True)
