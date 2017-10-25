import unittest
from app import app


class LoginTests(unittest.TestCase):
    # initialization logic for the test suite declared in the test module
    # code that is executed before all tests in one test run
    @classmethod
    def setUpClass(cls):
        pass

    # clean up logic for the test suite declared in the test module
    # code that is executed after all tests in one test run
    @classmethod
    def tearDownClass(cls):
        pass

    # initialization logic
    # code that is executed before each test
    def setUp(self):
        # create test client
        self.app = app.test_client()

        # set to testing
        self.app.testing = True

    # clean up logic
    # code that is executed after each test
    def tearDown(self):
        pass

    # test method
    def test_startpage(self):
        result = self.app.get("/")

        self.assertEqual(result.status_code, 200)

        # test method
    def login_test_md5(self):
        pass


# runs the unit tests in the module
if __name__ == '__main__':
    unittest.main()
