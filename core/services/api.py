import requests
from django.conf import settings

FLASK_API_URL = 'http://localhost:5000/api'

class APIClient:
    @staticmethod
    def submit_contact_form(name, email, subject, message):
        """Submit contact form to Flask API"""
        try:
            response = requests.post(
                f'{FLASK_API_URL}/contact',
                json={
                    'name': name,
                    'email': email,
                    'subject': subject,
                    'message': message
                }
            )
            return response.json(), response.status_code
        except requests.RequestException as e:
            return {'error': str(e)}, 500