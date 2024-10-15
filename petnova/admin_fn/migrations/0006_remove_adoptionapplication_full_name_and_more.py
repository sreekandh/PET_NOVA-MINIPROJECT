# Generated by Django 5.1 on 2024-10-15 01:13

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_fn', '0005_caretaker_is_active_caretaker_password_cat_price_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adoptionapplication',
            name='full_name',
        ),
        migrations.AddField(
            model_name='adoptionapplication',
            name='first_name',
            field=models.CharField(default='first name', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='adoptionapplication',
            name='last_name',
            field=models.CharField(default='last name', max_length=30),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='TrainerSlotBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service', models.CharField(max_length=255)),
                ('duration', models.PositiveIntegerField()),
                ('additional_notes', models.TextField(blank=True, null=True)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('pet_name', models.CharField(max_length=100)),
                ('pet_breed', models.CharField(max_length=100)),
                ('pet_species', models.CharField(max_length=100)),
                ('pet_age', models.PositiveIntegerField()),
                ('pet_image', models.ImageField(blank=True, null=True, upload_to='pet_images/')),
                ('service_start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='confirmed', max_length=10)),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='admin_fn.trainer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_bookings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
