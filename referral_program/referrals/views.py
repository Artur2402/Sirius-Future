from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .models import User, Student, Lesson
from .serializers import UserSerializers, StudentSerializer


class UserCreateView(generics.CreateAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializers


class UserDetailView(generics.RetrieveAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializers
  lookup_field = 'unique_id'


class ReferralLinkView(APIView):
  def get(self, request, unique_id):
    try:
      user = User.objects.get(unique_id=unique_id)
      referral_link = user.get_referral_link()
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

    # print(f"Data being sent to the serializer: {data}")

    serializer = StudentSerializer(data=data)

    if serializer.is_valid():
      # print("Serializer is valid")
      serializer.save()
      return Response(serializer.data, status=status.HTTP_201_CREATED)
    # print(f"Serializer errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentView(APIView):
  def post(self, request):
    student_id = request.data.get('student_id')

    try:
      student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
      return Response({'error': "Student not found"}, status=404)

    Lesson.objects.create(student=student, referrer=student.referrer, count=4)
    # student.lessons_count += 4
    # student.referrer.lessons_count += 4
    # student.save()
    # student.referrer.save()

    return Response({'message': "Payment processed and lessons added."}, status=200)


class ReferralStatsView(APIView):
  def get(self, request, user_id):
    try:
      user = User.objects.get(id=user_id)
    except User.DoesNotExist:
      return Response({"error": "User not found"}, status=404)

    referred_students = user.students.all()
    total_referred = referred_students.count()
    total_lessons_earned = sum([lesson.count for lesson in user.referrer_lessons.all()])

    return Response({
      "total_referred": total_referred,
      "total_lessons_earned": total_lessons_earned
    }, status=200)