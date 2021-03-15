from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from .models import User, Asiointi, Ruokalista, RavinVaikutu, Perustiedot
from django.shortcuts import get_object_or_404
from knox.models import AuthToken
from .serializers import (
    CreateUserSerializer, 
    UserSerializer, 
    LoginUserSerializer,
    ChangePasswordSerializer,
    ForgetPasswordSerializer,
    AsiointiSerializer, 
    RuokalistaSerializer, 
    RavinVaikutuSerializer, 
    PerustiedotSerializer
)




#user viewset
class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated,]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

#registration viewset
class RegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })


        
#login viewset
class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer._validated_data
    
        return Response({
            "user" : UserSerializer(user, context=self.get_serializer_context()).data,
            "token": AuthToken.objects.create(user)[1]
        })

class ChangePasswordAPI(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    @classmethod
    def get_extra_actions(cls):
        return []

    def get_object(self, queryset=None):
        return self.request.user





# Create your views here.
class AsiointiViewset(viewsets.ModelViewSet):
    queryset = Asiointi.objects.all()
    serializer_class = AsiointiSerializer
    permission_classes = [permissions.AllowAny,]

    """def get_queryset(self):
        return self.request.user.asiointis.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)"""


#ruokalista viewsets
class RuokalistaViewset(viewsets.ModelViewSet):
    queryset = Ruokalista.objects.all()
    serializer_class = RuokalistaSerializer
    permission_classes = [permissions.AllowAny]

    """def get_queryset(self):
        return self.request.user.ruokalistas.all()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)"""



#ravintovaikutus viewset
class RavinVaikutuViewset(viewsets.ModelViewSet):
    queryset = RavinVaikutu.objects.all()
    serializer_class = RavinVaikutuSerializer
    permission_classes = [permissions.AllowAny]

    """def get_queryset(self):
        return self.request.user.ravinvaikutus.all()

    def preform_create(self,  serializer):
        serializer.save(owner=self.request.user)"""



#perustiedot viewset
class PerustiedotViewset(viewsets.ModelViewSet):
    queryset = Perustiedot.objects.all()
    serializer_class = PerustiedotSerializer
    permission_classes = [permissions.AllowAny]

    """def get_queryset(self):
        return self.request.user.perustiedots.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)"""
