import unittest

from flask_testing import TestCase
from app import app


class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app


class Test(BaseTestCase):
    def test_p(self):
        pass

    def test_city(self):
        self.assert200(self.client.get('/city/all'))

    def test_certain_city(self):
        self.assert405(self.client.get('/city/500'))


if __name__ == '__main__':
    unittest.main()
