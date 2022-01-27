from rest_framework import serializers
from .models import NewUser
from rest_framework.validators import UniqueValidator

class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required= True,
        validators= [UniqueValidator(queryset= NewUser.objects.all())]
    )
    password = serializers.CharField(
        min_length= 8,
        write_only= True,
        required= True,
        style= {'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = NewUser
        fields = ['email', 'password','first_name', 'last_name', 'mobile']

    def create(self, validated_data):
        return NewUser.objects.create_user(**validated_data)



class ChangePasswordSerializer(serializers.Serializer):

    model = NewUser
    old_password = serializers.CharField(required= True)
    new_password = serializers.CharField(required=True)

