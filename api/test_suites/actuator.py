from .test_base import *

#==========================================================================
#                        Actuator Endpoint Tests
#==========================================================================


class ActuatorEndpointCRUD(CustomBaseTestCase):

    def test_actuator_creation(self):

        print("Testing actuator creation...")

        url = reverse("api:actuator_create")
        args1 = {"name": "actuator1",
                 "mqtt_topic": "actuator1",
                 "crop": self.crop.id,
                 "actuator_type": self.actuator_type.id,
                 "start_time": '00:00:00',
                 "end_time": '23:59:59'}

        #try to create an actuator as an anonymous user
        response = self.client.post(url, args1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


        #try to create an actuator as a user from another org
        self.login_as_other_user()
        response = self.client.post(url, args1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create an actuator as a normal user
        #which only has view permission on the crop
        self.login_as_normal_user()
        response = self.client.post(url, args1)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to create an actuator as a normal user
        #which has add permission on the crop
        self.login_as_normal_user()
        self.create_permission(self.user, self.org, self.crop, 'add', True)
        response = self.client.post(url, args1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.client.logout()


    def test_actuator_detail(self):

        print("Testing actuator detail...")
        args1 = {"pk": self.actuator.id}
        url = reverse("api:actuator_detail", kwargs = args1)

        #try to get an actuator as an anonymous user
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to get an actuator as a user from another org
        self.login_as_other_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to get an actuator as a normal user
        #which has view permission on the crop
        self.login_as_normal_user()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        #try to get an actuator as a normal user
        #which only has view permission on the crop
        self.login_as_normal_user()
        self.permission1.delete()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.client.logout()


    def test_actuator_modification(self):

        print("Testing actuator modification...")
        args1 = {"pk": self.actuator.id}
        args2 = {"name": "actuator1",
                 "mqtt_topic": "actuator1",
                 "crop": self.crop.id,
                 "actuator_type": self.actuator_type.id,
                 "start_time": '00:00:00',
                 "end_time": '23:59:59'}

        url = reverse("api:actuator_modify", kwargs = args1)

        #try to modify an actuator as an anonymous user
        response = self.client.put(url, args2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify an actuator as a user from another org
        self.login_as_other_user()
        response = self.client.put(url, args2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify an actuator as a normal user
        #which has view permission on the crop
        self.login_as_normal_user()
        response = self.client.put(url, args2)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to modify an actuator as a normal user
        #which has edit permission on the crop
        self.login_as_normal_user()
        self.create_permission(self.user, self.org, self.crop, 'edit', True)

        response = self.client.put(url, args2)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.logout()

    def test_actuator_deletion(self):

        print("Testing actuator deletion...")
        args1 = {"pk": self.actuator.id}

        url = reverse("api:actuator_delete", kwargs = args1)

        #try to delete an actuator as an anonymous user
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete an actuator as a user from another org
        self.login_as_other_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete an actuator as a normal user
        #which does not have delete permission on the crop
        self.login_as_normal_user()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        #try to delete an actuator as a normal user
        #which has delete permission on the crop
        self.login_as_normal_user()
        self.create_permission(self.user, self.org, self.crop, 'delete', True)
        
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.client.logout()



