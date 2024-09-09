from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

  def test_create_user(self):
    User = get_user_model()
    user = User.objects.create_user(
      username='testuser',
      email='test@example.com',
      password='secret'
    )
    self.assertEqual(user.username, 'testuser')
    self.assertEqual(user.email, 'test@example.com')
    self.assertTrue(user.check_password('secret'))

  class ReferralLinkTest(TestCase):

    def setUp(self):
      self.user = get_user_model().objects.create_user(
        username='referrer',
        email='referrer@example.com',
        password='testpassword'
      )
      self.referral_link = self.user.get_referral_link()

    def test_register_via_referral(self):
      response = self.client.get(self.referral_link)
      self.assertEqual(response.status_code, 200)
