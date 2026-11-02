from django.shortcuts import render
from custom import models
from custom import serializers
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .mixins import DttViewsetMixin
from django.http import HttpResponse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.db.utils import IntegrityError
from rest_framework.schemas import ManualSchema
from .import schemas

# Create your views here.
class BaseAPIView(APIView):
    permission_classes = (IsAuthenticated,)


class ExamCenterViewSet(DttViewsetMixin, ModelViewSet):
    api_model = models.ExamVenue
    list_serializer = serializers.ExamVenueSerializer
    serializer_class = serializers.ExamVenueSerializer

    def get_queryset(self):
        """query by state"""
        if 'state' in self.request.query_params:
            state = self.request.query_params.get('state')
            return self.api_model.objects.filter(state=state)
        else:
            return super(ExamCenterViewSet, self).get_queryset()


class ExamCategoryViewSet(DttViewsetMixin, ModelViewSet):
    api_model = models.Category
    list_serializer = serializers.CategorySerializer
    serializer_class = serializers.CategorySerializer

class GenderView(APIView):
    """
    List all gender
    """
    def get(self, request):
        gender = models.GENDER
        return Response(gender)

class TestTypeView(APIView):
    def get(self, request):
        tests = models.TEST_DRIVE_TYPE
        return Response(tests)


class stateView(APIView):
    """
    List of all states
    """
    def get(self, request, format=None):
        states = models.STATE
        return Response(states)


class LanguageView(APIView):
    """
    List of all languages
    """
    def get(self, request, format=None):
        languages = models.LANG_CHOICES
        return Response(languages)


class AtomicMixin(object):
    def dispatch(self, request, *args, **kwargs):
        with transaction.atomic():
            return super(AtomicMixin, self).dispatch(request, *args, **kwargs)


class ExamBookingView(APIView):
    schema = schemas.booking_endpoint
    def post(self, request, *args, **kwargs):
        sid = transaction.savepoint()
        data = request.data.copy()
        form = serializers.CustomBookingSerializer(data=request.data)
        if form.is_valid():
            # with transaction.atomic():
            card_number = form.data.get('card_number')
            examination_number = form.data.get('examination_number')
            exam_category = form.data.get('exam_category')
            first_name = form.data.get('first_name')
            last_name = form.data.get('last_name')
            category = models.Category.objects.get(pk=exam_category)
            description = "{} - {} for {}".format(first_name, last_name, category.title)
            # check if scratch card or exam nuber already exists
            card = models.ScratchCard.objects.filter(pin_no=card_number)
            if card.exists():
                return Response({
                    'status': False,
                    'message': 'card_number already exists',
                }, status=400)
            part = models.ExamParticipant.objects.filter(examination_number=examination_number)
            if part.exists():
                return Response({
                    'status': False,
                    'message': 'examination_number already exists',
                }, status=400)
            #...............
            #.........
            scratch_card = models.ScratchCard.objects.create(
                pin_no=card_number,
                category_id=exam_category,
                description=description,
                used=True
            )
            try:
                exam = models.Exam.objects.filter(category=category).latest('updated_at')
            except:
                scratch_card.delete()
                transaction.savepoint_rollback(sid)
                data = {}
                data['message'] = "Exam not ready for {}".format(category.title)
                return Response(data, status=400)
            # create the booking
            d = form.data
            # why not use request.data here too
            """
            booking = serializers.BookingSerializer(data=dict(
                title=d['title'],
                first_name=d['first_name'],
                last_name=d['last_name'],
                middle_name=d['middle_name'],
                state=d['state'],
                mobile_number=d['mobile_number'],
                email_address=d['email_address'],
                address=d['address'],
                date_of_birth=d['date_of_birth'],
                gender=d['gender'],
                preffered_date=d['preffered_date'],
                drive_test_type=d['drive_test_type'],
                exam_preferred_language=d['exam_preferred_language'],
                exam_venue=d['exam_venue'],
                card_number=d['card_number'],
                photo=d['photo'])
            )
            """
            booking = serializers.BookingSerializer(data=request.data)
            if booking.is_valid():
                candidate = booking.save()
                candidate.examination_number=d['examination_number']
                candidate.save()
            else:
                transaction.savepoint_rollback(sid)
                scratch_card.delete()
                print('rolled back the transaction')
                return Response({
                    'status': False,
                    'message': 'Please correct the errors below and try again',
                    'errors': booking.errors
                }, status=400)
            # create exam participant for that category
            participant = models.ExamParticipant.objects.create(exam=exam, examination_number=d['examination_number'])
            # commit transaction
            transaction.savepoint_commit(sid)
            return Response({
                'status': True,
                'message': 'Exam booking successfully created for candidate no {} on {}'.format(d['examination_number'], d['preffered_date']),
                'data': booking.data
            }, status=201)
        else:
            return Response({
                'status': False,
                'message': 'Please correct the errors below and try again',
                'errors': form.errors
            }, status=400)

        