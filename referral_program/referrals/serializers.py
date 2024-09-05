from rest_framework import serializers
from .models import User, Student


class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = ['full_name', 'phone', 'email', 'referrer']