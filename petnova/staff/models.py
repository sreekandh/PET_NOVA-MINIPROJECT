from django.db import models

# Create your models here.


# models.py
from django.db import models
from django.shortcuts import render

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.name}'

# views.py

from .models import ContactMessage


def view_contact_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')  # Retrieve messages
    return render(request, 'staff/view_contact_messages.html', {'messages_list': messages_list})
