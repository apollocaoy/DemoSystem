import unittest

import json
import redis
from api import app

class TestDemoApi(unittest.TestCase):


    def setUp(self):

        redisConn = redis.Redis('192.168.99.100', 6379)

        redisConn.set('ebddbb7d-29f3-4cb8-877f-313d1d6e296f', 'test value')

    def test_index(self):

        self.test_app = app.test_client()

        response = self.test_app.get('/', content_type='application/json')

        self.assertEqual(response.status_code, 200)

        self.assertIsNotNone(response.data)

    def test_get_notfound(self):

        self.test_app = app.test_client()

        response = self.test_app.get('/12b07c79-92e1-4e6b-a4b7-49dd2bdba9a3', content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_get_found(self):

        self.test_app = app.test_client()

        response = self.test_app.get('/ebddbb7d-29f3-4cb8-877f-313d1d6e296f', content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data)
        #self.assertEqual('ebddbb7d-29f3-4cb8-877f-313d1d6e296f', response.data['key'])
        #self.assertEqual('test value', response.data['value'])

    def test_post(self):

        self.test_app = app.test_client()

        data = {}
        data['key'] = ''
        data['value'] = 'value'

        response = self.test_app.post('/', content_type='application/json', data=json.dumps(data))

        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':

    unittest.main()
