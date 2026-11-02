from django.db import transaction
from .models import ExamBooking, ExamVenue, ScratchCard
from exam.models import Exam, ExamMark, ExamParticipant, ExamAnswerChoice, ExamAnswerText, ExamQuestion
from question_bank.models import *
from restframework import serializers
from .views import JSONResponse

class ExamSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Exam
        fields = ("__all__")

class ExamBookingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamBooking
        fields = ("__all__")

class ExamVenueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamVenue
        fields = ("__all__")

class ScratchCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ScratchCard
        fields = ("__all__")

class ExamParticipantSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamParticipant
        fields = ("__all__")

class ExamMarkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamMark
        fields = ("__all__")

class ExamAnswerChoiceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamAnswerChoice
        fields = ("__all__")

class ExamAnswerTextSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamAnswerText
        fields = ("__all__")

class ExamQuestionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ExamQuestion
        fields = ("__all__")

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category

class TokenSerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	class Meta:
		model = ScratchCard

class TranslatedQuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TranslatedQuestion
		# fields = ('id')

class TranslatedQuestionOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = TranslatedQuestionOption
		# fields = ('id')
		# exclude = ('is_answer',)

class QuestionOptionSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionOption
		# fields = ('id')
		# exclude = ('is_answer',) #TODO: To exclude fields, you must first list all fields via fields

class QuestionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Question
		# fields = ('id')

class QuestionMediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuestionMedia
		# fields = ('id')

class TranslatedQuestionMediaSerializer(serializers.ModelSerializer):
	class Meta:
		model = TranslatedQuestionMedia
		# fields = ('id')
