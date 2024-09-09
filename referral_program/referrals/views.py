from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Student
from .serializers import UserSerializers, StudentSerializer, PaymentSerializer
import logging
from django.core.cache import cache

logger = logging.getLogger('myapp')


class UserCreateView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializers


class UserDetailView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializers
  lookup_field = 'unique_id'


class ReferralLinkView(APIView):

  def get(self, request, unique_id):
    cache_key = f'referral_link_{unique_id}'
    cached_data = cache.get(cache_key)

    if cached_data:
      return Response({"referral_link": cached_data})

    try:
      user = User.objects.get(unique_id=unique_id)
      referral_link = user.get_referral_link()

      cache.set(cache_key, referral_link, timeout=600)
      return Response({"referral_link": referral_link})
    except User.DoesNotExist:
      return Response({"error": "User not found"}, status=404)


class RegisterStudentView(APIView):

  def post(self, request, unique_id):
    try:
      referrer = User.objects.get(unique_id=unique_id)
    except User.DoesNotExist:
      return Response({"error": "Referrer not found"}, status=404)

    data = request.data.copy()
    data['referrer'] = referrer.id
    serializer = StudentSerializer(data=data)

    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
  permission_classes = [IsAuthenticated]

  def post(self, request):
    serializer = PaymentSerializer(data=request.data)

    if serializer.is_valid():
      student_email = serializer.validated_data['student_email']

      try:
        student = Student.objects.get(email=student_email)

        student.lessons_count += 4
        student.save()

        if student.referrer:
          referrer = student.referrer
          referrer.lessons_count += 4
          referrer.save()

          logger.info(f'Added 4 lessons to both student {student_email} and referrer {referrer.email}')
        else:
          logger.warning(f'Student {student_email} has no referrer')

        return Response({'message': 'Payment processed and lessons added successfully'}, status=status.HTTP_200_OK)

      except ObjectDoesNotExist:
        logger.error(f'Student with email {student_email} does not exist')
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

    else:
      logger.error(f'Payment validation failed: {serializer.errors}')
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReferralStatsView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request, user_id):
    try:
      user = User.objects.get(id=user_id)
      referred_students = user.student.referred_students.all()
      serializer = StudentSerializer(referred_students, many=True)
      return Response({"referred_students": serializer.data})
    except User.DoesNotExist:
      return Response({"error": "User not found"}, status=404)


class ProtectedView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    return Response({"message": "Это защищенный контент, доступный только авторизованным пользователям!"})


class ProfileView(APIView):
  permission_classes = [IsAuthenticated]

  def get(self, request):
    user = request.user  # Получаем авторизованного пользователя
    profile_data = {
      "username": user.username,
      "email": user.email,
      "referrals": user.referred_students.all()  # Например, список рефералов
    }
    return Response(profile_data)
