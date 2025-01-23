from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={
        'input_type': 'password'
    }, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password','password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']: 
            raise serializers.ValidationError({
                'password': 'Password fields do not match.' 
            })
        return attrs
    
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'password']  

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        try:
            user = User.objects.get(username=username)  
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid username or password.')

        if not user.check_password(password):
            raise serializers.ValidationError('Invalid username or password.')

        return attrs