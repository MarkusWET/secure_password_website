import urllib.request
import urllib.error
from flask import Flask
from flask_testing import LiveServerTestCase


# Testing with LiveServer
class MyTest(LiveServerTestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def test_app_start(self):
        try:
            response = urllib.request.urlopen(self.get_server_url())
            self.assertEqual(response.status, 200)
        except urllib.error.HTTPError as err:
            self.fail("[{}] {}".format(err.code, err.reason))
        except urllib.error.URLError as err:
            self.fail(err.reason)
