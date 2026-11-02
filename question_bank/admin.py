from django.contrib import admin

# Register your models here.
from .models import Question, TranslatedQuestion, QuestionMedia, TranslatedQuestionMedia
from .models import QuestionOption, TranslatedQuestionOption, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('title', 'fees', 'is_active')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'language', 'question_type', 'created_at')
	search_fields = ('question', 'question_type', )


@admin.register(TranslatedQuestion)
class TranslatedQuestionAdmin(admin.ModelAdmin):
	list_display = ('question', 'translated_question', 'created_at')
	search_fields = ('question', 'translated_question', )

@admin.register(QuestionMedia)
class QuestionMediaAdmin(admin.ModelAdmin):
	list_display = ('question', 'label', 'language')
	search_fields = ('question', 'label', )

@admin.register(TranslatedQuestionMedia)
class TranslatedQuestionMediaAdmin(admin.ModelAdmin):
	list_display = ('question', 'translated_label', 'language', 'created_at')
	search_fields = ('question', 'translated_label', 'language')

@admin.register(QuestionOption)
class QuestionOptionAdmin(admin.ModelAdmin):
	list_display = ('question', 'question_option', 'language', 'is_answer', 'created_at')
	search_fields = ('question', )

@admin.register(TranslatedQuestionOption)
class TranslatedQuestionOptionAdmin(admin.ModelAdmin):
	list_display = ('translated_question_option', 'language', 'created_at')
	search_fields = ('question', 'language', )