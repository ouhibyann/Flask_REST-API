from app import create_app
from models.db import db
from models.character import Character
import unittest
import json


class test_character(unittest.TestCase):
    app = create_app(config_name="testing")
    client = app.test_client()

    ''' --------------------------------
    Testing the getALL / READ of the API's character
    --------------------------------------'''

    def test_getAll_character(self):
        # This formatting is due to JSON on windows ...
        self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                            "\"True\",\"hat\": 3}")
        res = self.client.get('/character', data={"id": 7})
        self.assertEqual(res.status_code, 200)

    ''' --------------------------------
     Testing the getOne / READ one of the API's character
    --------------------------------------'''

    def test_getOne_character(self):
        self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                            "\"True\",\"hat\": 3}")
        res = self.client.get('/oneCharacter', data="{\"id\": 7}")
        self.assertEqual(res.status_code, 200)

    ''' --------------------------------
    Testing the CREATE / POST of the API's character
    --------------------------------------'''

    def test_create_response(self):
        self.client.delete('/character', data="{\"id\": 7}")  # delete the character if exists
        res = self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                                  "\"True\",\"hat\": 3}")
        # check status code
        self.assertEqual(res.status_code, 201)
        # check the data sent with the status code As the order of the elements in the JSON may be different,
        # we only check that the correct id is return in the whole data
        self.assertIn("id\": 7", str(res.data))

    def test_alreadyExist_create_response(self):
        res = self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                                  "\"True\",\"hat\": 3}")
        # we send it a second time so the app should respond 'user already exists, 400"
        res = self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                                  "\"True\",\"hat\": 3}")
        self.assertEqual(res.status_code, 400)

    def test_NoInput_create_character(self):
        res = self.client.post('/character')
        self.assertEqual(res.status_code, 400)

    def test_Age_Not_create_character(self):
        self.client.delete('/character', data="{\"id\":7}")
        res = self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": -5,\"weight\": 75,\"human\": "
                                                  "\"True\",\"hat\": 3}")
        self.assertIn("age is not correct", str(res.data))

    def test_Not_Human_create_character(self):
        self.client.delete('/character', data="{\"id\":7}")
        res = self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                                  "\"False\",\"hat\": 3}")
        self.assertEqual(res.status_code, 400)
        self.assertIn("can not create the character", str(res.data))

    def test_Not_AgeandWeight_create_character(self):
        self.client.delete('/character', data="{\"id\":7}")
        res = self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 8,\"weight\": 90,\"human\": "
                                                  "\"True\",\"hat\": 3}")
        self.assertEqual(res.status_code, 400)
        self.assertIn("weight is too big for age", str(res.data))

        
    ''' --------------------------------
    Testing the DELETE of the API's character
    --------------------------------------'''

    def test_delete_character(self):
        # With the order of the tests, this character should exist
        # If it doesn't one should make a put request via the API
        self.client.post('/character', data="{\"id\": 7,\"name\": \"moi\",\"age\": 23,\"weight\": 75,\"human\": "
                                            "\"True\",\"hat\": 3}")
        res = self.client.delete('/character', data="{\"id\":7}")
        self.assertEqual(res.status_code, 200)
        self.assertIn("\"User deleted \": 7", str(res.data))

    def test_Missing_delete_character(self):
        # First delete of the character, then another one
        self.client.delete('/character', data="{\"id\":7}")
        res = self.client.delete('/character', data="{\"id\":7}")
        self.assertEqual(res.status_code, 400)

    def test_NoInput_delete_character(self):
        res = self.client.delete('/character')
        self.assertEqual(res.status_code, 400)

    ''' --------------------------------
        Testing the update / PUT of the API's character
        --------------------------------------'''

    def test_update_character(self):
        res = self.client.put('/character', data="{\"id\":1,  \"name\":\"matt\"}")
        self.assertEqual(res.status_code, 201)

    def test_NoInput_update_character(self):
        res = self.client.put('/character', data="{}")
        self.assertEqual(res.status_code, 400)
        self.assertIn('No input data provided', str(res.data))

    def test_NoExist_update_Character(self):
        self.client.delete('/character', data="{\"id\":7}")
        res = self.client.put('/character', data="{\"id\":7,  \"name\":\"matt\"}")
        self.assertEqual(res.status_code, 400)
        self.assertIn('Character does not exist', str(res.data))


if __name__ == "__main__":
    unittest.main()
