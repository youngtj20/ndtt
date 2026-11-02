from django.conf import settings
from exam.models import ExamParticipant
from exam.models import ExamQuestion, Exam
from functools import reduce
from django.db.models import Sum

from custom.models import ExamVenue, ExamBooking, Payment, ScratchCard, Payment

def extra_context(request):
  total_revenue = Payment.objects.all()#.aggregate(Sum('amount'))
  # print("total_revenue")
  print(total_revenue)
  return {
    'total_revenue': total_revenue if total_revenue else 0,#ModelName.objects.aggregate(Sum('field_name'))
    'total_centers':  len(ExamVenue.objects.all()),
    'total_token_sales': len(Payment.objects.all()),
    'total_booking': len(ExamBooking.objects.all()),
    'total_exams': len(Exam.objects.all()),
  }
    
def debug(context):
  return {'DEBUG': settings.DEBUG}