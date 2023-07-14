from .test_base import *


#==========================================================================
#                        Organization Endpoint Tests
#==========================================================================

class OrganizationEndpointCRUD(CustomBaseTestCase):

    
    def test_org_creation(self):

        args1 = {"name": "maticas",
                 "description": "maticas is building the future of agriculture today.", 
                 "password": "maticas"}

        print("Creation function")
        url = reverse("api:org_create")

        #try to create as a anonymous user
        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #simulate a org user is connected 
        #notice that user already has an org he belongs to
        self.login_as_normal_user()

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create with a brand new user, which does not 
        #belong to other org
        user = self.create_user('brand new user', 'newuser2@gmail.com', 'password')
        self.client.logout()
        self.client.force_login(user = user)

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.client.logout()

    def test_org_detail(self):

        args1 = {'pk': self.org.id,}
        url = reverse("api:org_detail", kwargs = args1)
        
        #print("DEEEETAIL")

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
        self.client.logout()

    def test_org_modification(self):

        '''
            Test modifiying an actuator type
        '''

        other_user = 0

        #print("MODIFYYYYYY")
        args1 = {"pk": str(self.org.id)}
        args2 = {"name": "super crazy org",
                 "description": "super duper crazy org",
                 "password": self.org_password}

        url = reverse("api:org_modify", kwargs = args1)

        #try to get the variable as an anonymous user
        response = self.client.put( url, data = args2 ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the org as a user which does not belong to the org
        self.login_as_other_user(other_user)
        response = self.client.put( url, data = args2 ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the org as a user belonging to the org
        #which does not have 'edit' permissions
        self.login_as_normal_user()

        response = self.client.put( url, data = args2 ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try with the 'edit' permissions added 
        self.create_permission(self.user, self.org, None, 'edit', True)
        response = self.client.put( url, data = args2 ) 

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()


    def test_org_deletion(self):

        '''
            Test deleting an actuator type
        '''

        other_user = 0

        args1 = {
            "pk": str(self.org.id),  # Convert the UUID to a string
        }

        #get the variable, delete it and then check if it still exists
        url = reverse("api:org_delete", kwargs = args1)

        #try to delete as anonymous user
        response = self.client.delete( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the org as a user which does not belong to the org
        self.login_as_other_user(other_user)
        response = self.client.delete( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the org as a normal user (which does not have delete permission)
        self.login_as_normal_user()
        response = self.client.delete( url )  
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the org as a normal user (with delete permission)
        self.login_as_normal_user()
        Permission.objects.create(
            user            = self.user,
            org             = self.org,
            permission_type = 'delete',
            granted         = True
        )

        prev = Org.objects.all()
        response = self.client.delete( url )  
        after = Org.objects.all()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNot(prev, after)

        self.client.logout()

