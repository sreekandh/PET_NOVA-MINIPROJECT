from django.shortcuts import render



# Create your views here.
def staff_info(request):
    return render(request, 'staff/staff_info.html')

def trainer_service(request):
    return render(request, 'staff/trainer_service.html')

def caretaker_service(request):
    return render(request, 'staff/caretaker_service.html')

def about_page(request):
    return render(request,'staff/about_page.html')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import ContactMessage  # Import your model

@login_required
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Save the message to the database
        contact_message = ContactMessage(name=name, email=email, message=message)
        contact_message.save()

        # Send email to admin
        subject = f'New Contact Form Submission from {name}'
        email_message = f'You have received a new message from {name} ({email}):\n\n{message}'
        admin_email = 'sreekandh1212@gmail.com'
        
        try:
            send_mail(subject, email_message, email, [admin_email])
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_page')  # Redirect to the contact page after submission
        except Exception as e:
            messages.error(request, 'There was an error sending your message. Please try again later.')

    return render(request, 'staff/contact_page.html')



# views.py

from .models import ContactMessage


def view_contact_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')  # Retrieve messages
    return render(request, 'staff/view_contact_messages.html', {'messages_list': messages_list})
