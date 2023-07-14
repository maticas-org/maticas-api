from .test_base import *

#==========================================================================
#                       Actuator Type Endpoint Tests
#==========================================================================
    
    
class ActuatorTypeEndpointCRUD(CustomBaseTestCase):


    def test_actuator_type_create(self):

        '''
            Test actuator type creation
        '''

        args1 = {"name": "on/off",
                 "description": "Actuators to be controlled only as an on/off element"}

        url = reverse("api:actuatortype_create")

        #try to create an actuator type as a non admin user
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


    def test_actuator_type_detail(self):

        '''
            Test actuator type detail endpoint for different types of user
        '''


        #request the actuator type data
        args1 = {'pk': self.actuator_type.id,}
        url =  reverse("api:actuatortype_detail", kwargs = args1)  
        
        #request as anonymous user
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login_as_normal_user()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_actuator_type_modification(self):

        '''
            Test modifiying an actuator type
        '''

        args1 = {"pk": str(self.actuator_type.id),}
        args2 = {"name": "on/off",
                 "description": "Actuators to be controlled only as an on/off element"}

        url = reverse("api:actuatortype_modify", kwargs = args1)

        #try to modify the actuator type as an anonimous user
        response = self.client.get( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the actuator type as a logged in user
        self.login_as_normal_user()
        response = self.client.get( url )  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the actuator type as an admin user
        self.login_as_admin()
        response = self.client.get( url )  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        prev = Variable.objects.all()
        response = self.client.put( url, data = args2 ) 
        after = Variable.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(prev, after)

        self.client.logout()

    def test_actuator_type_deletion(self):

        '''
            Test deleting an actuator type
        '''

        args1 = {
            "pk": str(self.actuator_type.id),  # Convert the UUID to a string
        }

        #try to delete the actuator_type as an anonymous user
        url = reverse("api:actuatortype_delete", kwargs = args1)

        response = self.client.delete( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the actuator_type as a logged in user
        self.login_as_normal_user()
        response = self.client.delete( url )  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the actuator_type as an admin user
        self.login_as_admin()

        #modify the variable and check the before and after
        prev = Variable.objects.all()
        response = self.client.delete( url )  
        after = Variable.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNot(prev, after)

        self.client.logout()

