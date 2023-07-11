import random 
import string

from django.urls            import reverse
from rest_framework         import status
from rest_framework.test    import APITestCase

from structure.models import *
random.seed(69)




def generate_text(lenght = 10):

    return ''.join(random.choices(string.ascii_lowercase, k=lenght))


#class to avoid repeating my self so much 
class CustomBaseTestCase(APITestCase):

    def setUp(self):

        self.user_password = 'testpassword'
        self.admin_password = 'adminpassword'

        # Create admin user
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            username    = 'admin',
            email       = 'admin@example.com',
            password    = self.admin_password,
        )


        # Create a test user
        self.user = User.objects.create_user(
            username    = 'testuser',
            email       = 'testuser@example.com',
            password    = self.user_password
        )

        # Create a test organization
        self.org = Org.objects.create(
            name        = 'Test Organization',
            description = 'Test organization description',
            password    = 'testpassword'
        )

        # Create a test crop
        self.crop = Crop.objects.create(
            org                  = self.org,
            name                 = 'Test Crop',
            coordinate_latitude  = 10.12345,
            coordinate_longitude = 20.54321
        )

        # Create a test variable
        self.variable = Variable.objects.create(
            name        = 'Test Variable',
            units       = 'Test Units',
            description = 'Test variable description'
        )

        # Create a test condition
        self.condition = Condition.objects.create(
            crop        = self.crop,
            variable    = self.variable,
            min_value   = 0,
            max_value   = 100
        )

        # Create a test actuator type
        self.actuator_type = Actuator_type.objects.create(
            name        = 'Test Actuator Type',
            description = 'Test actuator type description'
        )

        # Create a test actuator
        self.actuator = Actuator.objects.create(
            name            = 'Test Actuator',
            mqtt_topic      = 'test/topic',
            crop            = self.crop,
            actuator_type   = self.actuator_type
        )

        # Create a test measurement
        self.measurement = Measurement.objects.create(
            crop        = self.crop,
            datetime    = '2023-05-28 10:00:00',
            value       = 50,
            variable    = self.variable
        )

        # Create a test permission
        self.permission = Permission.objects.create(
            user            = self.user,
            org             = self.org,
            crop            = self.crop,
            permission_type = 'edit',
            granted         = True
        )

        # Create a test permission
        Permission.objects.create(
            user            = self.user,
            org             = self.org,
            permission_type = 'edit',
            granted         = True
        )


        self.create_some_data()

    def login_as_normal_user(self):

        self.client.logout()
        self.client.force_login(user = self.user)


    def login_as_admin(self):

        self.client.logout()
        self.client.login(username = self.admin_user.username, password = self.admin_password)

    def login_as_other_user(self):

        self.client.logout()
        self.client.force_login(user = self.data[0]["user"])
        



    def create_some_data(self, ndata = 1):

        self.data = {}

        for i in range(ndata):

            txt = generate_text()
            gen = {}

            # Create a test user
            gen["user"] = User.objects.create_user(
                username    = txt,
                email       = txt + '@example.com',
                password    = txt
            )

            # Create a test organization
            gen["org"] = Org.objects.create(
                name        = txt,
                description = txt,
                password    = txt
            )

            # Create a test crop
            gen["crop"] = Crop.objects.create(
                org                  = gen["org"],
                name                 = txt,
                coordinate_latitude  = 10.12345,
                coordinate_longitude = 20.54321
            )

            # Create a test variable
            gen["variable"] = Variable.objects.create(
                name        = txt,
                units       = txt,
                description = txt
            )

            # Create a test condition
            gen["condition"] = Condition.objects.create(
                crop        = gen["crop"],
                variable    = gen["variable"],
                min_value   = 0,
                max_value   = 100
            )

            # Create a test actuator type
            gen["actuator_type"] = Actuator_type.objects.create(
                name        = txt,
                description = txt
            )

            # Create a test actuator
            gen["actuator"] = Actuator.objects.create(
                name            = txt,
                mqtt_topic      = txt,
                crop            = gen["crop"],
                actuator_type   = gen["actuator_type"]
            )

            # Create a test measurement
            gen["measurement"] = Measurement.objects.create(
                crop        = gen["crop"],
                datetime    = '2023-05-28 10:00:00',
                value       = 50,
                variable    = gen["variable"]
            )

            # Create a test permission
            gen["permission"] = Permission.objects.create(
                user            = gen["user"],
                org             = gen["org"],
                crop            = gen["crop"],
                permission_type = 'edit',
                granted         = True
            )

            self.data[i] = gen

#==========================================================================
#                       User Endpoint Tests
#==========================================================================

class UserCreationLoginAuth(CustomBaseTestCase):

    def test_user_login(self):

        """ 
            Test if log in endpoint works okey for a created user, and if
            returns 401 if the user never has been created.
        """


        args1 = {"username": self.user.username,
                 "password": self.user_password}

        url = reverse("api:user_login")

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        args2 = {"username": "nonExistentUserName",
                 "password": "nonExistentPassword"}

        response = self.client.post( url, data = args2  ) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_create(self):

        """
            Test the user creation endpoint
        """

        args1 = {"username":    "NewUser2",
                 "password":    "New User 2 Password",
                 "email":       "Newuser2@email.com",}
        url = reverse("api:user_create")

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


#==========================================================================
#                       Variable Endpoint Tests
#==========================================================================

class VariableEndpointCRUD(CustomBaseTestCase):


    def test_variable_create(self):

        """
            Test variable creation
        """

        
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

        """
            Test reading an ambient variable, if an anonimous user can read anyother user can, and that's the idea
        """


        #request the first variable from the existing ones
        args1 = {'pk': self.variable.id,}
        url =  reverse("api:variable_detail", kwargs = args1)  
        
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login_as_admin()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_variable_modification(self):

        """
            Test modifiying an ambient variable
        """

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

        """
            Test deleting an ambient variable, 
        """

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
    

#==========================================================================
#                       Actuator Type Endpoint Tests
#==========================================================================
    
    
class ActuatorTypeEndpointCRUD(CustomBaseTestCase):


    def test_actuator_type_create(self):

        """
            Test actuator type creation
        """

        args1 = {"name": "on/off",
                 "description": "Actuators to be controlled only as an on/off element"}

        url = reverse("api:actuatortype_create")

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


    def test_actuator_type_detail(self):

        """
            Test actuator type detail endpoint for different types of user
        """


        #request the first variable from the existing ones
        args1 = {'pk': self.actuator_type.id,}
        url =  reverse("api:actuatortype_detail", kwargs = args1)  
        
        #request as anonymous user
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login_as_normal_user()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_actuator_type_modification(self):

        """
            Test modifiying an actuator type
        """

        args1 = {"pk": str(self.actuator_type.id),}
        args2 = {"name": "on/off",
                 "description": "Actuators to be controlled only as an on/off element"}

        url = reverse("api:actuatortype_modify", kwargs = args1)

        #try to get the variable as an anonimous user
        response = self.client.get( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login_as_normal_user()
        response = self.client.get( url )  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.login_as_admin()
        response = self.client.get( url )  
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        prev = Variable.objects.all()
        response = self.client.put( url, data = args2 ) 
        after = Variable.objects.all()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNot(prev, after)

        self.client.logout()



    def test_variable_deletion(self):

        """
            Test deleting an actuator type
        """

        args1 = {
            "pk": str(self.actuator_type.id),  # Convert the UUID to a string
        }

        #get the variable, delete it and then check if it still exists
        url = reverse("api:actuatortype_delete", kwargs = args1)

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

#==========================================================================
#                        Organization Endpoint Tests
#==========================================================================

class OrganizationEndpointCRUD(CustomBaseTestCase):

    
    def test_org_creation(self):

        args1 = {"name": "maticas",
                 "description": "maticas is building the future of agriculture today.", 
                 "password": "maticas"}

        url = reverse("api:org_create")

        #try to create as a anonymous user
        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #simulate the client is now logged in
        self.login_as_normal_user()

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_org_detail(self):

        args1 = {'pk': self.org.id,}
        url = reverse("api:org_detail", kwargs = args1)

        #request as anonymous user
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as normal user belonging to the organization
        self.login_as_normal_user()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #request as a different user which does not belong to the same org
        self.login_as_other_user()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        






