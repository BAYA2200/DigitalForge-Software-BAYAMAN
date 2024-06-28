from rest_framework import serializers

from .models import ManagerUser, Apartment, Client

class ManagerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagerUser
        fields = ('email', 'username', 'last_name', 'patronymic', 'phone_number', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Обновите пароль с хэшированием
        instance.save()
        return instance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)



    class Meta:
        model = ManagerUser
        fields = ('email', 'username', 'last_name', 'patronymic', 'phone_number','password')


    def create(self, validated_data):
        user = ManagerUser(
            email=validated_data['email'],
            username=validated_data['username'],
            last_name=validated_data['last_name'],
            patronymic=validated_data['patronymic'],
            phone_number=validated_data['phone_number'],
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
