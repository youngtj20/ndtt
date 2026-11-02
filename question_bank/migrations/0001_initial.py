# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('title', models.CharField(max_length=10)),
                ('fees', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('question', models.CharField(max_length=500)),
                ('language', models.CharField(default='en', choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('image', models.FileField(null=True, upload_to='question/images/', blank=True)),
                ('audio', models.FileField(null=True, upload_to='question/audio/', blank=True)),
                ('video', models.FileField(null=True, upload_to='question/video/', blank=True)),
                ('question_type', models.CharField(choices=[('scqt', 'Single Choice Question Type'), ('mcqt', 'Multi Choice Question Type'), ('tet', 'Text Entry Type')], max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(related_name='question', to='question_bank.Category')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('label', models.TextField()),
                ('language', models.CharField(default='en', choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('image', models.FileField(null=True, upload_to='', blank=True)),
                ('audio', models.FileField(null=True, upload_to='', blank=True)),
                ('video', models.FileField(null=True, upload_to='', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(to='question_bank.Question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('question_option', models.CharField(max_length=400)),
                ('language', models.CharField(default='en', choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('image', models.FileField(null=True, upload_to='question/images/', blank=True)),
                ('audio', models.FileField(null=True, upload_to='question/audio/', blank=True)),
                ('video', models.FileField(null=True, upload_to='question/video/', blank=True)),
                ('is_answer', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(related_name='answer_choices', to='question_bank.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TranslatedQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('translated_question', models.CharField(max_length=500)),
                ('language', models.CharField(choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('image', models.FileField(null=True, upload_to='translated/images/', blank=True)),
                ('audio', models.FileField(null=True, upload_to='translated/audio/', blank=True)),
                ('video', models.FileField(null=True, upload_to='translated/video/', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(related_name='translated_questions', to='question_bank.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TranslatedQuestionMedia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('translated_label', models.TextField()),
                ('image', models.FileField(null=True, upload_to='', blank=True)),
                ('audio', models.FileField(null=True, upload_to='', blank=True)),
                ('video', models.FileField(null=True, upload_to='', blank=True)),
                ('language', models.CharField(choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(to='question_bank.Question')),
            ],
        ),
        migrations.CreateModel(
            name='TranslatedQuestionOption',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('translated_question_option', models.CharField(max_length=400)),
                ('language', models.CharField(choices=[('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')], max_length=2)),
                ('is_answer', models.BooleanField(default=False)),
                ('image', models.FileField(null=True, upload_to='translated/images/', blank=True)),
                ('audio', models.FileField(null=True, upload_to='translated/audio/', blank=True)),
                ('video', models.FileField(null=True, upload_to='translated/video/', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(related_name='translated_question_answer_choices', to='question_bank.TranslatedQuestion')),
            ],
        ),
    ]
