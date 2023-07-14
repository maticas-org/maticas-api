from .test_base import *

#==========================================================================
#                        Crop Endpoint Tests
#==========================================================================

class CropEndpointCRUD(CustomBaseTestCase):

    
    def test_crop_creation(self): 

        args1 = {"org": self.org.id,
                 "name": "big data lab", 
                 "coordinate_latitude": 10.3,
                 "coordinate_longitude": 10.3}

        url = reverse("api:crop_create")

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
                                  permission_type = 'add',
                                  granted         = True)

        response = self.client.post( url, data = args1  ) 
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()
    

    def test_crop_detail(self):

        args1 = {'pk': self.crop.id,}
        url = reverse("api:crop_detail", kwargs = args1)

        #request as anonymous user
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as a different user which does not belong to the same org
        self.login_as_other_user()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #request as normal user belonging to the organization
        #which has view permissions over the org
        self.login_as_normal_user()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #request as normal user belonging to the organization
        #which does not have view permissions over the org
        self.login_as_normal_user()
        self.permission2.delete()
        response = self.client.get(url) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()


    def test_crop_modification(self):


        other_user = 0

        args1 = {"pk": str(self.crop.id)}
        args2 = {"org": self.org.id,
                 "name": "big data lab", 
                 "coordinate_latitude": 10.3,
                 "coordinate_longitude": 10.3}

        url = reverse("api:crop_modify", kwargs = args1)

        #try to modify the  as an anonymous user
        response = self.client.put( url, data = args2 ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the org as a user which does not belong to the org
        self.login_as_other_user(other_user)
        response = self.client.put( url, data = args2 ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the crop as a user belonging to the org
        #with no edit permissions
        self.login_as_normal_user()
        response = self.client.put( url, data = args2) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify the org as a user belonging to the org
        #with edit permissions
        self.login_as_normal_user()
        Permission(user            = self.user,
                   org             = self.org,
                   crop            = None,
                   permission_type = 'edit',
                   granted         = True).save()

        response = self.client.put( url, data = args2) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()


    def test_crop_deletion(self):

        #print("DELETEEEEEEEEEE")
        other_user = 0

        args1 = {
            "pk": str(self.crop.id),  # Convert the UUID to a string
        }

        #get the variable, delete it and then check if it still exists
        url = reverse("api:crop_delete", kwargs = args1)

        #try to delete as anonymous user
        response = self.client.delete( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the crop as a user which does not belong to the org
        self.login_as_other_user(other_user)
        response = self.client.delete( url ) 
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete the crop as a user belonging to the org
        #(which does not have delete permission)
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

        response = self.client.delete( url )  
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()

