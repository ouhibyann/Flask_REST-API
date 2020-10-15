import app
import unittest


class test_get_character(unittest.TestCase):

    def setup(self):
        self.app = app.app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client

    def test_get_response(self):
        res = self.client().get('/character')
        self.assertEqual(res.status_code, 200)

if __name__ == "__main__":
    unittest.main()