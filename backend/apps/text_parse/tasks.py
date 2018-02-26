from os import fstat, unlink
import time
import string
import redis
from django.conf import settings
from backend.celery_app import app
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


@app.task
def parse_file(file_path, file_name, redis_name):
    log.info('file_path = %r, file_name = %r, redis_name = %r',
             file_path, file_name, redis_name)
    result = {
        'file_name': file_name,
        'parsed_percentage': 0,
        'digits': 0,
        'charachters': 0,
        'whitespaces': 0,
        'punctuation': 0
    }
    r = redis.Redis.from_url(settings.REDIS_URL)
    r.hmset(redis_name, result)
    file = open(file_path, 'r')
    stat_result = fstat(file.fileno())
    size = stat_result.st_size
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
                result['charachters'] += 1
            result['parsed_percentage'] = round((float(file.tell()) * 100) / size)
            r.hmset(redis_name, result)
            if size <= file.tell():
                break
            time.sleep(0.1)
    finally:
        file.close()
        unlink(file_path)
