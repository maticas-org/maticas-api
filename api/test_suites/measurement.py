
from .test_base import *

#==========================================================================
#                        Measurement Endpoint Tests
#==========================================================================

class MeasurementEndpointCRUD(CustomBaseTestCase):

    def test_measurement_creation(self):

        print("Testing measurement creation")

        args1 = {"crop": self.crop.id,
                 "datetime": "2025-01-01T00:00:00Z",
                 "variable": self.variable.id,
                 "value": 10.3}

        url = reverse("api:measurement_create")

        #try to create as a anonymous user
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create as a user from another org
        self.login_as_other_user()
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create a measurement as a user with out add permissions over the
        #crop which the measurement belongs to
        self.login_as_normal_user()
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #allow the user to add things to the crop
        Permission.objects.create(user            = self.user,
                                    org             = self.org,
                                    crop            = self.crop,
                                    permission_type = 'add',
                                    granted         = True)
        response = self.client.post( url, data = args1  )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()

    def test_measurement_detail(self):

        print("Testing measurement detail")

        args1 = {'pk': self.measurement.id,}
        url = reverse("api:measurement_detail", kwargs = args1)

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
        #which has no view permissions over the crop
        self.login_as_normal_user()
        self.permission1.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        self.client.logout()


    def test_measurement_modication(self):

        print("Testing measurement modification")
        args1 = {'pk': self.measurement.id,}
        args2 = {"crop": self.crop.id,
                 "datetime": "2025-01-01T00:00:00Z",
                 "variable": self.variable.id,
                 "value": 10.3}

        url = reverse("api:measurement_modify", kwargs = args1)

        #try to modify as a anonymous user
        response = self.client.put( url, data = args2  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify as a user from another org
        self.login_as_other_user()
        response = self.client.put( url, data = args2  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify a measurement as a user with out edit permissions over the
        #crop which the measurement belongs to
        self.login_as_normal_user()
        self.permission1.delete()
        response = self.client.put( url, data = args2  )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #allow the user to edit things to the crop
        Permission.objects.create(user            = self.user,
                                  org             = self.org,
                                  crop            = self.crop,
                                  permission_type = 'edit',
                                  granted         = True)

        response = self.client.put( url, data = args2  )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_measurement_deletion(self):

        print("Testing measurement deletion")
        args1 = {'pk': self.measurement.id,}
        url = reverse("api:measurement_delete", kwargs = args1)

        #try to delete as a anonymous user
        response = self.client.delete( url )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)   

        #try to delete as a user from another org
        self.login_as_other_user()
        response = self.client.delete( url )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete a measurement as a user with out delete permissions over the
        #crop which the measurement belongs to
        self.login_as_normal_user()
        response = self.client.delete( url )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #allow the user to delete things to the crop
        Permission.objects.create(user            = self.user,
                                  org             = self.org,
                                  crop            = self.crop,
                                  permission_type = 'delete',
                                  granted         = True)
        response = self.client.delete( url )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()
