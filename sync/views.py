from django.shortcuts import render
from custom.views import JSONResponse
import requests
from .models import Sync
from django.core import serializers
import itertools
from custom.models import ExamBooking, ExamVenue, ScratchCard, Payment
from exam.models import Exam, ExamMark, ExamParticipant, ExamAnswerChoice, ExamAnswerText, ExamQuestion
from question_bank.models import *
from ndtt.settings import REMOTE_URL, BASE_DIR
import json
from django.views.decorators.csrf import csrf_exempt
import os, shutil
import zipfile
from io import BytesIO
from django.db import transaction
from django.http import HttpResponse

@csrf_exempt
def getfiles(request):
    # Files (local path) to put in the .zip
    # FIXME: Change this (get paths from DB etc)
    filenames = json.loads(request.POST.get('filenames'))

    # Open StringIO to grab in-memory ZIP contents
    s = BytesIO()
    with zipfile.ZipFile(s, "w") as zp:
        for f in filenames:
            try:
                zp.write(f[1:], compress_type = zipfile.ZIP_DEFLATED)
            except:
                continue

# Grab ZIP file from in-memory, make response with correct MIME-type
    resp = HttpResponse(s.getvalue(), content_type = "application/zip")
    # ..and correct content-disposition
    resp['Content-Disposition'] = 'attachment; filename=%s' % "remote_files"

    return resp


def index(request):
    return render(request, 'core/sync_page.html', {})

@csrf_exempt
def identify_center(request):
    if request.method == "POST":
        email = request.POST.get('email')
        code = request.POST.get('code')
        password = request.POST.get('password')
        destination = request.POST.get('destination')
        try:
            center = ExamVenue.objects.filter(email=email).filter(code=code).first()
        except:
            response = JSONResponse({'found': 'false'})
            # response.__setitem__("Content-type", "application/json")
            # response.__setitem__("Access-Control-Allow-Origin", "*")
            return response
        if center:
            try:
                last_sync = Sync.objects.filter(destination=destination).filter(center=center).latest('last_sync')
                last_sync = last_sync.last_sync
            except:
                last_sync = '2017-01-01 00:00:00'
            response = JSONResponse({'center': str(center.id), 'last_sync': last_sync, 'found':'true'})
            # response.__setitem__("Content-type", "application/json")
            # response.__setitem__("Access-Control-Allow-Origin", "*")
            return response
        else:
            response = JSONResponse({'found':'false'})
            # response.__setitem__("Content-type", "application/json")
            # response.__setitem__("Access-Control-Allow-Origin", "*")
            return response
    else:
        return render(request, 'core/confirm_center.html', {'remote': REMOTE_URL})


def get_remote_data(request):
    last_sync = request.GET.get('last_sync')
    center = request.GET.get('center')
    exams = Exam.objects.filter(updated_at__gte=last_sync)
    bookings = ExamBooking.objects.filter(updated_at__gte=last_sync).filter(exam_venue__id=center)
    participants = ExamParticipant.objects.filter(updated_at__gte=last_sync)
    participants = [x for x in participants for y in bookings if x.examination_number==y.examination_number]
    categories = Category.objects.filter()
    venue = ExamVenue.objects.filter(id=center)
    # payments = Payment.objects.filter()#(updated_at__gte=last_sync)
    combo = [categories, venue, exams, bookings, participants]
    flat = list(itertools.chain.from_iterable(combo))
    bundle = serializers.serialize("json", flat, indent=3)
    return HttpResponse(bundle)


def get_local_data(last_sync):
    marks = ExamMark.objects.filter(updated_at__gte=last_sync)
    answers = ExamAnswerText.objects.filter(updated_at__gte=last_sync)
    choices = ExamAnswerChoice.objects.filter(updated_at__gte=last_sync)
    bookings = ExamBooking.objects.filter(updated_at__gte=last_sync)
    participants = ExamParticipant.objects.filter(updated_at__gte=last_sync)
    combo = [marks, answers, choices, bookings, participants]
    flat = list(itertools.chain.from_iterable(combo))
    bundle = serializers.serialize("json", flat, indent=3)
    return bundle


def perform_sync(retval):
    created, updated = 0, 0
    for obj in serializers.deserialize("json", retval, indent=3):
    
        # Get model info
        model_class = obj.object.__class__
        obj_id = obj.object.id
        manager = model_class._default_manager
    
        try:
            # Get the existing object
            existing_obj = model_class.objects.get(id=obj_id)
    
            # Check the timestamps
            date_existing = existing_obj.updated_at
            date_imported = obj.object.updated_at
            if date_imported > date_existing:
                # Update fields
                for field in obj.object._meta.fields:
                    if field.editable and not field.primary_key and not field.unique:
                        imported_val = getattr(obj.object, field.name)
                        existing_val = getattr(existing_obj, field.name)
                        if existing_val != imported_val:
                            setattr(existing_obj, field.name, imported_val)
                updated += 1
                existing_obj.save()
        except:
            obj.save()
            created += 1

    return created, updated

@csrf_exempt
def do_remote_sync(request):
    bundle = request.body
    created, updated = perform_sync(bundle)
    return JSONResponse({'created': created, 'updated': updated})

@transaction.atomic
def sync_online_to_local(request):
    last_sync = request.GET.get('last_sync')
    center = request.GET.get('center')
    bundle = requests.get(REMOTE_URL + 'perform/local/sync/?center=' + center + '&last_sync=' + last_sync).text
    bundle = json.loads(json.dumps(bundle))
    created, updated = perform_sync(bundle)

    response = JSONResponse({'created': created, 'updated': updated})
    # response.__setitem__("Content-type", "application/json")
    # response.__setitem__("Access-Control-Allow-Origin", "*")
    center = request.GET.get('center')
    destination = request.GET.get('destination')
    m = requests.get(REMOTE_URL + 'memorize/?destination=' + destination + '&center=' + center)
    return response


@csrf_exempt
@transaction.atomic
def sync_local_to_online(request):
    last_sync = request.GET.get('last_sync')
    bundle = get_local_data(last_sync)
    res = requests.post(REMOTE_URL + 'perform/online/sync/', data=bundle)
    data = res.json()
    if res.status_code == 200:
        response = JSONResponse(data)
        # response.__setitem__("Content-type", "application/json")
        # response.__setitem__("Access-Control-Allow-Origin", "*")
        center = request.GET.get('center')
        destination = request.GET.get('destination')
        m = requests.get(REMOTE_URL + 'memorize/?destination=' + destination + '&center=' + center)
        return response
    else:
        response = JSONResponse({'data': 'sync not complete'})
        # response.__setitem__("Content-type", "application/json")
        # response.__setitem__("Access-Control-Allow-Origin", "*")
        return response


def memorize(request):
    center = request.GET.get('center')
    destination = request.GET.get('destination')
    Sync.objects.create(center_id=center, destination=destination)
    return JSONResponse(status=200, data={})
