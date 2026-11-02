# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import custom.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('question_bank', '0001_initial'),
        ('exam', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamBooking',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('title', models.CharField(null=True, max_length=100, blank=True)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('middle_name', models.CharField(null=True, max_length=100, blank=True)),
                ('state', models.CharField(choices=[('ABIA', 'Abia'), ('ADAMAWA', 'Adamawa'), ('AKWA IBON', 'Akwa Ibom'), ('ANAMBRA', 'Anambra'), ('BAUCHI', 'Bauchi'), ('BAYELSA', 'Bayelsa'), ('BENUE', 'Benue'), ('BORNO', 'Borno'), ('CROSS RIVER', 'Cross River'), ('DELTA', 'Delta'), ('EBONYI', 'Ebonyi'), ('EDO', 'Edo'), ('EKITI', 'ekiti'), ('ENUGU', 'Enugu'), ('FCT', 'FCT'), ('GOMBE', 'Gombe'), ('IMO', 'Imo'), ('JIGAWA', 'Jigawa'), ('KADUNA', 'Kaduna'), ('KANO', 'kano'), ('KASTINA', 'Kastina'), ('KEBBI', 'Kebbi'), ('KOGI', 'Kogi'), ('KWARA', 'Kwara'), ('LAGOS', 'Lagos'), ('NASSARAWA', 'Nassarawa'), ('NIGER', 'Niger'), ('ONDO', 'Ondo'), ('OGUN', 'Ogun'), ('OSUN', 'Osun'), ('OYO', 'Oyo'), ('PLATEAU', 'Plateau'), ('RIVERS', 'Rivers'), ('SOKOTO', 'Sokoto'), ('TARABA', 'Taraba'), ('YOBE', 'Yobe'), ('ZAMFARA', 'Zamfara')], max_length=100)),
                ('mobile_number', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=254, blank=True)),
                ('address', models.TextField(blank=True)),
                ('date_of_birth', models.DateField(blank=True)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=1)),
                ('preffered_date', models.DateField()),
                ('drive_test_type', models.CharField(null=True, choices=[('new', 'New'), ('renew', 'Re-New')], max_length=30, blank=True)),
                ('exam_preferred_language', models.CharField(default='en', choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('photo', models.ImageField(null=True, upload_to='booking_images', blank=True)),
                ('onsite_photo', models.TextField(null=True, blank=True)),
                ('card_number', models.CharField(null=True, max_length=12, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('examination_number', models.CharField(default=custom.models.generate_exam_number, unique=True, max_length=10, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='ExamPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('photo', models.ImageField(null=True, upload_to='', blank=True)),
                ('examination_number', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(to='exam.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamVenue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('exam_venue', models.CharField(max_length=200)),
                ('state', models.CharField(choices=[('ABIA', 'Abia'), ('ADAMAWA', 'Adamawa'), ('AKWA IBON', 'Akwa Ibom'), ('ANAMBRA', 'Anambra'), ('BAUCHI', 'Bauchi'), ('BAYELSA', 'Bayelsa'), ('BENUE', 'Benue'), ('BORNO', 'Borno'), ('CROSS RIVER', 'Cross River'), ('DELTA', 'Delta'), ('EBONYI', 'Ebonyi'), ('EDO', 'Edo'), ('EKITI', 'ekiti'), ('ENUGU', 'Enugu'), ('FCT', 'FCT'), ('GOMBE', 'Gombe'), ('IMO', 'Imo'), ('JIGAWA', 'Jigawa'), ('KADUNA', 'Kaduna'), ('KANO', 'kano'), ('KASTINA', 'Kastina'), ('KEBBI', 'Kebbi'), ('KOGI', 'Kogi'), ('KWARA', 'Kwara'), ('LAGOS', 'Lagos'), ('NASSARAWA', 'Nassarawa'), ('NIGER', 'Niger'), ('ONDO', 'Ondo'), ('OGUN', 'Ogun'), ('OSUN', 'Osun'), ('OYO', 'Oyo'), ('PLATEAU', 'Plateau'), ('RIVERS', 'Rivers'), ('SOKOTO', 'Sokoto'), ('TARABA', 'Taraba'), ('YOBE', 'Yobe'), ('ZAMFARA', 'Zamfara')], max_length=20)),
                ('code', models.CharField(max_length=10)),
                ('email', models.EmailField(max_length=254)),
                ('mobile_number', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=300)),
                ('address', models.CharField(max_length=400)),
                ('is_active', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('transaction_ref', models.CharField(unique=True, max_length=100)),
                ('mobile_number', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.CharField(null=True, max_length=200, blank=True)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ScratchCard',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('used', models.BooleanField(default=False)),
                ('pin_no', models.CharField(default=custom.models.generate_pin_number, unique=True, max_length=12, editable=False)),
                ('description', models.TextField()),
                ('category', models.ForeignKey(related_name='scratch_card', to='question_bank.Category')),
            ],
        ),
        migrations.AddField(
            model_name='exambooking',
            name='exam_venue',
            field=models.ForeignKey(to='custom.ExamVenue'),
        ),
    ]
