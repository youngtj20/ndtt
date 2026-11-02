from django import forms

from .models import ExamBooking, ExamVenue
from exam.models import Exam
from django.contrib.auth.models import User
from question_bank.models import Category, Question, TranslatedQuestion, QuestionOption


class ExamBookingForm(forms.ModelForm):
	# exam_venue = forms.ModelChoiceField(queryset=ExamVenue.objects.none())
	class Meta:
		model = ExamBooking
		fields = [
			# "id",
			"photo",
			"first_name",
			"last_name",
			"middle_name",
			"state",
			"mobile_number",
			"email_address",
			"address",
			"date_of_birth",
			"preffered_date",
			# "drive_test_type",
			"exam_preferred_language",
			"exam_venue",
			'gender',
			# "card_number",
			# "onsite_photo",
			# "created_at",
			# "updated_at",
			# "full_name",
			# "examination_number",
		]
	

class LoginForm(forms.Form):
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

	class Meta:
		model = User
		fields = ('username', 'password')


class CategoryForm(forms.ModelForm):
	class Meta:
		model = Category
		fields = ('__all__')


class ExamForm(forms.ModelForm):
	class Meta:
		model = Exam
		fields = ('title', 'category', 'exam_type', 'exam_start_date', 'exam_end_date', 'duration',
				  'is_active', 'pass_mark', 'marks_per_question', 'number_of_question')


class QuestionForm(forms.ModelForm):

	class Meta:
		model = Question
		fields = ('question', 'image', 'audio', 'category', 'question_type')
		widgets = {
			'question': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}


class OptionForm(forms.ModelForm):
	
	class Meta:
		model = QuestionOption
		fields = ('question_option', 'image', 'audio', 'is_answer')
		widgets = {
			'question_option': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}


class TranslatedQuestionForm(forms.ModelForm):
	class Meta:
		model = TranslatedQuestion
		fields = ('translated_question', 'language', 'image', 'audio')
		widgets = {
			'translated_question': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
		}


class VenueForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = ExamVenue
		exclude = ('created_at', 'updated_at')