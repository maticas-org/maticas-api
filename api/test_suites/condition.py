from .test_base import *

#==============================================================================
#                           Condition Endpoint Tests
#==============================================================================

class ConditionEndpointCRUD(CustomBaseTestCase):


    def test_create_condition(self):

        print("Testing Condition Creation")
        args1 = {"crop": self.crop.id,
                "variable": self.variable.id,
                "min_value": 1,
                "max_value": 10.3}

        url = reverse("api:condition_create")

        #try to create as a anonymous user
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create as a user from another org
        self.login_as_other_user()
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create a crop as a user with out add permissions over the org
        self.login_as_normal_user()
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #allow the user to add things to the org
        Permission.objects.create(user            = self.user,
                                  org             = self.org,
                                  crop            = self.crop,
                                  permission_type = 'add',
                                  granted         = True)
        
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()


    def test_condition_detail(self):
            
            print("Testing Condition Detail")
            args1 = {'pk': self.condition.id,}
            url = reverse("api:condition_detail", kwargs = args1)
    
            #request as anonymous user
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
            #request as a different user which does not belong to the same org
            self.login_as_other_user()
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
            #request as normal user belonging to the organization
            #which has view permissions over the crop
            self.login_as_normal_user()
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
    
            #request as normal user belonging to the organization
            #which does not have view permissions over the crop
            self.login_as_normal_user()
            self.permission1.delete()
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
            self.client.logout()

    def test_condition_modify(self):

        print("Testing Condition Modify")
        args1 = {'pk': self.condition.id,}
        url = reverse("api:condition_modify", kwargs = args1)

        args2 = {"crop": self.crop.id,
                "variable": self.variable.id,
                "min_value": 1,
                "max_value": 10.3}

        #request as anonymous user
        response = self.client.put(url, data = args2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as a different user which does not belong to the same org
        self.login_as_other_user()
        response = self.client.put(url, data = args2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as normal user belonging to the organization
        #which does not have edit permissions over the crop
        self.login_as_normal_user()
        response = self.client.put(url, data = args2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as normal user belonging to the organization
        #which has edit permissions over the crop
        self.login_as_normal_user()
        self.create_permission(self.user, self.org, self.crop, 'edit', True)
        response = self.client.put(url, data = args2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.logout()
        

    def test_condition_deletion(self):

        print("Testing Condition Deletion")
        args1 = {'pk': self.condition.id,}
        url = reverse("api:condition_delete", kwargs = args1)

        #request as anonymous user
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as a different user which does not belong to the same org
        self.login_as_other_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as normal user belonging to the organization
        #which does not have delete permissions over the crop
        self.login_as_normal_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as normal user belonging to the organization
        #which has delete permissions over the crop
        self.login_as_normal_user()
        self.create_permission(self.user, self.org, self.crop, 'delete', True)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.client.logout()



