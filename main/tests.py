from rest_framework.test import APITestCase
from .models import Post
from datetime import datetime,date,timedelta
from django.test.client import Client

class PostTests(APITestCase):
    def setUp(self):
        self.login_data =  {
            "username": "string",
            "email": "user@example.com",
            "password": "string@123"
            }
  
        self.logged_client = Client()
        self.userid = self.logged_client.post("/register/", self.login_data).json()['id']

        auth_vals = self.logged_client.post('/authenticate/', self.login_data).json()['access']
        self.header = {
            'accept': 'application/json', 
            'Authorization': f'Bearer {auth_vals}' 
        }

    def test_post_creation_success(self):
        data = {
            "title": "string",
            "desc": "string"
            }
        response = self.client.post(f'/posts/', data=data, headers=self.header)
        self.assertEqual(response.status_code, 201)

        # check if post is created in database
        post_obj = Post.objects.get(user=self.userid)
        self.assertEqual(post_obj.id, response.json()['id'])

    
    def test_post_creation_faliure(self):
        data = {
            "desc": "string"
            }
        response = self.client.post(f'/posts/', data=data,headers= self.header)
        self.assertEqual(response.status_code, 400)

#./manage.py test --verbosity=2 --keepdb