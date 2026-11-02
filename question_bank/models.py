from __future__ import unicode_literals
import uuid
from django.db import models
# Create your models here.

ENGLISH = 'en'
HAUSA = 'ho'
YORUBA = 'yo'
IGBO = 'ig'
PIDGIN = 'pg'
LANG_CHOICES = ( 
	(ENGLISH, 'English'), 
	(HAUSA, 'Hausa'), 
	(YORUBA, 'Yoruba'), 
	(IGBO, 'Igbo'),
	(PIDGIN, 'Pidgin') )


class Category(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=10)
	fees = models.DecimalField(decimal_places =2, max_digits=10)
	is_active = models.BooleanField(default=False)

	def __str__(self):
		return '%s' %self.title


class Question(models.Model):
	"""Question Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	question = models.CharField(max_length=500)
	language = models.CharField(max_length=2, choices=LANG_CHOICES, default=ENGLISH)
	image = models.FileField(null=True, blank=True, upload_to="question/images/")
	audio = models.FileField(null=True, blank=True, upload_to="question/audio/")
	video = models.FileField(null=True, blank=True, upload_to="question/video/")
	category = models.ForeignKey(Category, related_name='question')
	question_type = models.CharField(max_length=30, choices=( 
		('scqt', 'Single Choice Question Type'), 
		('mcqt', 'Multi Choice Question Type'), 
		('tet', 'Text Entry Type') ) )
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.question)


class TranslatedQuestion(models.Model):
	"""Translated Question Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	translated_question = models.CharField(max_length=500)
	question = models.ForeignKey(Question, related_name='translated_questions', on_delete=models.CASCADE)
	language = models.CharField(max_length=2, choices=LANG_CHOICES)
	image = models.FileField(null=True, blank=True, upload_to="translated/images/")
	audio = models.FileField(null=True, blank=True, upload_to="translated/audio/")
	video = models.FileField(null=True, blank=True, upload_to="translated/video/")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.translated_question)


class QuestionMedia(models.Model):
	"""Question Media Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	label = models.TextField()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	language = models.CharField(max_length=2, choices=LANG_CHOICES, default=ENGLISH)
	image = models.FileField(null=True, blank=True)
	audio = models.FileField(null=True, blank=True)
	video = models.FileField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.label)


class TranslatedQuestionMedia(models.Model):
	"""Translated Question Media Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	translated_label = models.TextField()
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	image = models.FileField(null=True, blank=True)
	audio = models.FileField(null=True, blank=True)
	video = models.FileField(null=True, blank=True)
	language = models.CharField(max_length=2, choices=LANG_CHOICES)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.translated_label)


class QuestionOption(models.Model):
	"""Question Option Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	question_option = models.CharField(max_length=400)
	question = models.ForeignKey(Question, related_name='answer_choices', on_delete=models.CASCADE)
	language = models.CharField(max_length=2, choices=LANG_CHOICES, default=ENGLISH)
	image = models.FileField(null=True, blank=True, upload_to="question/images/")
	audio = models.FileField(null=True, blank=True, upload_to="question/audio/")
	video = models.FileField(null=True, blank=True, upload_to="question/video/")
	is_answer = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.question_option)


class TranslatedQuestionOption(models.Model):
	"""Translated Question Option Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	translated_question_option = models.CharField(max_length=400)
	question = models.ForeignKey(TranslatedQuestion, related_name='translated_question_answer_choices',
								 on_delete=models.CASCADE)
	language = models.CharField(max_length=2, choices=LANG_CHOICES)
	is_answer = models.BooleanField(default=False)
	image = models.FileField(null=True, blank=True, upload_to="translated/images/")
	audio = models.FileField(null=True, blank=True, upload_to="translated/audio/")
	video = models.FileField(null=True, blank=True, upload_to="translated/video/")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.question)