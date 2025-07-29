from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserContactModel


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,  
        allow_blank=True,  # Allows empty string
        # validators=[serializers.EmailValidator()]  # Ensures it's a valid email format
    )
    class Meta:
        model = User
        fields = ['id','username','email','password','confirm_password']
        extra_kwargs = {'password':{'write_only':True}}

    def validate(self, data):
        """Check that password and confirm_password match."""
        password = data.get('password')
        confirm_password = self.initial_data.get('confirm_password')  # Fix: Use initial_data

        if not confirm_password:
            raise serializers.ValidationError({"confirm_password": "This field is required."})
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})

        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password') 
        user = User.objects.create_user(**validated_data)
        return user

class ContactUsSerailizer(serializers.ModelSerializer):
    class Meta:
        model = UserContactModel
        fields = ['name','email','description','phonenumber']



    