from rest_framework import serializers
from django.core.validators import EmailValidator
from .models import User, Student


class UserSerializers(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(validators=[EmailValidator()])
  phone = serializers.RegexField(regex=r'^\+?\d{10,15}$',
                                 error_messages={"invalid": "Введите корректный номер телефона."})

  class Meta:
    model = Student
    fields = ['full_name', 'phone', 'email', 'referrer']

  def validate_full_name(self, value):
    if len(value.split()) < 2:
      raise serializers.ValidationError("Введите полное имя.")
    return value

  def validate_email(self, value):
    if Student.objects.filter(email=value).exists():
      raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован.")
    return value


class PaymentSerializer(serializers.Serializer):
  student_id = serializers.IntegerField()
  amount = serializers.DecimalField(max_digits=10, decimal_places=2)

  def validate_amount(self, value):
    if value <= 0:
      raise serializers.ValidationError("Сумма оплаты должна быть положительной.")
    return value
