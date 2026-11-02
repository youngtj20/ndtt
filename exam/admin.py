from django.contrib import admin

# Register your models here.
from .models import Exam, ExamQuestion, ExamParticipant, ExamMark

admin.site.register(ExamMark)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
	list_display = ('title', 'description', 'duration', 'exam_start_date', 'exam_end_date', 'is_active', 'category',
					'pass_mark', 'marks_per_question',
					'exam_type', 'created_at')
	search_fields = ('title', 'description', 'exam_type', 'category')

@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'exam', 'exam_description', 'created_at')
	# search_fields = ('question_', 'translated_question', )
	def exam_description(self, obj):
		return obj.exam.description

@admin.register(ExamParticipant)
class ExamParticipantAdmin(admin.ModelAdmin):
	list_display = ('examination_number', 'exam', 'exam_description', 'can_take_test', 'created_at')
	search_fields = ('examination_number','finished_test',)
	def exam_description(self, obj):
		return obj.exam.description
