import sys

import requests

from accounts.models import ListUser


class PersonaAuthenticationBackend:

    def authenticate(self, assertion):
        data = {'assertion': assertion, 'audience': 'localhost'}
        print('sending to mozilla', data, file=sys.stderr)
        verify_response = requests.post('https://verifier.login.persona.org/verify', data=data)
        print('received', verify_response.content, file=sys.stderr)

        if verify_response.ok:
            verification_data = verify_response.json()
            if verification_data['status'] == 'okay':
                email = verification_data['email']
                try:
                    return self.get_user(email)
                except ListUser.DoesNotExist as e:
                    return ListUser.objects.create(email=email)

    def get_user(self, email):
        return ListUser.objects.get(email=email)
