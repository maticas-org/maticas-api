from rest_framework import generics
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.authtoken.models import Token #ADDED
from rest_framework.authentication import TokenAuthentication, SessionAuthentication #ADDED
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from .serializers import *
from .permissions import *
from structure.models import *

# ===================
# ==== Org related ==
# ===================
class OrgAPICreate(generics.CreateAPIView):
    permission_classes  = (OrgPermission,)
    queryset         = Org.objects.all()
    serializer_class = OrgSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            org_instance = serializer.save()

            #the creator of the org gets assign permissions
            Permission.objects.create(user = request.user,
                                      org = org_instance,
                                      permission_type = 'assign',
                                      granted = True)


            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrgAPIDetail(generics.RetrieveAPIView):
    permission_classes  = (OrgPermission,)
    queryset            = Org.objects.all()
    serializer_class    = OrgSerializerRestricted

class OrgAPIDetailModify(generics.RetrieveUpdateAPIView):
    permission_classes  = (OrgPermission,)
    queryset            = Org.objects.all()
    serializer_class    = OrgSerializer

class OrgAPIDetailDelete(generics.RetrieveDestroyAPIView):
    permission_classes  = (OrgPermission,)
    queryset            = Org.objects.all()
    serializer_class    = OrgSerializerFullRestricted


# ====================
# ==== Crop related ==
# ====================
class CropAPICreate(generics.CreateAPIView):
    permission_classes  = (CropPermission,)
    queryset         = Crop.objects.all()
    serializer_class = CropSerializer

class CropAPIDetail(generics.RetrieveAPIView):
    permission_classes  = (CropPermission,)
    queryset            = Crop.objects.all()
    serializer_class    = CropSerializer

class CropAPIDetailModify(generics.RetrieveUpdateAPIView):
    permission_classes  = (CropPermission,)
    queryset            = Crop.objects.all()
    serializer_class    = CropSerializer

class CropAPIDetailDelete(generics.RetrieveDestroyAPIView):
    permission_classes  = (CropPermission,)
    queryset            = Crop.objects.all()
    serializer_class    = CropSerializerFullRestricted


# =============================
# ==== Actuator_type related ==
# =============================
class Actuator_typeAPICreate(generics.CreateAPIView):

    permission_classes  = (IsAdminUser,)
    queryset            = Actuator_type.objects.all()
    serializer_class    = Actuator_typeSerializer

class Actuator_typeAPIDetail(generics.RetrieveAPIView):

    queryset            = Actuator_type.objects.all()
    serializer_class    = Actuator_typeSerializer

class Actuator_typeAPIDetailModify(generics.RetrieveUpdateAPIView):

    permission_classes  = (IsAdminUser,)
    queryset            = Actuator_type.objects.all()
    serializer_class    = Actuator_typeSerializer

class Actuator_typeAPIDetailDelete(generics.RetrieveDestroyAPIView):

    permission_classes  = (IsAdminUser,)
    queryset            = Actuator_type.objects.all()
    serializer_class    = Actuator_typeSerializerFullRestricted


# ========================
# ==== Actuator related ==
# ========================
class ActuatorAPICreate(generics.CreateAPIView):
    permission_classes  = (ActuatorPermission,)
    queryset            = Actuator.objects.all()
    serializer_class    = ActuatorSerializer

class ActuatorAPIDetail(generics.RetrieveAPIView):
    permission_classes  = (ActuatorPermission,)
    queryset         = Actuator.objects.all()
    serializer_class = ActuatorSerializer

class ActuatorAPIDetailModify(generics.RetrieveUpdateAPIView):
    permission_classes  = (ActuatorPermission,)
    queryset            = Actuator.objects.all()
    serializer_class    = ActuatorSerializer

class ActuatorAPIDetailDelete(generics.RetrieveDestroyAPIView):
    permission_classes  = (ActuatorPermission,)
    queryset            = Actuator.objects.all()
    serializer_class    = ActuatorSerializerFullRestricted


# =========================
# ==== Condition related ==
# =========================
class ConditionAPICreate(generics.CreateAPIView):
    permission_classes  = (ConditionPermission,)
    queryset         = Condition.objects.all()
    serializer_class = ConditionSerializer

class ConditionAPIDetail(generics.RetrieveAPIView):
    permission_classes  = (ConditionPermission,)
    queryset         = Condition.objects.all()
    serializer_class = ConditionSerializer

class ConditionAPIDetailModify(generics.RetrieveUpdateAPIView):
    permission_classes  = (ConditionPermission,)
    queryset         = Condition.objects.all()
    serializer_class = ConditionSerializer

class ConditionAPIDetailDelete(generics.RetrieveDestroyAPIView):
    permission_classes  = (ConditionPermission,)
    queryset         = Condition.objects.all()
    serializer_class = ConditionSerializerFullRestricted


# ===========================
# ==== Measurement related ==
# ===========================
class MeasurementAPICreate(generics.CreateAPIView):
    permission_classes  = (MeasurementPermission,)
    queryset         = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class MeasurementAPIDetail(generics.RetrieveAPIView):
    permission_classes  = (MeasurementPermission,)
    queryset         = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class MeasurementAPIDetailModify(generics.RetrieveUpdateAPIView):
    permission_classes  = (MeasurementPermission,)
    queryset         = Measurement.objects.all()
    serializer_class = MeasurementSerializer

class MeasurementAPIDetailDelete(generics.RetrieveDestroyAPIView):
    permission_classes  = (MeasurementPermission,)
    queryset         = Measurement.objects.all()
    serializer_class = MeasurementSerializerFullRestricted

class MeasurementAPIListByTimeRange(generics.ListAPIView):
    permission_classes  = (MeasurementListPermission,)
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        # Get the start and end times from the request parameters (e.g., query parameters)
        start_time = self.kwargs.get('start_time', None)
        end_time = self.kwargs.get('end_time', None)
        crop = self.kwargs.get('crop_id', None)

        if (start_time is None) or (end_time is None) or (crop is None):
            # Return an empty queryset if the time range is not specified
            return Measurement.objects.none()

        # Validate and convert the time range to Python datetime objects
        try:
            start_time = parse_datetime(start_time)
            end_time = parse_datetime(end_time)

        except (TypeError, ValueError):
            # Return an empty queryset if the time range is invalid
            return Measurement.objects.none()

        # Query the measurements within the specified time range
        queryset = Measurement.objects.filter(datetime__range=(start_time, end_time), crop=crop).order_by('datetime')
        return queryset


class MeasurementAPIListAll(generics.ListAPIView):
    permission_classes  = (MeasurementListPermission,)
    serializer_class = MeasurementSerializer

    def get_queryset(self):
        # Get the start and end times from the request parameters (e.g., query parameters)
        crop = self.kwargs.get('crop_id', None)

        if (crop is None):
            # Return an empty queryset if the time range is not specified
            return Measurement.objects.none()

        # Query the measurements within the specified time range
        queryset = Measurement.objects.filter(crop=crop).order_by('datetime')
        return queryset

from django.http import HttpResponse


@api_view(['POST'])
def  write_batch(request):

    if request.method == 'POST':
        data = request.data
        serializer = MeasurementSerializer(data=data, many=True)
        has_permission = MeasurementPermission.can_post_from_data(request.user, data)

        if serializer.is_valid() and has_permission:
            serializer.save()
            return Response({"detail": "OK"}, status=status.HTTP_201_CREATED)
        elif not has_permission:
            return Response({"detail": "Permission denied"}, status=status.HTTP_403_FORBIDDEN)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"detail": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

# ========================
# ==== Variable related ==
# ========================
class VariableAPICreate(generics.CreateAPIView):

    permission_classes  = (IsAdminUser,)
    queryset            = Variable.objects.all()
    serializer_class    = VariableSerializer

class VariableAPIDetail(generics.RetrieveAPIView):

    queryset         = Variable.objects.all()
    serializer_class = VariableSerializer

class VariableAPIDetailModify(generics.RetrieveUpdateAPIView):

    permission_classes  = (IsAdminUser,)
    queryset            = Variable.objects.all()
    serializer_class    = VariableSerializer

class VariableAPIDetailDelete(generics.RetrieveDestroyAPIView):

    permission_classes  = (IsAdminUser,)
    queryset            = Variable.objects.all()
    serializer_class    = VariableSerializerFullRestricted


# ====================
# ==== User related ==
# ====================
class CreateUserView(generics.CreateAPIView):
    queryset            = User.objects.all()
    serializer_class    = UserSerializer
    permission_classes  = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user  = authenticate(username=email, password=password)
            
            #try to get the token, if not existent create it
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)

            if user is not None:
                login(request, user)
                data = {'detail': 'Logged in successfully.', 'token': token.key}
                return Response(data, status=status.HTTP_200_OK)
            else:
                #print(f"{user}:{email}:{password}")
                return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)