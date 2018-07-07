import os
import traceback
import urllib.request
from datetime import datetime

import heroku3
from apscheduler.schedulers.blocking import BlockingScheduler
from pytz import timezone

sc = BlockingScheduler()

KEEPALIVE_URL = os.environ.get('KEEPALIVE_URL', '')
IS_AM = os.environ.get('IS_AM', '')
IS_PM = os.environ.get('IS_PM', '')
SELF_API_KEY = os.environ.get('SELF_API_KEY', '')
ANOTHER_API_KEY = os.environ.get('ANOTHER_API_KEY', '')


def keep_alive():
    now = datetime.now(timezone('Asia/Tokyo'))
    if 0 <= now.hour <= 7:
        return
    if KEEPALIVE_URL:
        for url in KEEPALIVE_URL.split(';'):
            try:
                urllib.request.urlopen(url)
            except:
                traceback.print_exc()


def swich_work():
    def inner():
        try:
            another_conn = heroku3.from_key(ANOTHER_API_KEY)
            another_app = list(another_conn.apps())[0]
            another_app.process_formation()['clock'].scale(1)

            self_conn = heroku3.from_key(SELF_API_KEY)
            self_app = list(self_conn.apps())[0]
            self_app.process_formation()['clock'].scale(0)
        except:
            traceback.print_exc()

    now = datetime.now(timezone('Asia/Tokyo'))
    if IS_AM and now.strftime('%p') == 'PM':
        inner()
    elif IS_PM and now.strftime('%p') == 'AM':
        inner()


@sc.scheduled_job('interval', minutes=10)
def do_work():
    keep_alive()
    swich_work()


def main():
    sc.start()


if __name__ == '__main__':
    main()
