from rest_framework import serializers
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.utils.timezone import is_aware, make_aware, utc

from structure.models import *
from typing import List, Tuple, Dict

# ===================
# ==== Org related ==
# ===================
class OrgSerializerRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "description")
        model = Org

class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "description", "password")
        model = Org

class OrgSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Org


# ====================
# ==== Crop related ==
# ====================
class CropSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("org", "name", "coordinate_latitude", "coordinate_longitude")
        model = Crop

class CropSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Crop


# =============================
# ==== Actuator_type related ==
# =============================
class Actuator_typeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ( "name", "description",)
        model = Actuator_type

class Actuator_typeSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Actuator_type


# ========================
# ==== Actuator related ==
# ========================
class ActuatorSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name", "mqtt_topic", "crop", "actuator_type", "start_time", "end_time",)
        model = Actuator

class ActuatorSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Actuator


# =========================
# ==== Condition related ==
# =========================
class ConditionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ( "crop", "variable", "min_value", "max_value",)
        model = Condition

class ConditionSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Condition


# ===========================
# ==== Measurement related ==
# ===========================


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("crop", "datetime", "variable", "value",)
        model = Measurement

class MeasurementSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Measurement

class MeasurementBatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ("crop", "datetime", "variable", "value",)

    def to_internal_value(self, data):
        # Copy the incoming data to avoid mutating the original input
        mutable_data = data.copy()
        
        # Extract and parse the datetime field from the input data
        datetime_str = mutable_data.get('datetime', None)
        if datetime_str:
            datetime_obj = parse_datetime(datetime_str)
            
            # Check if the datetime object is timezone aware, make it aware if not
            if datetime_obj and not is_aware(datetime_obj):
                datetime_obj = make_aware(datetime_obj, utc)
            
            # Convert the datetime to UTC if it's not already
            datetime_obj = datetime_obj.astimezone(utc)
            
            # Update the mutable data with the converted datetime
            mutable_data['datetime'] = datetime_obj

        # Proceed with the default processing using the updated data
        return super().to_internal_value(mutable_data)


# ========================
# ==== Variable related ==
# ========================
class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ( "name", "units", "description",)
        model = Variable

class VariableSerializerFullRestricted(serializers.ModelSerializer):
    class Meta:
        fields = ()
        model = Variable


# ====================
# ==== User related ==
# ====================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

# coment


