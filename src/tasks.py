import os
import time
from datetime import datetime
import urllib.request
import json

from celery import Celery


app = Celery("tasks",
             broker=os.environ.get('CELERY_BROKER_URL', 'redis://'),
             backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis'))
app.conf.CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
app.conf.CELERY_WORKER_SEND_TASK_EVENTS = True


@app.task
def add(x, y):
    return x + y


@app.task
def sleep(seconds):
    time.sleep(seconds)

    
@app.task(bind=True)
def sleep_wh(self, seconds, callback):
    time.sleep(seconds)
    if callback:
        req = urllib.request.Request(callback, 
            data=json.dumps({'taskId':self.request.id, 'result': 'OK'}).encode('utf-8'),
            headers={'content-type': 'application/json'})
        urllib.request.urlopen(req)


@app.task
def echo(msg, timestamp=False):
    return "%s: %s" % (datetime.now(), msg) if timestamp else msg


@app.task
def error(msg):
    raise Exception(msg)


if __name__ == "__main__":
    app.start()