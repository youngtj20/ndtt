# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from decimal import Decimal
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('question_bank', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(null=True, max_length=300, blank=True)),
                ('exam_type', models.CharField(default='sheduled', choices=[('sheduled', 'Sheduled'), ('manual', 'Manual'), ('practice', 'Practice Test'), ('anytime', 'Anytime')], max_length=30)),
                ('exam_start_date', models.DateField(null=True, blank=True)),
                ('exam_end_date', models.DateField(null=True, blank=True)),
                ('duration', models.DurationField()),
                ('is_active', models.BooleanField(default=False)),
                ('pass_mark', models.IntegerField()),
                ('number_of_question', models.IntegerField()),
                ('marks_per_question', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(related_name='exam', to='question_bank.Category')),
            ],
        ),
        migrations.CreateModel(
            name='ExamAnswerChoice',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('answer_choice', models.ForeignKey(to='question_bank.QuestionOption')),
                ('exam', models.ForeignKey(to='exam.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamAnswerText',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('answer_text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(to='exam.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamMark',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('score', models.DecimalField(default=Decimal('0.0'), decimal_places=1, max_digits=3)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(to='exam.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamParticipant',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('examination_number', models.CharField(unique=True, max_length=10)),
                ('can_take_test', models.BooleanField(default=True)),
                ('finished_test', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(to='exam.Exam')),
            ],
        ),
        migrations.CreateModel(
            name='ExamQuestion',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('exam', models.ForeignKey(to='exam.Exam')),
                ('question', models.ForeignKey(related_name='exam_questions', to='question_bank.Question')),
            ],
        ),
        migrations.AddField(
            model_name='exammark',
            name='exam_participant',
            field=models.ForeignKey(to='exam.ExamParticipant'),
        ),
        migrations.AddField(
            model_name='exammark',
            name='exam_question',
            field=models.ForeignKey(to='exam.ExamQuestion'),
        ),
        migrations.AddField(
            model_name='examanswertext',
            name='exam_mark',
            field=models.ForeignKey(to='exam.ExamMark'),
        ),
        migrations.AddField(
            model_name='examanswertext',
            name='exam_participant',
            field=models.ForeignKey(to='exam.ExamParticipant'),
        ),
        migrations.AddField(
            model_name='examanswerchoice',
            name='exam_mark',
            field=models.ForeignKey(to='exam.ExamMark'),
        ),
        migrations.AddField(
            model_name='examanswerchoice',
            name='exam_participant',
            field=models.ForeignKey(to='exam.ExamParticipant'),
        ),
    ]
