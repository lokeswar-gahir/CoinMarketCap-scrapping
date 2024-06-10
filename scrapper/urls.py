from django.urls import path
from .views import *


urlpatterns = [
    path('', index, name='index'),
    path('api/taskmanager/start_scraping/', startScrapping, name='start_scrapping'),
    path('api/taskmanager/scraping_status/<job_id>/', scrappingStatus, name='scrapping_status'),
]
