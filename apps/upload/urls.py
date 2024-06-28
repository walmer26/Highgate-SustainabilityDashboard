from django.urls import path
from .views import ReportUploadView

app_name = 'upload'

urlpatterns = [
    path('report/', ReportUploadView.as_view(), name='upload_report'),
]
