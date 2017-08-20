import os
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import traceback
import heroku3

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
        try:
            urllib.request.urlopen(KEEPALIVE_URL)
        except:
            traceback.print_exc()


def swich_work():
    def inner():
        try:
            another_conn = heroku3.from_key(ANOTHER_API_KEY)
            another_app = another_conn.apps()['heroku-keepalive-{}'.format('pm' if IS_AM else 'am')]
            another_app.process_formation()['clock'].scale(1)

            self_conn = heroku3.from_key(SELF_API_KEY)
            self_app = self_conn.apps()['heroku-keepalive-{}'.format('am' if IS_AM else 'pm')]
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


sc.start()
