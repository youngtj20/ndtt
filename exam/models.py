from django.db import models
from question_bank.models import Question, QuestionOption, Category
import uuid
from decimal import Decimal

# Create your models here.
class Exam(models.Model):
	"""Exam Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=200)
	category = models.ForeignKey(Category, related_name='exam')
	description = models.CharField(null=True, blank=True, max_length=300)
	exam_type = models.CharField(max_length=30, choices=(
		('sheduled', 'Sheduled'),
		('manual', 'Manual'),
		('practice', 'Practice Test'),
		('anytime', 'Anytime')
	), default='sheduled')
	exam_start_date = models.DateField(null=True, blank=True)
	exam_end_date = models.DateField(null=True, blank=True)
	duration = models.DurationField()
	is_active = models.BooleanField(default=False)
	pass_mark = models.IntegerField()
	number_of_question = models.IntegerField()
	marks_per_question = models.IntegerField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.title)

class ExamQuestion(models.Model):
	"""Exam Question Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, related_name='exam_questions', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s %s' % (self.exam, self.question)

class ExamParticipant(models.Model):
	"""Exam Participant Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	examination_number = models.CharField(max_length=10, unique=True)
	can_take_test = models.BooleanField(default=True) # Flag For e.g Payment, Auth etc
	finished_test = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s %s' % (self.examination_number, self.exam.title)

# class ExamSheet(models.Model):
# 	"""Exam Sheet Model"""
# 	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
# 	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
# 	exam_participant = models.ForeignKey(ExamParticipant, on_delete=models.CASCADE)
# 	question = models.ForeignKey(Question, on_delete=models.CASCADE)
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)
# 	def __str__(self):
# 		return '%s %s %s' % (self.exam_participant.examination_number, self.exam.title, 
# 			self.question.question)

class ExamMark(models.Model):
	"""All Candidate Results, No Support For Resume"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	# exam_question = models.ForeignKey(ExamQuestion, on_delete=models.CASCADE)
	score = models.DecimalField(max_digits=3,decimal_places=1,default=Decimal('0.0'))
	exam_participant = models.ForeignKey(ExamParticipant, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s got answer %s' % (self.exam_participant, self.score)
		
class ExamAnswerText(models.Model):
	"""Exam Answer Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	exam_participant = models.ForeignKey(ExamParticipant, on_delete=models.CASCADE)
	exam_mark = models.ForeignKey(ExamMark, on_delete=models.CASCADE)
	answer_text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.answer_text)

class ExamAnswerChoice(models.Model):
	"""Exam Answer Choice Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	exam_participant = models.ForeignKey(ExamParticipant, on_delete=models.CASCADE)
	exam_mark = models.ForeignKey(ExamMark, on_delete=models.CASCADE)
	answer_choice = models.ForeignKey(QuestionOption, on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s' % (self.answer_choice.question_option)