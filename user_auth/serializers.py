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
    email = serializers.EmailField()
    password = serializers.CharField(style={
        'input_type': 'password'
    })

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        try:
            user = user.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('invalid email or password')
        if not user.check_password(password):
            raise serializers.ValidationError('invalid email or password')
        
        return attrs