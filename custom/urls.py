from django.conf.urls import url

from . import views

urlpatterns = [
    #admin
    url(r'^login/$', views.auth, name='login'),
    url(r'^logt/$', views.logout_user, name='logout'),
    # url(r'^dashboard/$', views.index, name='index'),
    url(r'^category/list/$', views.cat_list),
    url(r'^category/edit/(?P<uuid>[\w-]+)/$', views.cat_edit),
    url(r'^category/delete/(?P<uuid>[\w-]+)/$', views.cat_delete),
    url(r'^exam/list', views.exam_list_web),
    url(r'^exam/detail/(?P<uuid>[\w-]+)/$', views.exam_detail_web),
    url(r'^exam/edit/(?P<uuid>[\w-]+)/$', views.exam_edit_web),
    url(r'^exam/create/$', views.exam_create_web),
    url(r'^question/list/$', views.question_list_web),
    url(r'^question/detail/(?P<uuid>[\w-]+)/$', views.question_detail_web),
    url(r'^question/create/$', views.question_create_web),
    # url(r'^question/new$', views.question_create_new),
    url(r'^question/option/form/(?P<num>[\w-]+)', views.option_form_api),
    url(r'^question/edit/(?P<uuid>[\w-]+)/$', views.question_edit_web),
    url(r'^question/api/edit/(?P<uuid>[\w-]+)/$', views.question_edit_api),
    url(r'^option/api/edit/(?P<uuid>[\w-]+)/$', views.option_edit_api),
    url(r'^option/api/delete/(?P<uuid>[\w-]+)/$', views.option_delete_api),
    url(r'^option/api/list/(?P<uuid>[\w-]+)/$', views.option_list_api),
    url(r'^option/api/create/(?P<uuid>[\w-]+)/$', views.option_create_api),
    url(r'^question/translate/(?P<uuid>[\w-]+)/$', views.translate_question),
    url(r'^question/translate/edit/(?P<uuid>[\w-]+)/$', views.translate_question_edit),
    url(r'^exam/question/add/(?P<uuid>[\w-]+)/$', views.add_exam_question),
    url(r'^category/create/$', views.category_create),
    url(r'^center/list/$', views.exam_venue_list),
    url(r'^center/create/$', views.exam_venue_create),
    url(r'^booking/list/$', views.booking_list),
    url(r'booking/edit/(?P<uuid>[\w-]+)/$', views.booking_edit),
    url(r'^booking/list/api/$', views.booking_list_api),
    url(r'^question/list/api/$', views.question_list_api),
    url(r'^generate/token/$', views.generate_token),
    url(r'^token/list/$', views.token_list),
    url(r'token/today/$', views.token_today),
    url(r'^payment/$', views.payment),
    url(r'^make_payment/$', views.make_payment),
    url(r'^report/$', views.report),
    url(r'^payment/report/api/$', views.payment_report),
    url(r'^result/pdf/$', views.GeneratePdf.as_view()),

    url(r'^select/category/$', views.select_category),
    url(r'^start/booking/$', views.start_booking),
    url(r'booking$', views.booking_page),
    url(r'^preview/booking/(?P<uuid>[\w-]+)/$', views.preview_booking),
    url(r'booking_verification$', views.booking_verification_page),
    url(r'verify_bookings$', views.verify_booking),
    url(r'^logout/$', views.logout),

    url(r'driving_test$', views.driving_test_page),

    url(r'verify_candidate$', views.verify_candidate),
    url(r'candidate_verification$', views.candidate_verification_page),

    url(r'capture_photo$', views.capture_photo),
    url(r'photo_capture$', views.photo_capture_page),
    url(r'logout$', views.logout),

    url(r'process_candidate_exam$', views.process_candidate_exam),

    url(r'candidate_result$', views.candidate_result_page),
    url(r'^verify_result$', views.verify_result, name='verify_result'),

    # REST APIs
    url(r'^exam/center/$', views.get_venue),

    url(r'^exam/$', views.exam_list),
    url(r'^exam/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_detail),

    url(r'^exam_participant/$', views.exam_participant_list),
    url(r'^exam_participant/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_participant_detail),

    url(r'^load_candidate_questions/$', views.load_candidate_questions),
    url(r'^load_candidate_exam_info/$', views.load_candidate_exam_info),
    url(r'^exam_question/$', views.exam_question_list),
    url(r'^exam_question/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_question_detail),

    # url(r'^exam_sheet/$', views.exam_sheet_list),
    # url(r'^exam_sheet/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_sheet_detail),

    # url(r'^exam_answer_choice/$', views.exam_answer_choice_list),
    # url(r'^exam_answer_choice/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_answer_choice_detail),

    # url(r'^exam_answer_text_question/$', views.exam_answer_text_question_list),
    # url(r'^exam_answer_text_question/(?P<pk>[0-9,A-Z,a-z,-]+)$', 
    # 	views.exam_answer_text_question_detail),

    url(r'^question/$', views.question_list),
    url(r'^question/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.question_detail),

    # url(r'^question_media/$', views.question_media_list),
    # url(r'^question_media/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.question_media_detail),

    # url(r'^question_option/$', views.question_option_list),
    # url(r'^question_option/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.question_option_detail),

    # url(r'^translated_question/$', views.translated_question_list),
    # url(r'^translated_question/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.translated_question_detail),

    # url(r'^translated_question_media/$', views.translated_question_media_list),
    # url(r'^translated_question_media/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.translated_question_media_detail),

    # url(r'^translated_question_option/$', views.translated_question_option_list),
    # url(r'^translated_question_option/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.translated_question_option_detail),

    url(r'^exam_bookings/$', views.exam_booking_list),
    url(r'^exam_bookings/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_booking_detail),

    # url(r'^exam_photo/$', views.exam_photo_list),
    # url(r'^exam_photo/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_photo_detail),

    # url(r'^exam_venue/$', views.exam_venue_list),
    # url(r'^exam_venue/(?P<pk>[0-9,A-Z,a-z,-]+)$', views.exam_venue_detail),
    url(r'^create_pin/$', views.create_pin),
]
