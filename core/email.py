import os
import json
from django.core.mail import send_mail
from django.conf import settings

def send_notification(subject: str, body: str):
    """Send a notification using configured backend.

    Priority:
    1. If SENDGRID_API_KEY env var present, use SendGrid Web API.
    2. Otherwise use Django's configured email backend (send_mail).
    """
    sendgrid_key = os.environ.get('SENDGRID_API_KEY')
    if sendgrid_key:
        try:
            import requests
            url = 'https://api.sendgrid.com/v3/mail/send'
            payload = {
                "personalizations": [{"to": [{"email": settings.DEFAULT_FROM_EMAIL}]}],
                "from": {"email": settings.DEFAULT_FROM_EMAIL},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}],
            }
            headers = {
                'Authorization': f'Bearer {sendgrid_key}',
                'Content-Type': 'application/json'
            }
            resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
            resp.raise_for_status()
            return True
        except Exception:
            # Fall back to Django send_mail (development-friendly)
            pass
    # Fallback to Django's email backend
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])
        return True
    except Exception:
        return False
