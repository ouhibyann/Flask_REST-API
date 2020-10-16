from app import create_app
import unittest


class test_character(unittest.TestCase):
    app = create_app(config_name="testing")
    client = app.test_client()

    ''' --------------------------------
    Testing the getALL / READ of the API's hat
    --------------------------------------'''

    def test_getAll_hat(self):
        # This formatting is due to JSON on windows ...
        self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"")
        res = self.client.get('/hat')
        self.assertEqual(res.status_code, 200)


    ''' --------------------------------
     Testing the getOne / READ one of the API's hat
    --------------------------------------'''

    def test_getOne_hat(self):
        self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"}")
        res = self.client.get('/oneHat', data="{\"id\": 7}")
        self.assertEqual(res.status_code, 200)


    ''' --------------------------------
    Testing the CREATE / POST of the API's hat
    --------------------------------------'''

    def test_create_hat(self):
        self.client.delete('/hat', data="{\"id\": 7}")  # delete the hat if exists
        res = self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"}")
        # check status code
        print(res.data)
        self.assertEqual(res.status_code, 201)
        # check the data sent with the status code As the order of the elements in the JSON may be different,
        # we only check that the correct id is return in the whole data
        self.assertIn("\"id\": 7", str(res.data))

    def test_alreadyExist_create_hat(self):
        res = self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"}")
        # we send it a second time so the app should respond 'user already exists, 400"
        res = self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"}")
        self.assertEqual(res.status_code, 400)
        self.assertIn("Hat already exists", str(res.data))

    def test_NoInput_create_hat(self):
        res = self.client.post('/hat', data="{}")
        self.assertEqual(res.status_code, 400)
        self.assertIn("No input data provided", str(res.data))


    ''' --------------------------------
    Testing the DELETE of the API's hat
    --------------------------------------'''

    def test_delete_hat(self):

        self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"}")
        res = self.client.delete('/hat', data="{\"id\":7}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Hat deleted", str(res.data))

    def test_Missing_delete_hat(self):
        # First delete of the character, then another one
        self.client.delete('/hat', data="{\"id\":7}")
        res = self.client.delete('/hat', data="{\"id\":7}")
        self.assertEqual(res.status_code, 400)
        self.assertIn('Hat already missing', str(res.data))

    def test_NoInput_delete_character(self):
        res = self.client.delete('/hat', data="{}")
        self.assertEqual(res.status_code, 400)
        self.assertIn('No input data provided', str(res.data))

    ''' --------------------------------
        Testing the update / PUT of the API's hat
        --------------------------------------'''

    def test_update_character(self):
        self.client.post('/hat', data="{\"id\": 7,\"colour\": \"YELLOW\"}")
        res = self.client.put('/hat', data="{\"id\":1,  \"colour\":\"PURPLE\"}")
        self.assertEqual(res.status_code, 201)

    def test_NoInput_update_character(self):
        res = self.client.put('/hat', data="{}")
        self.assertEqual(res.status_code, 400)
        self.assertIn('No input data provided', str(res.data))

    def test_NoExist_update_Character(self):
        self.client.delete('/hat', data="{\"id\":7}")
        res = self.client.put('/hat', data="{\"id\":7,  \"colour\":\"PURPLE\"}")
        self.assertEqual(res.status_code, 400)
        self.assertIn('Hat does not exist', str(res.data))


if __name__ == "__main__":
    unittest.main()
