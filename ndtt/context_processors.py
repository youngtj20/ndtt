from django.conf import settings
import config
from exam.models import ExamParticipant
from exam.models import ExamQuestion, Exam
from custom.models import ExamVenue, ExamBooking, Payment, ScratchCard

def extra_context(request):
    return {
      'app_name':  config.app,
    #   'user': request.user
      'total_centers':  ExamVenue.objects.count(),
      'total_token_sales': Payment.objects.count(),
      'total_booking': ExamBooking.objects.count(),
      'total_exams': Exam.objects.count(),
    }
    
def debug(context):
  return {'DEBUG': settings.DEBUG}