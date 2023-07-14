from .test_base import *

class UserCreationLogin(CustomBaseTestCase):

    def test_user_login(self):

        #try with an existing user and right credentials
        args1 = {"username": self.user.username,
                 "password": self.user_password}

        url = reverse("api:user_login")

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #try with an existing user and wrong credentials
        args1 = {"username": self.user.username,
                 "password": 'any wrong password'}

        url = reverse("api:user_login")

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        #try with an unexistent user
        args2 = {"username": "nonExistentUserName",
                 "password": "nonExistentPassword"}

        response = self.client.post( url, data = args2  ) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):

        '''
            Test the user creation endpoint
        '''

        args1 = {"username":    "NewUser2",
                 "password":    "New User 2 Password",
                 "email":       "Newuser2@email.com",}
        url = reverse("api:user_create")

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

