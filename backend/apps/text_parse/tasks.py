from os import fstat
import time
import string
from backend.celery_app import app


@app.task
def parse_file(file_path):
    result = {
        'parsed_percentage': 0,
        'digits': 0,
        'charachters': 0,
        'whitespaces': 0,
        'punctuation': 0
    }
    file = open(file_path, 'r')
    stat_result = fstat(file.fileno())
    size = stat_result.st_size
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
        result['parsed_percentage'] = round((file.tell() * 100) / size)

        if size <= file.tell():
            break
        time.sleep(0.5)
