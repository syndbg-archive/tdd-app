import requests
import logging

from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


PERSONA_VERIFY_URL = 'https://verifier.login.persona.org/verify'


class PersonaAuthenticationBackend:

    def authenticate(self, assertion):
        logging.warning('entering authenticate function')
        response = requests.post(
            PERSONA_VERIFY_URL,
            verify=True,
            data={'assertion': assertion, 'audience': settings.DOMAIN}
        )
        logging.warning('got response from persona')
        logging.warning(response.content.decode())
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
