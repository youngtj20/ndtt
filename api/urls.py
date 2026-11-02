from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.documentation import include_docs_urls

router = DefaultRouter()
router.register('exam_venues', viewset=views.ExamCenterViewSet, base_name='venues')
router.register('exam_categories', viewset=views.ExamCategoryViewSet, base_name='categories')
# router.register('booking', viewset=views.ExamBookingViewSet, base_name='booking')

urlpatterns = [
    url(r'^booking/', views.ExamBookingView.as_view()),
    url(r'^languages/', views.LanguageView.as_view()),
    url(r'^states/', views.stateView.as_view()),
    url(r'^gender/', views.GenderView.as_view()),
    url(r'^drive-test-type/', views.TestTypeView.as_view()),
    url(r'docs/', include_docs_urls(title='DTT Booking API')),
]

urlpatterns += router.urls