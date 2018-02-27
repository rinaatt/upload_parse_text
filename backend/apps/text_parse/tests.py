import json
import time
from io import StringIO
from django.test import TestCase
from django.urls import reverse


FAKE_FILE = StringIO("""\
Hello World!
Проверка загрузки файла.
0123456789
#()+-.,;
""")
FAKE_FILE.name = 'hello_world.txt'
FAKE_FILE.content_type = 'text/plain; charset=utf-8'
FAKE_FILE_RESULT = {
    'file_name': FAKE_FILE.name,
    'parsed_percentage': 100,
    'digits': 10,
    'characters': 5+5+8+8+5,
    'whitespaces': 7,
    'punctuation': 2+8,
    'done': True,
}


class ViewTests(TestCase):

    def test_index(self):
        time.sleep(1)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_upload(self):
        time.sleep(1)
        response = self.client.post(
            reverse('xhr', kwargs={'action_name': 'upload'}),
            data={'file': FAKE_FILE},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['result'], 'OK')
        time.sleep(0.5)
        response = self.client.get(data['next'])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, FAKE_FILE.name)

    def test_parse(self):
        time.sleep(1)
        response = self.client.post(
            reverse('xhr', kwargs={'action_name': 'upload'}),
            data={'file': FAKE_FILE},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        time.sleep(0.5)
        parse_response = self.client.get(
            reverse('xhr', kwargs={'action_name': 'parse_results'}),
            data={'hash': data['result_hash']},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(parse_response.status_code, 200)
        parse_result = json.loads(parse_response.content)
        self.assertEqual(FAKE_FILE_RESULT['file_name'],
                         parse_result['file_name'])
        self.assertEqual(FAKE_FILE_RESULT['digits'],
                         parse_result['digits'])
        self.assertEqual(FAKE_FILE_RESULT['characters'],
                         parse_result['characters'])
        self.assertEqual(FAKE_FILE_RESULT['whitespaces'],
                         parse_result['whitespaces'])
        self.assertEqual(FAKE_FILE_RESULT['punctuation'],
                         parse_result['punctuation'])
