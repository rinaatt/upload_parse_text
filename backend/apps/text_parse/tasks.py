from os import fstat, unlink, stat
import time
import string
import redis
import json
from django.conf import settings
from backend.celery_app import app
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)
PARSE_SLEEP = getattr(settings, 'PARSE_SLEEP', 0)

r = redis.Redis.from_url(settings.REDIS_URL)


def save_to_redis(name, value):
    r.set(name, json.dumps(value))


@app.task
def parse_file(file_path, file_name, redis_name):
    log.info('file_path = %r, file_name = %r, redis_name = %r',
             file_path, file_name, redis_name)
    result = {
        'file_name': file_name,
        'parsed_percentage': 0,
        'digits': 0,
        'characters': 0,
        'whitespaces': 0,
        'punctuation': 0,
        'done': False,
    }
    save_to_redis(redis_name, result)
    stat_result = stat(file_path)
    file = open(file_path, 'r')
    try:
        while True:
            symbol = file.read(1)
            if symbol in string.punctuation:
                result['punctuation'] += 1
            elif symbol in string.digits:
                result['digits'] += 1
            elif symbol in string.whitespace:
                result['whitespaces'] += 1
            else:
                result['characters'] += 1
            if stat_result.st_size > 0:
                result['parsed_percentage'] = round(
                    (float(file.tell()) * 100) / stat_result.st_size
                )
            else:
                result['parsed_percentage'] = 100
            save_to_redis(redis_name, result)
            if file.tell() >= stat_result.st_size:
                break
            time.sleep(PARSE_SLEEP)
    finally:
        result['done'] = True
        save_to_redis(redis_name, result)
        file.close()
        unlink(file_path)
