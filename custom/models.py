from django.db import models
import uuid, random, os
from exam.models import Exam, ExamQuestion, Category, ExamParticipant

from django.utils.deconstruct import deconstructible
# Create your models here.

ENGLISH = 'en'
HAUSA = 'ho'
YORUBA = 'yo'
IGBO = 'ig'
PIDGIN = 'pg'
LANG_CHOICES = ( 
	(ENGLISH, 'English'), 
	(HAUSA, 'Hausa'), 
	(YORUBA, 'Yoruba'), 
	(IGBO, 'Igbo'),
	(PIDGIN, 'Pidgin'))


STATE = (('ABIA', 'Abia'), ('ADAMAWA', 'Adamawa'), ('AKWA IBON', 'Akwa Ibom'), ('ANAMBRA', 'Anambra'),\
('BAUCHI', 'Bauchi'),('BAYELSA', 'Bayelsa'),('BENUE', 'Benue'),('BORNO', 'Borno'),('CROSS RIVER', 'Cross River'),\
('DELTA', 'Delta'),('EBONYI', 'Ebonyi'),('EDO', 'Edo'),('EKITI', 'ekiti'),('ENUGU', 'Enugu'),('FCT', 'FCT'), ('GOMBE', 'Gombe'),\
('IMO', 'Imo'),('JIGAWA', 'Jigawa'),('KADUNA', 'Kaduna'), ('KANO', 'kano'),('KASTINA', 'Kastina'),('KEBBI', 'Kebbi'),\
('KOGI', 'Kogi'),('KWARA', 'Kwara'),('LAGOS', 'Lagos'),('NASSARAWA', 'Nassarawa'),('NIGER', 'Niger'),('ONDO', 'Ondo'),\
('OGUN', 'Ogun'),('OSUN', 'Osun'),('OYO', 'Oyo'),('PLATEAU', 'Plateau'),('RIVERS', 'Rivers'),('SOKOTO', 'Sokoto'),\
('TARABA', 'Taraba'),('YOBE', 'Yobe'),('ZAMFARA', 'Zamfara'))

GENDER = (('M', 'Male'), ('F', 'Female'))
TEST_DRIVE_TYPE = (('new', 'New'), ('renew', 'Re-New'))

def generate_pin_number():
	result = ''
	for x in range(1, 12):
		result += str(random.randint(0, 9))
	return result


class ScratchCard(models.Model):
	"""docstring for ScratchCard"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	used = models.BooleanField(default=False)
# 	amount = models.DecimalField(max_digits=15, decimal_places=2, null=True)
	pin_no = models.CharField(max_length=50, unique=True, editable=False, default=generate_pin_number)
	price = models.CharField(max_length=50, null=True)
	category = models.ForeignKey(Category, related_name="scratch_card")
	description = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	updated_at = models.DateTimeField(auto_now=True, null=True)

	def __str__(self):
		return '%s' % (self.pin_no)
	
	@property
	def amount(self):
		return self.category.fees
	
	class Meta:
		ordering = ('-created_at',)


class ExamVenue(models.Model):
	"""Exam Venue Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	exam_venue = models.CharField(max_length=200)
	state = models.CharField(max_length=20, choices=STATE)
	code = models.CharField(max_length=10)
	email = models.EmailField()
	mobile_number = models.CharField(max_length=15)
	password = models.CharField(max_length=300)
	address = models.CharField(max_length=400)
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s' % (self.exam_venue)


def generate_exam_number():
	result = ''
	for x in range(1, 10):
		result += str(random.randint(0, 9))
	return result

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        if ext is None:
        	ext = 'jpg'
        if ext == "blob":
        	ext = "jpg"
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

@deconstructible
class PathAndRename(object):
	def __init__(self, path):
		self.path = path
	
	def __call__(self, instance, filename):
		ext = filename.split('.')[-1]
		if ext is None:
			ext = 'jpg'
		if ext == "blob":
			ext = "jpg"
        # get filename
		if instance.pk:
			filename = '{}.{}'.format(instance.pk, ext)
		else:
            # set filename as random string
			filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        # return the whole path to the file
		return os.path.join(self.path, filename)

path_and_rename2 = PathAndRename("booking_images")

path_and_rename3 = path_and_rename("booking_images")

class ExamBooking(models.Model):
	"""Exam Booking Model"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	title = models.CharField(max_length=100, blank=True, null=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=100, null=True, blank=True)
	state = models.CharField(max_length=100, choices=STATE)
	mobile_number = models.CharField(max_length=50)
	email_address = models.EmailField(blank=True)
	address = models.TextField(blank=True)
	date_of_birth = models.DateField(blank=True)
	gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')))
	preffered_date = models.DateField()
	drive_test_type = models.CharField(max_length=30, choices=( 
		('new', 'New'), 
		('renew', 'Re-New')), blank=True, null=True)
	exam_preferred_language = models.CharField(max_length=2, choices=LANG_CHOICES, 
		default=ENGLISH)
	exam_venue = models.ForeignKey(ExamVenue, on_delete=models.CASCADE)
	photo = models.ImageField(null=True, blank=True, upload_to=path_and_rename2)
	onsite_photo = models.TextField(null=True, blank=True)
	card_number = models.CharField(max_length=12, blank=True, null=True)
	examination_number = models.CharField(max_length=10, unique=True, editable=False, default=generate_exam_number)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('-created_at',)

	def __str__(self):
		return '%s' % (self.full_name)
	def _get_full_name(self):
		"Return the person's full name."
		return '%s %s' % (self.first_name, self.last_name)

	full_name = property(_get_full_name)
	# always check if pin exists b4
	# examination_number = models.CharField(max_length=10, unique=True, editable=False, default=generate_exam_number)

class ExamPhoto(models.Model):
	"""N Random photos of student taken during their exams"""
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	photo = models.ImageField(null=True, blank=True)
	exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
	examination_number = models.CharField(blank=False, null=False, max_length=10)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	def __str__(self):
		return '%s %s' % (self.examination_number, self.exam.title)


class Payment(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	transaction_ref = models.CharField(unique=True, max_length=100)
	mobile_number = models.TextField()
	amount = models.DecimalField(decimal_places =2, max_digits=10)
	description = models.CharField(max_length=200, null=True, blank=True)
	status = models.BooleanField(default=False)
	created_at = models.DateField(auto_now_add=True)
