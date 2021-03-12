from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from .models import Asiointi, Ruokalista, RavinVaikutu, Perustiedot
from django.contrib.auth.password_validation import validate_password
#user
User = get_user_model()

class CreateUserSerializer(serializers.ModelSerializer):
    """serializes the user creating"""
    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password' : {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

#User serialzer
class UserSerializer(serializers.ModelSerializer):
    """serializes the user"""
    class Meta:
        model = User
        fields = ('id', 'email', 'first_login')


#login serializers
class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


#change password serializer
class ChangePasswordSerializer(serializers.Serializer):
    """" password changing serializer """
    old_password = serializers.CharField(required=True)
    new_password1= serializers.CharField(required=True)
    new_password2= serializers.CharField(required=True)

    def validate(self, data):
        # add here additional check for password strength if needed
        if not self.context['request'].user.check_password(data.get('old_password')):
            raise serializers.ValidationError({'old_password': 'Wrong password.'})

        if data.get('new_password2') != data.get('new_password1'):
            raise serializers.ValidationError({'new_password1': 'Password must be confirmed correctly.'})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password1'])
        instance.save()
        return instance

    def create(self, validated_data):
        pass

    @property
    def data(self):
        # just return success dictionary. you can change this to your need, but i dont think output should be user data after password change
        return {'Password updated successfully': True}


#forget password serializer
class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


##asiointi serializer
class AsiointiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asiointi
        fields = ('id', 'yksi', 'kaksi', 'kolme', 'nelja')


#ruokalista serializer
class RuokalistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruokalista
        fields = ('id', 'viisi','kuusi','seitseman','kahdeksan','yhdeksan')


#ravinvaikutus serializer
class RavinVaikutuSerializer(serializers.ModelSerializer):
    class Meta:
        model = RavinVaikutu
        fields = ('id','kymenen','yksitoista','kaksitoista','kolmetoista')


#perustiedot serialiser
class PerustiedotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perustiedot
        fields = ('id', 'yksi', 'kaksi','kolme', 'nelja', 'viisi','kuusi','seitseman','kahdeksan','yhdeksan','kymenen')

    