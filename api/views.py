from rest_framework import generics
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from structure.models import *

from .serializers import *


# ===================
# ==== Org related ==
# ===================
class OrgAPICreate(generics.CreateAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer

class OrgAPIDetail(generics.RetrieveAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializerRestricted

class OrgAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializer

class OrgAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Org.objects.all()
    serializer_class = OrgSerializerFullRestricted


# ====================
# ==== Crop related ==
# ====================
class CropAPICreate(generics.CreateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class CropAPIDetail(generics.RetrieveAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class CropAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

class CropAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Crop.objects.all()
    serializer_class = CropSerializerFullRestricted


# =============================
# ==== Actuator_type related ==
# =============================
class Actuator_typeAPICreate(generics.CreateAPIView):
    queryset = Actuator_type.objects.all()
    serializer_class = Actuator_typeSerializer

class Actuator_typeAPIDetail(generics.RetrieveAPIView):
    queryset = Actuator_type.objects.all()
    serializer_class = Actuator_typeSerializer

class Actuator_typeAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Actuator_type.objects.all()
    serializer_class = Actuator_typeSerializer

class Actuator_typeAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Actuator_type.objects.all()
    serializer_class = Actuator_typeSerializerFullRestricted


# ========================
# ==== Actuator related ==
# ========================
class ActuatorAPICreate(generics.CreateAPIView):
    queryset = Actuator.objects.all()
    serializer_class = ActuatorSerializer

class ActuatorAPIDetail(generics.RetrieveAPIView):
    queryset = Actuator.objects.all()
    serializer_class = ActuatorSerializer

class ActuatorAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Actuator.objects.all()
    serializer_class = ActuatorSerializer

class ActuatorAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Actuator.objects.all()
    serializer_class = ActuatorSerializerFullRestricted


# =========================
# ==== Condition related ==
# =========================
class ConditionAPICreate(generics.CreateAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

class ConditionAPIDetail(generics.RetrieveAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

class ConditionAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializer

class ConditionAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Condition.objects.all()
    serializer_class = ConditionSerializerFullRestricted


# ===========================
# ==== Measurement related ==
# ===========================
class MeasurementAPICreate(generics.CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class MeasurementAPIDetail(generics.RetrieveAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class MeasurementAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class MeasurementAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializerFullRestricted


# ========================
# ==== Variable related ==
# ========================
class VariableAPICreate(generics.CreateAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer

class VariableAPIDetail(generics.RetrieveAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer

class VariableAPIDetailModify(generics.RetrieveUpdateAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializer

class VariableAPIDetailDelete(generics.RetrieveDestroyAPIView):
    queryset = Variable.objects.all()
    serializer_class = VariableSerializerFullRestricted


# ====================
# ==== User related ==
# ====================
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'detail': 'Logged in successfully.'})
            else:
                print(f"{user}:{email}:{password}")
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
