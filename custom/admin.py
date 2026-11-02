from django.contrib import admin
from custom.models import ExamVenue, ExamBooking, ScratchCard, Payment
# Register your models here.
@admin.register(ExamVenue)
class ExamVenueAdmin(admin.ModelAdmin):
	list_display = ('exam_venue', 'created_at')

@admin.register(ExamBooking)
class ExamBookingAdmin(admin.ModelAdmin):
	list_display = ('full_name', 'examination_number', 'mobile_number', 
		'email_address', 'drive_test_type', 'address', 'date_of_birth', 
		'preffered_date', 'drive_test_type', 
		'exam_preferred_language', 'exam_venue', 'created_at', 'card_number', 'photo')
	search_fields = ('first_name', 'last_name', 'mobile_number', 'examination_number', )
	list_filter = ('drive_test_type', 'exam_preferred_language', 'exam_venue', )

@admin.register(ScratchCard)
class ScratchCardAdmin(admin.ModelAdmin):
	list_display = ('id', 'pin_no', 'used', 'amount', 'created_at', 'updated_at')
	search_fields = ('pin_no', 'used', 'created_at', )



admin.site.register(Payment)