from django.db import models
from django.conf import settings


class User(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField(unique=True)
  unique_id = models.CharField(unique=True, max_length=50)
  # lessons_count = models.IntegerField(default=0)

  def __str__(self):
    return f'{self.first_name} {self.last_name}'

  def get_referral_link(self):
    return f'{settings.SITE_URL}/register/{self.unique_id}'


class Student(models.Model):
  full_name = models.CharField(max_length=100)
  phone = models.CharField(max_length=15)
  email = models.EmailField(unique=True)
  referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='students')
  # lessons_count = models.IntegerField(default=0)

  def __str__(self):
    return self.full_name


class Lesson(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='lessons')
  referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrer_lessons', blank=True, null=True)
  count = models.IntegerField(default=4)
  date_added = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.count} lessons for {self.student} (referred by {self.referrer})'