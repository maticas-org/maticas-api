from django.test import TestCase
from django.contrib.auth.models import User
from .models import *


class ModelTestCase(TestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

        # Create a test organization
        self.org = Org.objects.create(
            name='Test Organization',
            description='Test organization description',
            password='testpassword'
        )

        # Create a test crop
        self.crop = Crop.objects.create(
            org=self.org,
            name='Test Crop',
            coordinate_latitude=10.12345,
            coordinate_longitude=20.54321
        )

        # Create a test variable
        self.variable = Variable.objects.create(
            name='Test Variable',
            units='Test Units',
            description='Test variable description'
        )

        # Create a test condition
        self.condition = Condition.objects.create(
            crop=self.crop,
            variable=self.variable,
            min_value=0,
            max_value=100
        )

        # Create a test actuator type
        self.actuator_type = Actuator_type.objects.create(
            name='Test Actuator Type',
            description='Test actuator type description'
        )

        # Create a test actuator
        self.actuator = Actuator.objects.create(
            name='Test Actuator',
            mqtt_topic='test/topic',
            crop=self.crop,
            actuator_type=self.actuator_type
        )

        # Create a test measurement
        self.measurement = Measurement.objects.create(
            crop=self.crop,
            datetime='2023-05-28 10:00:00',
            value=50,
            variable=self.variable
        )

        # Create a test permission
        self.permission = Permission.objects.create(
            user=self.user,
            org=self.org,
            crop=self.crop,
            permission_type='edit',
            granted=True
        )


    def test_org_model(self):
        """
            Tests if the organization has been saved and the __str__ overload is working
        """
        org = Org.objects.get(name='Test Organization')
        self.assertEqual(str(org), f"{org.id}.{org.name}")

    def test_crop_model(self):

        """
            Tests if the crop has been saved and the __str__ overload is working
        """
        crop = Crop.objects.get(name='Test Crop')
        self.assertEqual(str(crop), crop.name)


    def test_variable_model(self):

        """
            Tests if the variable has been saved and the __str__ overload is working
        """
        variable = Variable.objects.get(name='Test Variable')
        self.assertEqual(str(variable), f"{variable.name}.{variable.units}")

    def test_condition_model(self):

        """
            Tests if the condition has been saved and the __str__ overload is working
        """
        condition = Condition.objects.get(crop=self.crop, variable=self.variable)
        self.assertEqual(
            str(condition),
            f"{condition.variable}.{condition.min_value}.{condition.max_value}"
        )

    def test_actuator_type_model(self):
        """
            Tests if the actuator_type has been saved and the __str__ overload is working
        """
        actuator_type = Actuator_type.objects.get(name='Test Actuator Type')
        self.assertEqual(str(actuator_type), actuator_type.name)

    def test_actuator_model(self):

        """
            Tests if the actuator has been saved and the __str__ overload is working
        """
        actuator = Actuator.objects.get(name='Test Actuator')
        self.assertEqual(
            str(actuator),
            f"{actuator.name}.{actuator.mqtt_topic}"
        )

    def test_measurement_model(self):

        """
            Tests if the actuator has been saved and the __str__ overload is working
        """
        measurement = Measurement.objects.get(value=50)
        self.assertEqual(
            str(measurement),
            f"{measurement.value}.{measurement.variable}.{measurement.crop}"
        )

    def test_permission_model(self):

        """
            Tests if the permission has been saved and the __str__ overload is working
        """
        permission = Permission.objects.get(permission_type='edit')
        self.assertEqual(
            str(permission),
            f"{permission.user.username} has {permission.permission_type} permission for {permission.org.name}"
        )

