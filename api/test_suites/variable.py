from .test_base import *


#==========================================================================
#                       Variable Endpoint Tests
#==========================================================================

class VariableEndpointCRUD(CustomBaseTestCase):


    def test_variable_create(self):

        '''
            Test variable creation
        '''

        
        args1 = {"name": "Ambient Temperature",
                 "units": "°C",
                 "description": "Temperature of the air in celcius degrees"}

        url = reverse("api:variable_create")

        #try to create a variable as a non admin user
        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #simulate the client is now logged in
        self.login_as_normal_user()

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try as admin user
        self.login_as_admin()
        
        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()

    def test_variable_detail(self):

        '''
            Test reading an ambient variable, if an anonimous user can read anyother user can, and that's the idea
        '''


        #request the first variable from the existing ones
        args1 = {'pk': self.variable.id,}
        url =  reverse("api:variable_detail", kwargs = args1)  
        
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login_as_admin()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_variable_modification(self):

        '''
            Test modifiying an ambient variable
        '''

        args1 = {
            "pk": str(self.variable.id),  # Convert the UUID to a string
        }

        args2 = {"name": "Ambient Temperature",
                 "units": "°C",
                 "description": "Temperature of the air in Celsius degrees"}

        url = reverse("api:variable_modify", kwargs = args1)

        #try to get the variable as an anonimous user
        response = self.client.get( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #simulate logging in as a normal user 
        self.login_as_normal_user()

        #try to get the variable as a normal user
        response = self.client.get( url )  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to get the variable as a admin user
        self.login_as_admin()
        response = self.client.get( url )  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #modify the variable and check the before and after
        prev = Variable.objects.all()
        response = self.client.put( url, data = args2 ) 
        after = Variable.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(prev, after)


        self.client.logout()
    

    def test_variable_deletion(self):

        '''
            Test deleting an ambient variable, 
        '''

        args1 = {
            "pk": str(self.variable.id),  # Convert the UUID to a string
        }

        #get the variable, delete it and then check if it still exists
        url = reverse("api:variable_delete", kwargs = args1)

        #try to delete as anonimous user
        response = self.client.delete( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #simulate logging in as a normal user 
        self.login_as_normal_user()

        #try to get the variable as a normal user
        response = self.client.delete( url )  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #logs out from being a normal user and comes back as admin 
        self.login_as_admin()

        #modify the variable and check the before and after
        prev = Variable.objects.all()
        response = self.client.delete( url )  
        after = Variable.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNot(prev, after)

        self.client.logout()

