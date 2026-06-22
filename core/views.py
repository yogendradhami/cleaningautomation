from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Enquiry
from .email import send_notification


def index(request):
    return render(request, 'core/index.html')


def about(request):
    return render(request, 'core/about.html')


def services(request):
    return render(request, 'core/services.html')


def contact(request):
    sent = False
    if request.method == 'POST':
        # Simple anti-spam honeypot: bots may fill this field
        honeypot = request.POST.get('phone', '')
        if honeypot:
            # silently drop spam submissions
            return render(request, 'core/contact.html', {'sent': False})

        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        phone_number = request.POST.get('phone_number') or request.POST.get('phone') or ''
        property_type = request.POST.get('property_type', '')
        suburb = request.POST.get('suburb', '')
        preferred_date = request.POST.get('preferred_date') or None

        # Basic server-side validation
        if not (name and email):
            return render(request, 'core/contact.html', {'sent': False})

        # Save to database (images omitted)
        Enquiry.objects.create(
            name=name,
            email=email,
            phone_number=phone_number,
            property_type=property_type,
            suburb=suburb,
            preferred_date=preferred_date if preferred_date else None,
            message=message or '',
        )
        # Send notification (SendGrid web API if configured, otherwise Django email backend)
        subject = f'New enquiry from {name}'
        body = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
        ok = send_notification(subject, body)
        if not ok:
            print('Warning: failed to send email notification')
        sent = True
    return render(request, 'core/contact.html', {'sent': sent})


def privacy(request):
    return render(request, 'core/privacy.html')
