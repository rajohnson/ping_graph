import datetime
import flask
import ping3
import threading
import time
from tinyflux import TinyFlux, Point

IP_TO_PING = '192.168.0.1'
PING_INTERVAL_S = 1
DATABASE_FILE = 'db\pingData.tinyflux'

db = TinyFlux(DATABASE_FILE)

def pingThread():
    while True:
        p = Point(time=datetime.datetime.now(),fields={"ping_ms": ping3.ping(IP_TO_PING, unit="ms")})
        db.insert(p)
        time.sleep(PING_INTERVAL_S)  # there is a little extra time from the ping, but not dealing with it here.


app = flask.Flask(__name__)

@app.route('/')
def root():
    return f'<p>{len(db)}</p>'


if __name__ == "__main__":
    threading.Thread(target=pingThread, daemon=True).start()
    app.run(debug=True)
