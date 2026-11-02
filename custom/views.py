# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from base64 import b64decode
from django.core.files.base import ContentFile
from .models import ExamBooking
from exam.models import ExamParticipant
from exam.models import ExamQuestion
from django import forms
from django.forms.models import modelformset_factory, inlineformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.views.generic import View
from .utils import render_to_pdf, verify_payment
import datetime
from django.utils import timezone
from random import sample
from decimal import Decimal
from django.template.loader import render_to_string
from django.http import JsonResponse
import requests
import decimal
import hmac
import hashlib
from django.conf import settings
from django.urls import reverse

from exam.models import Exam, ExamParticipant, ExamQuestion, ExamMark, ExamAnswerChoice, ExamAnswerText
from question_bank.models import Question, QuestionMedia, QuestionOption, TranslatedQuestion, \
	TranslatedQuestionMedia, TranslatedQuestionOption, Category
from custom.models import ExamBooking, ExamPhoto, ExamVenue, ScratchCard, STATE, Payment

from .serializers import ExamSerializer, ExamParticipantSerializer, ExamQuestionSerializer, ExamBookingSerializer, \
	QuestionSerializer, CategorySerializer, ExamVenueSerializer, BookingSerializer, TokenSerializer, PaymentSerializer
from django.shortcuts import redirect
from django.contrib import messages
import json
from decimal import Decimal
from .forms import *
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as lg

class JSONResponse(HttpResponse):
	"""An HttpResponse that renders its content into JSON."""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)


class GeneratePdf(View):
	def get(self, request, *args, **kwargs):
		candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
		examParticipant = ExamParticipant.objects.get(examination_number=request.session['candidate'])
		candidate_marks = ExamMark.objects.filter(
			exam_participant=examParticipant.id, 
			exam=examParticipant.exam)
		candidate_mark = 0
		for mark in candidate_marks:
			candidate_mark+= mark.score
		score_in_percent = Decimal((candidate_mark / len(candidate_marks) ) * 100).quantize(Decimal('.01'))
		data = { 
			"candidate":  candidate, "exam": examParticipant, 
			"score_in_percent": score_in_percent,
			"verdict": "pass" if score_in_percent > 45 else "fail",
			"verdict_message": "Congratulations" if score_in_percent > 45 else "Sorry, you could not make it to the cut-off mark. Please try again.",
			"nQUestions": len(candidate_marks),
			"score": candidate_mark
		}
		pdf = render_to_pdf('custom/result.html', data)
		return HttpResponse(pdf, content_type='application/pdf')


@login_required
@staff_member_required
def index(request):
	return render(request, 'core/dashboard.html')


def auth(request):
	if request.method == "POST":
		login_form = LoginForm(request.POST)
		if login_form.is_valid():
			user = authenticate(username=request.POST['username'], password=request.POST[
				'password'])
			if user is not None:
				if user.is_staff and user.is_active:
					login(request, user)
					return redirect(index)
			else:
				messages.error(request, "your credentials can not be authenticated")
				return redirect(auth)
		else:
			messages.error(request, "Please check the input and try again")
			return render(request, 'core/login.html', {'form':login_form})
	login_form = LoginForm()
	return render(request, 'core/login.html', {'form':login_form})


def logout_user(request):
	lg(request)
	return redirect(auth)


def get_venue(request):
	venues = ExamVenue.objects.filter(state=request.GET['state'])
	smVenues = ExamVenueSerializer(venues, many=True).data
	return JSONResponse({'venues':smVenues})

@login_required
@staff_member_required
def exam_venue_list(request):
	venues = ExamVenue.objects.all()
	sVenues = ExamVenueSerializer(venues, many=True).data
	return render(request, 'core/venue_list.html', {'venues': sVenues})

@login_required
@staff_member_required
def exam_venue_create(request):
	if request.POST:
		form = VenueForm(request.POST)
		if form.is_valid():
			venue = form.save()
			return redirect(exam_venue_list)
		else:
			return render(request, 'core/exam_venue_create.html', {'form': form})
	else:
		form = VenueForm()
		return render(request, 'core/venue_create.html', {'form': form})


@login_required
@staff_member_required
def booking_list(request):
	venues = ExamVenue.objects.all()
	sVenues = ExamVenueSerializer(venues, many=True).data
	return render(request, 'core/booking_list.html', {'venues':sVenues})


def booking_list_api(request):
	venue = ExamVenue.objects.get(id=request.GET['venue'])
	booking = ExamBooking.objects.filter(exam_venue=venue)
	sBooking = BookingSerializer(booking, many=True).data
	return JSONResponse({'bookings':sBooking})


def question_list_api(request):
	questions = Question.objects.filter(category__id=request.GET['category'])
	sQuestions = QuestionSerializer(questions, many=True).data
	return JSONResponse({'questions':sQuestions})


def select_category(request):
	categories = Category.objects.all()
	sCategory = CategorySerializer(categories, many=True).data
	return render(request, 'core/select_category.html', {'categories': sCategory})


@login_required
@staff_member_required
def generate_token(request):
	if request.POST:
		category = Category.objects.get(id=request.POST['category'])
		number_of_tokens = int(request.POST['number_of_token'])
		description = request.POST['description']
		tokens = ScratchCard.objects.bulk_create([
			ScratchCard(category=category, description=description) for i in range(number_of_tokens)
			])
		return redirect(token_list)
	else:
		category = Category.objects.all()
		return render(request, 'core/generate_token.html', {'categories': category})


@login_required
@staff_member_required
def token_list(request):
	tokens = ScratchCard.objects.filter(used=False)
	sTokens = TokenSerializer(tokens, many=True).data
	return render(request, 'core/token_list.html', {'tokens': sTokens})


@login_required
@staff_member_required
def token_today(request):
	tokens = ScratchCard.objects.filter(created_at__gte=datetime.date.today())
	sTokens = TokenSerializer(tokens, many=True).data
	return render(request, 'core/token_list.html', {'tokens': sTokens})

def start_booking(request):
	if request.session.has_key('booking'):
		del request.session['booking']
	request.session['category'] = request.GET['category']
	return redirect(booking_page)


def payment(request):
	category = Category.objects.get(id=request.session['category'])
	return render(request, 'core/payment.html', {'category': category})


def make_payment(request):
	if request.POST:
		transaction_ref = request.POST.get('trxref')
		mobile_number = request.POST['mobile_number']
		amount = request.POST['amount']
		transaction = Payment.objects.filter(transaction_ref=transaction_ref)
		if not transaction:
			if verify_payment(transaction_ref, mobile_number, Decimal(amount)):
				card = ScratchCard.objects.create(category=Category.objects.get(id=request.session['category']), description=mobile_number)
				transaction = Payment.objects.create(transaction_ref=transaction_ref, mobile_number=mobile_number, amount=amount, description=card.category.title)
				messages.add_message(request, messages.SUCCESS, 'Your scratch card PIN is {0}, please copy an save it in a secure place'.format(card.pin_no))
				return redirect(booking_verification_page)
			else:
				messages.error(request, "Your payment could not be verified")
				return redirect(payment)
		else:
			card = ScratchCard.objects.get(description=mobile_number)
			messages.add_message(request, messages.SUCCESS, 'payment has been done, Use this pin for booking. {0}'.format(card.pin_no))
			return redirect(booking_verification_page)
	else:
		return HttpResponse(status=404)


def report(request):
	return render(request, 'core/report.html', {})


def payment_report(request):
	frm = request.GET.get('frm')
	to = request.GET.get('to')
	if frm and to:
		# print(to, frm, sep=" ")
		payments = Payment.objects.filter(created_at__range=[frm, to])
	else:
		payments = Payment.objects.all()
	sPayment = PaymentSerializer(payments, many=True)
	return JSONResponse({'payments':sPayment.data})


def booking_page(request):
	if not request.session.has_key('booking'):
		return redirect(booking_verification_page)

	if request.method == 'POST':
		form = ExamBookingForm(request.POST or None, request.FILES or None)
		card_details = ScratchCard.objects.get(pin_no=request.session['booking'])
		if form.is_valid() and not card_details.used:
			form = form.save(commit=False)
			form.title = request.POST.get('title')
			if request.session['booking']:
				form.card_number = request.session['booking']

			form.category = Category.objects.get(id=request.session['category'])
			form.save()
			card_details = ScratchCard.objects.get(pin_no=form.card_number)
			# payment = Payment.objects.get(mobile_number=form.mobile_number)
			# payment.status =True
			# payment.save()
			card_details.used = True
			card_details.save()
			try:
				exam = Exam.objects.filter(category=form.category).latest('updated_at')
			except:
				data = {}
				data['message'] = "Exams not found"
				return JsonResponse(data, status=400)
			ExamParticipant.objects.create(exam=exam, examination_number=form.examination_number)
			messages.success(request, "Your theory driving test has been booked")
			if request.session.has_key('booking'):
				del request.session['booking']
			if request.session.has_key('category'):
				del request.session['category']
			response = {}
			data = {}
			data['formId'] = form.id
			response['status'] = 'success'
			response['data'] = data
			return JsonResponse(response, status=201)
		else:
			errors = {
				field: [str(error) for error in field_errors]
				for field, field_errors in form.errors.items()
			}
			if not errors:
				errors = {'__all__': ['This scratch card has already been used. Please use a different PIN.']}
			response = {}
			response['message'] = errors['__all__'][0] if '__all__' in errors else "Please check the highlighted fields and try again"
			response['errors'] = errors
			return JsonResponse(response, status=400)
	try:
		booking = ExamBooking.objects.get(card_number=request.session['booking'])
		candidate = booking.id
		card_details = ScratchCard.objects.get(pin_no=request.session['booking'], used=True)
	except:
		booking = False
		card_details = False

	if booking and card_details:
		# context = {'form': ExamBookingForm(instance=booking)}
		return redirect(preview_booking, candidate )
		# return JSONResponse({ 'message': 'Booking already made' }, status=303)
	else:
		categories = Category.objects.all()
		sCategory = CategorySerializer(categories, many=True).data
		form = ExamBookingForm()
		category=Category.objects.get(id=request.session['category'])
		context = {'venues': ExamVenue.objects.all(), 'form':form, 'categories': sCategory, 'category':category}
	template = loader.get_template('core/booking.html')
	return HttpResponse(template.render(context, request))


def booking_edit(request, uuid):
	candidate = ExamBooking.objects.get(id=uuid)
	if request.POST:
		form = ExamBookingForm(request.POST, request.FILES or None, instance=candidate)
		if form.is_valid():
			candy = form.save(commit=False)
			candy.updated_at = timezone.now()
			candy.title = request.POST.get('title')
			candy.save()
			return redirect(booking_list)
		else:
			return render(request, 'core/booking_edit.html', {'form': form, 'candidate':candidate})
	else:
		form = ExamBookingForm(instance=candidate)
		return render(request, 'core/booking_edit.html', {'form': form, 'candidate': candidate})

def booking_verification_page(request):
	template = loader.get_template('custom/booking_verification.html')
	context = { 'title': 'Welcome to Drive' }
	return HttpResponse(template.render(context, request))

def preview_booking(request, uuid):
	booking = ExamBooking.objects.get(id=uuid)
	sBooking = BookingSerializer(booking).data
	exam_venue = ExamVenueSerializer(ExamVenue.objects.get(id=sBooking["exam_venue"])).data
	if request.session.has_key('candidate'):
		del request.session['candidate']
	if request.session.has_key('booking'):
		del request.session['booking']
	if request.session.has_key('category'):
		del request.session['category']
	return render(request, 'core/preview_booking.html', {'booking': sBooking, 'exam_venue': exam_venue, 'exam_date': booking.preffered_date })


def verify_booking(request):
	if request.method == 'POST':
		if 'voucher' in request.POST:
			try:
				card_details = ScratchCard.objects.get(pin_no=request.POST.get('pin_number'))
				if card_details:
					request.session['booking'] = card_details.pin_no
					return redirect(booking_page)
				else:
					messages.add_message(request, messages.WARNING, 'The scratch card number is not valid')
					messages.add_message(request, messages.WARNING, 'Please enter a valid scratch card number')
					return redirect(booking_verification_page)
			except ScratchCard.DoesNotExist:
				messages.add_message(request, messages.WARNING, 'The scratch card number is not valid')
				messages.add_message(request, messages.WARNING, 'Please enter a valid scratch card number')
				return redirect(booking_verification_page)
		elif 'pay_online' in request.POST:
			return redirect(payment)
		else:
			return HttpResponse(status=404)
	else:
		return HttpResponse(status=404)

def driving_test_page(request):
	if not request.session.has_key('candidate'):
		return redirect(candidate_verification_page)
	candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
	examParticipant = ExamParticipant.objects.get(examination_number=request.session['candidate'])
	template = loader.get_template('custom/driving_test.html')
	context = { 'title': candidate, 'exam_participant': examParticipant }
	return HttpResponse(template.render(context, request))

@csrf_exempt
def process_candidate_exam(request):
	if not request.session.has_key('candidate'):
		return HttpResponse(status=404)
	if request.method != 'POST':
		return HttpResponse(status=404)
	answerSet = json.loads(request.body.decode("utf-8"))
	if not answerSet:
		return HttpResponse(status=500)
	# print (answerSet)
	try:
		candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
		examParticipant = ExamParticipant.objects.get(examination_number=request.session['candidate'])
		booking = ExamBooking.objects.get(examination_number=request.session['candidate'])
		if examParticipant and candidate:
			if examParticipant.finished_test:
				return HttpResponse(status=201)
			exam_id = examParticipant.exam_id
			mExamQuestions = (Question.objects.filter(pk__in=[question["question_id"] for question in answerSet])
				.select_related('category')
				.prefetch_related(
					'answer_choices',
					'translated_questions',
					'translated_questions__translated_question_answer_choices'))
			smExamQuestions = QuestionSerializer(mExamQuestions, many=True)
			candidate_point = 0
			for eQuestion in smExamQuestions.data:
				eQuestion_id = eQuestion['id']
				answer_text = ''
				selected_choice_ids = []
				if eQuestion['question_type'] == 'scqt':
					for answer in answerSet:
						if eQuestion_id == answer['question_id']:
							if answer['selected_choice_ids']:
								selected_choice_ids = answer['selected_choice_ids']
							for option in eQuestion['answer_choices']:
								if option['is_answer']:
									if answer['selected_choice_ids'] and answer['selected_choice_ids'][0] == option['id']:
										candidate_point += 1 # Max Point
									break
							break
				elif eQuestion['question_type'] == 'mcqt':
					for answer in answerSet:
						if eQuestion_id == answer['question_id']:
							if answer['selected_choice_ids']:
								selected_choice_ids = answer['selected_choice_ids']
							sys_right_answer_count = 0
							user_right_answer_count = 0
							user_wrong_answer_count = 0
							for option in eQuestion['answer_choices']:
								if option['is_answer']:
									sys_right_answer_count+=1
									for user_selected_id in answer['selected_choice_ids']:
										if user_selected_id == option['id']:
											user_right_answer_count+=1
											break
							for user_selected_id in answer['selected_choice_ids']:
								for option in eQuestion['answer_choices']:
									if user_selected_id == option['id'] and not option['is_answer']:
										user_wrong_answer_count+=1
										break
							if user_right_answer_count > 0:
								candidate_point += abs(user_right_answer_count - user_wrong_answer_count) / sys_right_answer_count
							break
				else:
					pass
			mark_obj = ExamMark.objects.create(
			    exam=examParticipant.exam, 
			    exam_participant=examParticipant,
			    score=candidate_point
			)
			# questionable line here
			# r = requests.post("https://lacvis.com/DttExams/", data={'exam_no': request.session['candidate'], 'exam_score': candidate_point, 'pin': booking.card_number})
			examParticipant.finished_test = True
			examParticipant.save()
			return HttpResponse(status=200)
		else:
			return HttpResponse(status=404)
	except ExamQuestion.DoesNotExist:
		return HttpResponse(status=404)


def load_candidate_questions(request):
	if not request.session.has_key('candidate'):
		return HttpResponse(status=404)
	try:
		candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
		examParticipant = ExamParticipant.objects.select_related('exam', 'exam__category').get(
			examination_number=request.session['candidate'])
		if examParticipant and candidate:
			if not examParticipant.finished_test:
				exam = examParticipant.exam
				smExam = ExamSerializer(exam).data
				question_ids = list(Question.objects.filter(category_id=exam.category_id)
					.values_list('id', flat=True))
				number_of_question = min(exam.number_of_question, len(question_ids))
				questions = (Question.objects.filter(pk__in=sample(question_ids, number_of_question))
					.select_related('category')
					.prefetch_related(
						'answer_choices',
						'translated_questions',
						'translated_questions__translated_question_answer_choices'))
				smQuestion = QuestionSerializer(questions, many=True).data
				smExamQuestion = dict()
				smExamQuestion['exam'] = smExam
				smExamQuestion['questions'] = smQuestion
				return JSONResponse(smExamQuestion)
			else:
				
				return JSONResponse(json.dumps({'finished':'true'}))
		else:
			return HttpResponse(status=404)
	except ExamQuestion.DoesNotExist:
		return HttpResponse(status=404)

def load_candidate_exam_info(request):
	if not request.session.has_key('candidate'):
		return HttpResponse(status=404)
	try:
		candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
		if candidate:
			sCandidate = ExamBookingSerializer(candidate)
			return JSONResponse(sCandidate.data)
		else:
			return HttpResponse(status=404)
	except ExamQuestion.DoesNotExist:
		return HttpResponse(status=404)
		
def capture_photo(request):
	if not request.session.has_key('candidate'):
		return redirect(candidate_verification_page)
	base64Photo = request.POST.get("myphotodata", "")
	# binaryPhoto = b64decode(base64Photo)
	candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
	candidate.onsite_photo = base64Photo
	candidate.save()
	return redirect(driving_test_page)
	# setattr(candidate, model_field.name, ContentFile(binaryPhoto, examination_number + '.png'))

def candidate_verification_page(request):
	exam_type = request.GET.get('type')
	if not exam_type:
		exam_type = 'exam'
	if request.session.has_key('candidate'):
		try:
			examParticipant = ExamParticipant.objects.get(examination_number=request.session['candidate'])
			if examParticipant:
				if examParticipant.can_take_test and not examParticipant.finished_test:
					return redirect(photo_capture_page)
				if examParticipant.finished_test:
					return redirect(candidate_result_page)
				if not examParticipant.can_take_test:
					messages.info(request, "Sorry, your account has not been enabled to take a test yet. Please consult the admin for details")
					return redirect(candidate_verification_page)
			else:
				messages.info(request, "Sorry, your account has not been enabled to take a test yet. Please consult the admin for details")
				return redirect(candidate_verification_page)
		except ExamParticipant.DoesNotExist:
			return redirect(photo_capture_page)
	template = loader.get_template('custom/verify.html')
	context = { 'title': 'Welcome to Drive', 'type': exam_type }
	return HttpResponse(template.render(context, request))


def logout(request):
	try:
		if request.session.has_key('candidate'):
			del request.session['candidate']
		if request.session.has_key('booking'):
			del request.session['booking']
		if request.session.has_key('category'):
			del request.session['category']
		return redirect('/')
	except:
		pass
	return redirect('/')

def verify_candidate(request):
	if request.method == 'POST':
		try:
			examination_number = request.POST['examination_number']
			candidate = ExamBooking.objects.get(examination_number=examination_number)
			examParticipant = ExamParticipant.objects.get(examination_number=examination_number)
			if candidate:
				request.session['candidate'] = candidate.examination_number
				if examParticipant.can_take_test and not examParticipant.finished_test:
					return redirect(photo_capture_page)
				if examParticipant.finished_test:
					return redirect(candidate_result_page)
				if not examParticipant.can_take_test:
					messages.info(request, "Sorry, your account has not been enabled to take a test yet. Please consult the admin for details")
					return redirect(candidate_verification_page)
			else:
				messages.info(request, 'Invalid examination number')
				print('1')
				return redirect(candidate_verification_page)
		except ExamBooking.DoesNotExist:
			print('11')
			messages.info(request, 'Invalid examination number')
			return redirect(candidate_verification_page)
		except ExamParticipant.DoesNotExist:
			messages.info(request, 'Your exam is not ready yet, please try again later.')
			return redirect(candidate_verification_page)
	else:
		return HttpResponse(status=404)

def candidate_result_page(request):
	if request.session.has_key('candidate'):
		template = loader.get_template('custom/candidate_result.html')
		candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
		examParticipant = ExamParticipant.objects.get(examination_number=request.session['candidate'])
		if not candidate and not examParticipant:
			return redirect(candidate_verification_page)
		if not examParticipant.finished_test:
			return redirect(driving_test_page)
		candidate_mark = ExamMark.objects.filter(
			exam_participant=examParticipant.id, 
			exam=examParticipant.exam).latest('created_at')
		if not candidate_mark:
			return redirect(driving_test_page)
		score_in_percent = Decimal((candidate_mark.score / examParticipant.exam.number_of_question ) * 100).quantize(Decimal('.01'))
		sBooking = BookingSerializer(candidate).data
		exam_venue = ExamVenueSerializer(ExamVenue.objects.get(id=sBooking["exam_venue"])).data
		# Build a signed verification URL for QR code
		payload = f"{candidate.examination_number}:{candidate_mark.id}".encode()
		sig = hmac.new(settings.SECRET_KEY.encode(), payload, hashlib.sha256).hexdigest()
		verify_path = reverse('verify_result')
		verify_url = request.build_absolute_uri(f"{verify_path}?exam_no={candidate.examination_number}&mark_id={candidate_mark.id}&sig={sig}")
		context = { 
			"candidate":  candidate, "exam": examParticipant, 
			"candidate_gender":  "Male" if candidate.gender == 'M' else "Female",
			"canditate_date_of_birth": candidate.date_of_birth,
			"score_in_percent": score_in_percent,
			"verdict": "pass" if score_in_percent > 45 else "fail",
			"verdict_message": "Congratulations" if score_in_percent > 45 else "Sorry, you could not make it to the cut-off mark. Please try again.",
			"nQUestions": examParticipant.exam.number_of_question,
			"score": candidate_mark, 'exam_venue': exam_venue,
			"verify_url": verify_url,
		}
		# context = {'candidate': 'retnan'}
		return HttpResponse(template.render(context, request))
	else:
		messages.add_message(request, messages.ERROR, 'Please authenticate to continue')
		return redirect(candidate_verification_page)
	
def verify_result(request):
	# Public endpoint to verify a candidate result via signed QR code
	exam_no = request.GET.get('exam_no')
	mark_id = request.GET.get('mark_id')
	sig = request.GET.get('sig')
	status = 'invalid'
	message = 'Invalid or tampered verification link.'
	context = {'status': status, 'message': message}
	if not (exam_no and mark_id and sig):
		return render(request, 'custom/verify_result.html', context)
	try:
		expected = hmac.new(settings.SECRET_KEY.encode(), f"{exam_no}:{mark_id}".encode(), hashlib.sha256).hexdigest()
		if not hmac.compare_digest(sig, expected):
			return render(request, 'custom/verify_result.html', context)
		candidate = ExamBooking.objects.get(examination_number=exam_no)
		examParticipant = ExamParticipant.objects.get(examination_number=exam_no)
		mark = ExamMark.objects.get(id=mark_id, exam_participant=examParticipant)
		score_in_percent = Decimal((mark.score / examParticipant.exam.number_of_question ) * 100).quantize(Decimal('.01'))
		sBooking = BookingSerializer(candidate).data
		exam_venue = ExamVenueSerializer(ExamVenue.objects.get(id=sBooking["exam_venue"]))
		verdict = "pass" if score_in_percent > Decimal(45) else "fail"
		status = 'valid'
		message = 'Result verified successfully.'
		context = {
			'status': status,
			'message': message,
			'candidate': candidate,
			'exam': examParticipant,
			'exam_venue': exam_venue.data if hasattr(exam_venue, 'data') else exam_venue,
			'score_in_percent': score_in_percent,
			'score': mark,
			'verdict': verdict,
		}
		return render(request, 'custom/verify_result.html', context)
	except Exception:
		return render(request, 'custom/verify_result.html', context)


def photo_capture_page(request):
	if request.session.has_key('candidate'):
		try:
			examParticipant = ExamParticipant.objects.get(examination_number=request.session['candidate'])
			if examParticipant:
				if examParticipant.can_take_test and not examParticipant.finished_test:
					candidate = ExamBooking.objects.get(examination_number=request.session['candidate'])
					if candidate and candidate.photo:
						# No need to capture face as directed by MD
						return redirect(driving_test_page)
					return redirect(driving_test_page) # TODO: Remove this LINE when photo verification is needed.
					template = loader.get_template('custom/photo.html')
					candidate = ExamBooking.objects.filter(examination_number=request.session['candidate'])
					context = { 'candidate':  candidate}
					return HttpResponse(template.render(context, request))
				if examParticipant.finished_test:
					return redirect(candidate_result_page)
				if not examParticipant.can_take_test:
					messages.info(request, "Sorry, your account has not been enabled to take a test yet. Please consult the admin for details")
					return redirect(candidate_verification_page)
			else:
				messages.info(request, "Sorry, your account has not been enabled to take a test yet. Please consult the admin for details")
				return redirect(candidate_verification_page)
		except ExamParticipant.DoesNotExist:
			return redirect(photo_capture_page)
	else:
		messages.add_message(request, messages.ERROR, 'Please authenticate to continue')
		return redirect(candidate_verification_page)


@login_required
@staff_member_required
def cat_list(request):
	mCategories = Category.objects.all()
	smCategories = CategorySerializer(mCategories, many=True)
	return render(request, 'core/category_list.html', {'categories':smCategories.data})


def cat_delete(request, uuid):
	try:
		cat = Category.objects.get(id=uuid)
		cat.delete()
	except:
		cat = None
	data = dict()
	mCategories = Category.objects.filter()
	smCategories = CategorySerializer(mCategories, many=True).data
	context = {'categories': smCategories}
	data['list'] = render_to_string('core/partial_category_list.html', context)
	return JSONResponse(data)


@login_required
@staff_member_required
def cat_detail(request, uuid):
	try:
		mCategory = Category.objects.get(id=uuid)
	except Category.DoesNotExist:
		return HttpResponse(status=404)

	smCategory = CategorySerializer(mCategory)
	return render(request, 'core/category_detail.html', {'category': smCategory.data})

@login_required
@staff_member_required
def category_create(request):
	if request.method == "POST":
		category_form = CategoryForm(request.POST)
		category_form.save()
		return redirect(cat_list)
	else:
		category_form = CategoryForm()
		return render(request, 'core/category_create.html', {'category_form': category_form})

@login_required
@staff_member_required
def cat_edit(request, uuid):
	try:
		mCategory = Category.objects.get(id=uuid)
	except:
		return HttpResponse(status=404)

	if request.method == 'POST':
		category_form = CategoryForm(request.POST, instance=mCategory)
		if category_form.is_valid():
			category = category_form.save()
			return redirect(cat_list)
		else:
			return render(request, 'core/category_edit.html', {'category_form':category_form})
	else:
		category_form = CategoryForm(instance=mCategory)
		return render(request, 'core/category_edit.html', {'category_form': category_form})

@login_required
@staff_member_required
def exam_create_web(request):
	if request.method == 'POST':
		exam_form = ExamForm(request.POST)
		if exam_form.is_valid():
			exam = exam_form.save()
			return redirect(exam_list_web)
		else:
			return render(request, 'core/exam_create.html', {'exam_form': exam_form})
	exam_form = ExamForm()
	return render(request, 'core/exam_create.html', {'exam_form': exam_form})


@login_required
@staff_member_required
def exam_edit_web(request, uuid):
	exam = Exam.objects.get(id=uuid)
	exam_form = ExamForm(instance=exam)
	if request.method == 'POST':
		exam_form = ExamForm(request.POST, instance=exam)
		if exam_form.is_valid():
			exam = exam_form.save()
			return redirect(exam_list_web)
		else:
			return render(request, 'core/exam_edit.html', {'exam_form': exam_form})
	return render(request, 'core/exam_edit.html', {'exam_form': exam_form})



@login_required
@staff_member_required
def exam_list_web(request):
	mExam = Exam.objects.select_related('category')
	smExam = ExamSerializer(mExam, many=True)
	return render(request, 'core/exam_list.html', {'exams':smExam.data})

@login_required
@staff_member_required
def exam_detail_web(request, uuid):
	mExam = Exam.objects.select_related('category').get(id=uuid)
	smExam = ExamSerializer(mExam).data
	mExamQuestions = (ExamQuestion.objects.filter(exam=mExam)
		.select_related('exam', 'exam__category', 'question', 'question__category')
		.prefetch_related(
			'question__answer_choices',
			'question__translated_questions',
			'question__translated_questions__translated_question_answer_choices'))
	smExamQuestions = ExamQuestionSerializer(mExamQuestions, many=True).data
	context = {
		'exam': smExam,
		'questions': smExamQuestions,
	}
	return render(request, 'core/exam_detail.html', context)


def option_form_api(request, num):
	optionformset = modelformset_factory(QuestionOption, extra=int(num), fields=('question_option', 'is_answer', \
		'audio', 'image'), widgets={'question_option': forms.Textarea(attrs={'rows': 5})})
	formset = optionformset(queryset=QuestionOption.objects.none())
	context = {'formset':formset}
	data = {}
	data['optionform'] = render_to_string('core/option_form_set.html', context)
	return JSONResponse(data)


@login_required
@staff_member_required
def question_create_web(request):
	form = QuestionForm()
	optionformset = modelformset_factory(QuestionOption, extra=2, fields=('question_option', 'is_answer',
																		  'audio', 'image'), widgets={'question_option': forms.Textarea(attrs={'rows': 5})})
	formset = optionformset(queryset=QuestionOption.objects.none())
	if request.method == "POST":
		# have to edit total number of formsets
		# set request.PPOST to mutable
		request.POST._mutable = True
		form = QuestionForm(request.POST, request.FILES)
		extras = int(request.POST.get('optionNumber'))
		# edit the value of formset count
		request.POST['form-TOTAL_FORMS'] = extras
		optionformset = modelformset_factory(QuestionOption, extra=extras, fields=('question_option', 'is_answer',
																		  'audio', 'image'), widgets={'question_option': forms.Textarea(attrs={'rows': 5})})
		formset = optionformset(request.POST, request.FILES or None)
		if form.is_valid() and formset.is_valid():
			question = form.save()
			for form in formset:
				option = form.save(commit=False)
				option.question = question
				option.save()
			return redirect(question_list_web)
		else:
			return render(request, "core/question_create.html", {'form': form, 'formset': formset})
	return render(request, "core/question_create.html", {'form': form, 'formset': formset})


@login_required
@staff_member_required
def translate_question(request, uuid):
	question = Question.objects.get(id=uuid)
	# smQuestion = QuestionSerializer(question).data
	form = TranslatedQuestionForm()
	options = QuestionOption.objects.filter(question__id=uuid)
	optionformset = modelformset_factory(TranslatedQuestionOption, extra=len(options), fields=('translated_question_option', 'is_answer', 'image', 'audio'), widgets={'translated_question_option': forms.Textarea(attrs={'rows': 5})})
	formset = optionformset(queryset=TranslatedQuestionOption.objects.none())
	payload = zip(formset, options)
	if request.method == 'POST':
		form = TranslatedQuestionForm(request.POST, request.FILES or None)
		formset = optionformset(request.POST,  request.FILES or None)
		payload = zip(formset, options)
		if form.is_valid() and formset.is_valid():
			translated_question = form.save(commit=False)
			translated_question.question = question
			translated_question.save()
			for form in formset:
				translated_option = form.save(commit=False)
				translated_option.question = translated_question
				translated_option.language = translated_question.language
				translated_option.save()
			return redirect(question_detail_web, question.id)
		else:
			return render(request, 'core/question_translate.html', {'form': form, 'question': question, "payload": payload, "formset": formset})
	else:
		return render(request, 'core/question_translate.html', {'form': form, 'question': question, "payload": payload, "formset": formset})


@login_required
@staff_member_required
def translate_question_edit(request, uuid):
	translated_question = TranslatedQuestion.objects.get(id=uuid)
	question = Question.objects.get(id=translated_question.question.id)
	translated_options = TranslatedQuestionOption.objects.filter(question__id=uuid)
	options = QuestionOption.objects.filter(question=question)
	form = TranslatedQuestionForm(instance=translated_question)
	optionformset = modelformset_factory(TranslatedQuestionOption, extra=len(options), fields=('translated_question_option', 'is_answer', 'image', 'audio'), widgets={'translated_question_option': forms.Textarea(attrs={'rows': 5})})
	formset = optionformset(queryset=translated_options)
	print(formset)
	payload = zip(formset, options)
	if request.method == 'POST':
		form = TranslatedQuestionForm(request.POST, request.FILES or None, instance=translated_question)
		formset = optionformset(request.POST,  request.FILES or None, queryset=translated_options)
		if form.is_valid() and formset.is_valid():
			translated_question = form.save(commit=False)
			translated_question.question = question
			translated_question.save()
			for form in formset:
				translated_option = form.save(commit=False)
				translated_option.question = translated_question
				translated_option.language = translated_question.language
				translated_option.save()
			return redirect(question_detail_web, question.id)
		else:
			payload = zip(formset, options)
			return render(request, 'core/question_translate.html', {'form': form, 'question': question, "payload": payload, "formset": formset})
	else:
		return render(request, 'core/question_translate.html', {'form': form, 'question': question, "payload": payload, "formset": formset})


@login_required
@staff_member_required
def question_list_web(request):
	categories = Category.objects.all()
	return render(request, 'core/question_list.html', {'categories': categories})

@login_required
@staff_member_required
def question_detail_web(request, uuid):
	mQuestion = Question.objects.get(id=uuid)
	smQuestion = QuestionSerializer(mQuestion)
	return render(request, 'core/question_detail.html', {'question': smQuestion.data})

@login_required
@staff_member_required
def question_edit_web(request, uuid):
	question = Question.objects.get(id=uuid)
	options = QuestionOption.objects.filter(question__id=uuid)
	form = QuestionForm(instance=question)
	context = {
		'form': form,
		'options': options,
		'question': question,
	}
	return render(request, 'core/question_edit.html',context)


def question_edit_api(request, uuid):
	question = Question.objects.get(id=uuid)
	data = dict()
	if request.method == "POST":
		form = QuestionForm(request.POST, request.FILES or None, instance=question)
		if form.is_valid():
			question = form.save()
			context = {'question': question }
			data['question'] = render_to_string('core/partial_question_detail.html', context)
			return JSONResponse(data)
		else:
			context = {'form': form, "question": question}
			data['question'] = render_to_string('core/partial_question_edit.html', context)
			return JSONResponse(data)


@csrf_exempt
def option_create_api(request, uuid):
	question = Question.objects.get(id=uuid)
	data = dict()
	path = request.path
	if request.POST:
		form = OptionForm(request.POST, request.FILES or None)
		if form.is_valid():
			option = form.save(commit=False)
			option.question = question
			option.save()
			return redirect(option_list_api, uuid)
	else:
		form = OptionForm()
		context = {'form':form, 'path': path}
		data['option'] = render_to_string('core/partial_option_form.html', context)
		return JSONResponse(data)


@csrf_exempt
def option_edit_api(request, uuid):
	data = dict()
	option = QuestionOption.objects.get(id=uuid)
	if request.method == "GET":
		path = request.path
		optionForm = OptionForm(instance=option)
		context = {'form': optionForm, 'path': path}
		data['option'] = render_to_string('core/partial_option_edit.html', context)
		return JSONResponse(data)
	else:
		optionForm = OptionForm(request.POST, request.FILES or None, instance=option)
		if optionForm.is_valid():
			option=optionForm.save()
			return redirect(option_list_api, option.question.id)
		else:
			return redirect(option_list_api, option.question.id)

def option_list_api(request, uuid):#question uuid
	options = QuestionOption.objects.filter(question__id=uuid)
	data = dict()
	context = {'options':options}
	data['option'] = render_to_string('core/partial_option_list.html', context)
	return JSONResponse(data)


def option_delete_api(request, uuid):
	data = dict()
	option = QuestionOption.objects.get(id=uuid)
	question = option.question.id
	option.delete()
	return redirect(option_list_api, question)

@login_required
@staff_member_required
def add_exam_question(request, uuid):
	if request.method == 'GET':
		mExam = Exam.objects.get(id=uuid)
		mQuestion = Question.objects.filter(category=mExam.category).exclude(exam_questions__exam__id=uuid)
		smExam = ExamSerializer(mExam).data
		smQuestions = QuestionSerializer(mQuestion, many=True).data
		return render(request, 'core/addquestions.html', {'exam': smExam, 'questions': smQuestions})
	elif request.method == 'POST':
		mExam = Exam.objects.get(id=uuid)
		questions = request.POST.getlist('question[]')
		exam_questions = ExamQuestion.objects.bulk_create([
			ExamQuestion(exam=mExam, question=Question.objects.get(id=x)) for x in questions
		])
		return redirect(exam_detail_web, uuid)

@csrf_exempt
def category_list(request):
	try:
		mCategory = Category.objects.all()
	except Category.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smCategory = CategorySerializer(mCategory, many=True)
		return JSONResponse(smCategory.data)
	else:
		return HttpResponse(status=404)


@csrf_exempt
def exam_list(request):
	try:
		mExam = Exam.objects.all()
	except Exam.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExam = ExamSerializer(mExam, many=True)
		return JSONResponse(smExam.data)
	else:
		return HttpResponse(status=404)

@csrf_exempt
def exam_detail(request, pk):
	try:
		mExam = Exam.objects.get(pk=pk)
	except Exam.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExam = ExamSerializer(mExam)
		return JSONResponse(smExam.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		smExam = ExamSerializer(mExam, data=data)
		if smExam.is_valid():
			smExam.save()
			return HttpResponse(smExam.data)
		return JSONResponse(smExam.errors, status=400)
	elif request.method == 'DELETE':
		mExam.delete()
		return HttpResponse(status=204)


@csrf_exempt
def exam_participant_list(request):
	try:
		mExamParticipant = ExamParticipant.objects.all()
	except ExamParticipant.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExamParticipant = ExamParticipantSerializer(mExamParticipant, many=True)
		return JSONResponse(smExamParticipant.data)
	else:
		return HttpResponse(status=404)
		
@csrf_exempt
def exam_participant_detail(request, pk):
	try:
		mExamParticipant = ExamParticipant.objects.get(pk=pk)
	except ExamParticipant.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExamParticipant = ExamParticipantSerializer(mExamParticipant)
		return JSONResponse(smExamParticipant.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		smExamParticipant = ExamParticipantSerializer(mExamParticipant, data=data)
		if smExamParticipant.is_valid():
			smExamParticipant.save()
			return HttpResponse(smExamParticipant.data)
		return JSONResponse(smExamParticipant.errors, status=400)
	elif request.method == 'DELETE':
		mExamParticipant.delete()
		return HttpResponse(status=204)

@csrf_exempt
def exam_question_list(request):
	try:
		exam = request.GET.get('exam_id', default=False)
		if exam:
			mExamQuestion = ExamQuestion.objects.filter(exam=exam)
		else:
			mExamQuestion = ExamQuestion.objects.all()
	except ExamQuestion.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExamQuestion = ExamQuestionSerializer(mExamQuestion, many=True)
		return JSONResponse(smExamQuestion.data)
	else:
		return HttpResponse(status=404)
		
@csrf_exempt
def exam_question_detail(request, pk):
	try:
		mExamQuestion = ExamQuestion.objects.get(pk=pk)
	except ExamQuestion.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExamQuestion = ExamQuestionSerializer(mExamQuestion)
		return JSONResponse(smExamQuestion.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		smExamQuestion = ExamQuestionSerializer(mExamQuestion, data=data)
		if smExamQuestion.is_valid():
			smExamQuestion.save()
			return HttpResponse(smExamQuestion.data)
		return JSONResponse(smExamQuestion.errors, status=400)
	elif request.method == 'DELETE':
		mExamQuestion.delete()
		return HttpResponse(status=204)

@csrf_exempt
def exam_booking_list(request):
	try:
		mExamBooking = ExamBooking.objects.all()
	except ExamBooking.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExamBooking = ExamBookingSerializer(mExamBooking, many=True)
		return JSONResponse(smExamBooking.data)
	else:
		return HttpResponse(status=404)
		
@csrf_exempt
def exam_booking_detail(request, pk):
	try:
		mExamBooking = ExamBooking.objects.get(pk=pk)
	except ExamBooking.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smExamBooking = ExamBookingSerializer(mExamBooking)
		return JSONResponse(smExamBooking.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		smExamBooking = ExamBookingSerializer(mExamBooking, data=data)
		if smExamBooking.is_valid():
			smExamBooking.save()
			return HttpResponse(smExamBooking.data)
		return JSONResponse(smExamBooking.errors, status=400)
	elif request.method == 'DELETE':
		mExamBooking.delete()
		return HttpResponse(status=204)



@csrf_exempt
def question_list(request):
	try:
		mQuestion = Question.objects.all()
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smQuestion = QuestionSerializer(mQuestion, many=True)
		return JSONResponse(smQuestion.data)
	else:
		return HttpResponse(status=404)
		
@csrf_exempt
def question_detail(request, pk):
	try:
		mQuestion = Question.objects.get(pk=pk)
	except Question.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		smQuestion = QuestionSerializer(mQuestion)
		return JSONResponse(smQuestion.data)
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		smQuestion = QuestionSerializer(mQuestion, data=data)
		if smQuestion.is_valid():
			smQuestion.save()
			return HttpResponse(smQuestion.data)
		return JSONResponse(smQuestion.errors, status=400)
	elif request.method == 'DELETE':
		mQuestion.delete()
		return HttpResponse(status=204)

@csrf_exempt
def create_pin(request):
	if request.method == 'POST':
		pin = request.POST.get('pin')
		_type = request.POST.get('type')
		amount = request.POST.get('amount')
		if pin and amount:
			category = Category.objects.filter(title=_type)
			if not category:
			    category = Category.objects.filter().first()
			    if not category:
			        return JSONResponse({
    					'status': 'error',
    					'message': 'Invalid PIN TYPE, try "class A"'
    				})
# 			if len(pin) != 11:
# 				return JSONResponse({
# 					'code': 400,
# 					'status': 'error',
# 					'message': 'Invalid PIN length, pin should be a number which is exactly 11 digits'
# 				})
			p, created = ScratchCard.objects.get_or_create(
				pin_no=request.POST['pin'], category=category[0], price=request.POST['amount']
			)
			if not created:
				return JSONResponse({
					'code': 200,
					'status': 'Success',
					'message': 'PIN Already exists and can be used to book for TEST'
				})
			return JSONResponse({
				'code': 200,
				'status': 'Success',
				'message': 'New PIN was successfully created and can be used to book for TEST'
			})
		else:
			return JSONResponse({
				'code': 400,
				'status': 'Failed',
				'message': 'Please Input valid PIN, AMOUNT or TYPE'
			})
	else:
		return JSONResponse({
			'code': 300,
			'status': 'Failed',
			'message': "bad request! Only POST method supported"
		})
