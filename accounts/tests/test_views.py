from unittest.mock import patch

from django.contrib.auth import get_user_model, SESSION_KEY
from django.test import TestCase

User = get_user_model()


class LoginViewTest(TestCase):

    @patch('accounts.views.authenticate')
    def test_calls_authenticate_with_assertion_from_post(self, mocked_authenticate):
        mocked_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'assert this'})
        mocked_authenticate.assert_called_once_with(assertion='assert this')

    @patch('accounts.views.authenticate')
    def test_returns_OK_when_user_found(self, mocked_authenticate):
        user = User.objects.create(email='a@b.com')
        user.backend = ''
        mocked_authenticate.return_value = user
        response = self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(response.content.decode(), 'OK')

    @patch('accounts.views.authenticate')
    def test_gets_logged_in_session_if_authenticate_returns_a_user(self, mocked_authenticate):
        user = User.objects.create(email='a@b.com')
        user.backend = ''
        mocked_authenticate.return_value = user
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertEqual(self.client.session[SESSION_KEY], user.pk)

    @patch('accounts.views.authenticate')
    def test_does_not_get_logged_in_if_authenticate_returns_none(self, mocked_authenticate):
        mocked_authenticate.return_value = None
        self.client.post('/accounts/login', {'assertion': 'a'})
        self.assertNotIn(SESSION_KEY, self.client.session)
