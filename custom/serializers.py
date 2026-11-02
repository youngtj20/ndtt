from exam.models import Exam, ExamParticipant, ExamQuestion, ExamMark, ExamAnswerChoice, ExamAnswerText
from question_bank.models import Question, QuestionMedia, QuestionOption, TranslatedQuestion, \
	TranslatedQuestionMedia, TranslatedQuestionOption, Category
from custom.models import ExamBooking, ExamPhoto, ExamVenue, ScratchCard, Payment, STATE
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = "__all__"

class TokenSerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	class Meta:
		model = ScratchCard
		fields = "__all__"


class TranslatedQuestionOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TranslatedQuestionOption
		# fields = ('id')
		fields = "__all__"
		# exclude = ('is_answer',)

class TranslatedQuestionSerializer(serializers.ModelSerializer):
	translated_question_answer_choices = TranslatedQuestionOptionSerializer(many=True, read_only=True)
	class Meta:
		model = TranslatedQuestion
		# fields = ('id')
		fields = "__all__"


class QuestionOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionOption
		# fields = ('id')
		fields = "__all__"
		#TODO: To exclude fields, you must first list all fields via fields

class QuestionSerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	translated_questions = TranslatedQuestionSerializer(many=True, read_only=True)
	answer_choices = QuestionOptionSerializer(many=True, read_only=True)
	class Meta:
		model = Question
		# fields = ('id')
		fields = "__all__"

class ExamSerializer(serializers.ModelSerializer):
	# exam_questions = ExamQuestionSerializer(many=True, read_only=True)
	category = CategorySerializer()
	class Meta:
		model = Exam
		fields = "__all__"
		# fields = ('id', 'title', 'description', 'exam_type', 'start_date_if_sheduled', 
			# 'duration', 'anyone_can_take_test', 'created_at', 'updated_at', 'exam_questions')

class ExamQuestionSerializer(serializers.ModelSerializer):
	question = QuestionSerializer()
	exam = ExamSerializer()
	class Meta:
		model = ExamQuestion
		# fields = ('id',)
		fields = "__all__"

class ExamParticipantSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamParticipant
		fields = "__all__"
		# fields = ('id',)

class ExamMarkSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamMark
		fields = "__all__"
		# fields = ('id',)

class ExamAnswerChoiceSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamAnswerChoice
		# fields = ('id')
		fields = "__all__"

class ExamAnswerTextSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamAnswerText
		fields = "__all__"
		# fields = ('id')

class QuestionMediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionMedia
		fields = "__all__"
		# fields = ('id')

class TranslatedQuestionMediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = TranslatedQuestionMedia
		fields = "__all__"
		# fields = ('id')

class ExamBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamBooking
		fields = "__all__"
		# fields = ('id')

class ExamPhotoSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamPhoto
		fields = "__all__"
		# fields = ('id')

class ExamVenueSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamVenue
		fields = "__all__"
		# fields = ('id')
		


class BookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = ExamBooking
		fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Payment
		fields = "__all__"


class CustomBookingSerializer(serializers.Serializer):
	title = serializers.CharField(allow_blank=True, allow_null=True, max_length=100, required=False)
	first_name = serializers.CharField(max_length=100)
	last_name = serializers.CharField(max_length=100)
	middle_name = serializers.CharField(allow_blank=True, allow_null=True, max_length=100, required=False)
	state = serializers.ChoiceField(choices=STATE)
	mobile_number = serializers.CharField(max_length=50)
	email_address = serializers.EmailField(allow_blank=True, max_length=254, required=False)
	address = serializers.CharField(allow_blank=True, required=False, style={'base_template': 'textarea.html'})
	date_of_birth = serializers.DateField(required=False)
	gender = serializers.ChoiceField(choices=(('M', 'Male'), ('F', 'Female')))
	preffered_date = serializers.DateField()
	drive_test_type = serializers.ChoiceField(allow_blank=True, allow_null=True, choices=(('new', 'New'), ('renew', 'Re-New')), required=False)
	exam_preferred_language = serializers.ChoiceField(choices=(('en', 'English'), ('ho', 'Hausa'), ('yo', 'Yoruba'), ('ig', 'Igbo'), ('pg', 'Pidgin')), required=False)
	# what happens here?
	photo = serializers.ImageField(allow_null=True, required=False)
	card_number = serializers.CharField(max_length=12)
	examination_number = serializers.CharField(max_length=10)
	exam_category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
	exam_venue = serializers.PrimaryKeyRelatedField(queryset=ExamVenue.objects.all())
