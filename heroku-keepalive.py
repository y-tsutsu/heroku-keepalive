import os
from pytz import timezone
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import urllib.request
import traceback

sc = BlockingScheduler()


@sc.scheduled_job('interval', minutes=10)
def do_work():
    now = datetime.now(timezone('Asia/Tokyo'))
    if 0 <= now.hour <= 7:
        return
    if 'KEEPALIVE_URL' in os.environ:
        try:
            urllib.request.urlopen(os.environ['KEEPALIVE_URL'])
        except:
            traceback.print_exc()


sc.start()
