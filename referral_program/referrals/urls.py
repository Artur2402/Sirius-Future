from django.urls import path
from .views import (UserCreateView, UserDetailView, ReferralLinkView, RegisterStudentView,
                    PaymentView, ReferralStatsView, ProfileView)


urlpatterns = [
  path('profile/', ProfileView.as_view(), name='profile'),
  path('user/create/', UserCreateView.as_view(), name='user-create'),
  path('user/<str:unique_id>/', UserDetailView.as_view(), name='user-details'),
  path('user/<str:unique_id>/referral/', ReferralLinkView.as_view(), name='referral-link'),
  path('register/<str:unique_id>/', RegisterStudentView.as_view(), name='student-register'),
  path('payment/', PaymentView.as_view(), name='payment'),
  path('stats/<int:user_id>/', ReferralStatsView.as_view(), name='referral_stats')
]