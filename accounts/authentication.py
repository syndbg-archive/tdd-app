import requests

from django.contrib.auth import get_user_model

User = get_user_model()


PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'
DOMAIN = 'localhost'


class PersonaAuthenticationBackend:

    def authenticate(self, assertion):
        response = requests.post(
            PERSONA_VERIFY_URL,
            data={'assertion': assertion, 'audience': DOMAIN}
        )
        json = response.json()
        if response.ok and json['status'] == 'okay':
            json_email = json['email']
            try:
                return User.objects.get(email=json_email)
            except User.DoesNotExist:
                return User.objects.create(email=json_email)

    def get_user(self, email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return
