from django.contrib import admin
from .models import Sync
# Register your models here.
@admin.register(Sync)
class ExamVenueAdmin(admin.ModelAdmin):
	list_display = ('center', 'destination', 'last_sync')
