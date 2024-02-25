from rest_framework import serializers
from django.contrib.auth.models import User

from structure.models import *
from typing import List, Tuple

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

class BatchMeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ("crop", "datetime", "variable", "value", "type", "statusCode", "timestamp", "data")

    type = serializers.IntegerField()
    statusCode = serializers.IntegerField()
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()

    def create(self, validated_data):
        measurements: List[Measurement] = []
        data = validated_data.get(data, None)

        if data:
            for variable_uiid_key, variable_value in data.items():
                m = Measurement.objects.create(crop     = validated_data["crop"],
                                            datetime = validated_data["timestamp"],
                                            variable = variable_uiid_key, 
                                            value    = variable_value)
                measurements.append(m)
            return measurements
        else:
            return None

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


