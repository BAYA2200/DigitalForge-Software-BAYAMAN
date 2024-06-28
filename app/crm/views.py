from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters

from .filters import ApartmentFilter
from .models import ManagerUser, Apartment, Client
from .permissions import IsOwner
from .serializers import RegisterSerializer, ManagerUserSerializer, ApartmentSerializer, ClientSerializer


class RegisterManagerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ManagerUserListView(ListAPIView):
    queryset = ManagerUser.objects.all()
    serializer_class = ManagerUserSerializer


class ManagerUserDetailView(RetrieveAPIView):
    queryset = ManagerUser.objects.all()
    serializer_class = ManagerUserSerializer


class ManagerUserUpdateView(UpdateAPIView):
    queryset = ManagerUser.objects.all()
    serializer_class = ManagerUserSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsOwner, ]


class ManagerUserDeleteView(DestroyAPIView):
    queryset = ManagerUser.objects.all()
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsOwner, ]


class ObtainJWTView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = ManagerUser.objects.get(email=email)
        except ManagerUser.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


class ApartmentViewSet(viewsets.ModelViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, ]
    search_fields = ['address']
    filterset_class = ApartmentFilter

    def get_queryset(self):
        status = self.request.query_params.get('status')
        if status:
            return self.queryset.filter(status=status)
        return self.queryset


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
