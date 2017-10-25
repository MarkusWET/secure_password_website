import urllib3
from flask import Flask
from flask_testing import LiveServerTestCase


# Testing with LiveServer
class MyTest(LiveServerTestCase):

    # if the create_app is not implemented NotImplementedError will be raised
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_app_start(self):
        response = urllib3.connection_from_url(self.get_server_url())
        self.assertEqual(response.code, 200)
