import random 
import string

from django.urls           import reverse
from rest_framework        import status
from rest_framework.test   import APITestCase
from django.utils          import timezone

from structure.models import *
random.seed(69)


def generate_text(lenght = 10):
    return ''.join(random.choices(string.ascii_lowercase, k=lenght))


class CustomBaseTestCase(APITestCase):

    def setUp(self):
        self.user_password = 'testpassword'
        self.admin_password = 'adminpassword'
        self.org_password = 'testpassword'

        self.admin_user = self.create_superuser('admin', 'admin@example.com', self.admin_password)
        self.user = self.create_user('testuser', 'testuser@example.com', self.user_password)
        self.org = self.create_org('Test Organization', 'Test organization description', self.org_password)
        self.crop = self.create_crop(self.org, 'Test Crop', 10.12345, 20.54321)
        self.variable = self.create_variable('Test Variable', 'Test Units', 'Test variable description')
        self.condition = self.create_condition(self.crop, self.variable, 0, 100)
        self.actuator_type = self.create_actuator_type('Test Actuator Type', 'Test actuator type description')
        self.actuator = self.create_actuator('Test Actuator', 'test/topic', self.crop, self.actuator_type)
        self.measurement1 = self.create_measurement(self.crop, '2023-05-28T10:00:00Z', 50, self.variable)
        self.measurement2 = self.create_measurement(self.crop, '2023-05-28T10:01:00Z', 51, self.variable)
        self.measurement3 = self.create_measurement(self.crop, '2023-05-28T10:02:00Z', 51, self.variable)
        self.permission1 = self.create_permission(self.user, self.org, self.crop, 'view', True)
        self.permission2 = self.create_permission(self.user, self.org, None, 'view', True)

        self.create_some_data()

    def create_superuser(self, username, email, password):
        return User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )

    def create_user(self, username, email, password):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

    def create_org(self, name, description, password):
        return Org.objects.create(
            name=name,
            description=description,
            password=password
        )

    def create_crop(self, org, name, latitude, longitude):
        return Crop.objects.create(
            org=org,
            name=name,
            coordinate_latitude=latitude,
            coordinate_longitude=longitude
        )

    def create_variable(self, name, units, description):
        return Variable.objects.create(
            name=name,
            units=units,
            description=description
        )

    def create_condition(self, crop, variable, min_value, max_value):
        return Condition.objects.create(
            crop=crop,
            variable=variable,
            min_value=min_value,
            max_value=max_value
        )

    def create_actuator_type(self, name, description):
        return Actuator_type.objects.create(
            name=name,
            description=description
        )

    def create_actuator(self, name, mqtt_topic, crop, actuator_type):
        return Actuator.objects.create(
            name=name,
            mqtt_topic=mqtt_topic,
            crop=crop,
            actuator_type=actuator_type
        )

    def create_measurement(self, crop, datetime, value, variable):
        return Measurement.objects.create(
            crop=crop,
            datetime=datetime,
            value=value,
            variable=variable
        )

    def create_permission(self, user, org, crop, permission_type, granted):
        return Permission.objects.create(
            user=user,
            org=org,
            crop=crop,
            permission_type=permission_type,
            granted=granted
        )

    def create_some_data(self, ndata=2):
        self.data = {}
        for i in range(ndata):
            txt = generate_text()
            gen = {}
            gen["user"] = self.create_user(txt, txt + '@example.com', txt)
            gen["org"] = self.create_org(txt, txt, txt)
            gen["crop"] = self.create_crop(gen["org"], txt, 10.12345, 20.54321)
            gen["variable"] = self.create_variable(txt, txt, txt)
            gen["condition"] = self.create_condition(gen["crop"], gen["variable"], 0, 100)
            gen["actuator_type"] = self.create_actuator_type(txt, txt)
            gen["actuator"] = self.create_actuator(txt, txt, gen["crop"], gen["actuator_type"])
            gen["measurement"] = self.create_measurement(gen["crop"], '2023-05-28 10:00:00', 50, gen["variable"])
            gen["permission"] = self.create_permission(gen["user"], gen["org"], gen["crop"], 'edit', True)
            self.data[i] = gen

    def login_as_normal_user(self):
        self.client.logout()
        self.client.login(username=self.user.username, password=self.user_password)

    def login_as_admin(self):
        self.client.logout()
        self.client.login(username=self.admin_user.username, password=self.admin_password)

    def login_as_other_user(self, user_num=0):
        self.client.logout()
        self.client.force_login(user=self.data[user_num]["user"])

