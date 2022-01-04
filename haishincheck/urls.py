from django.contrib import admin
from django.urls import path


from .views import (
    HomeView, execute_scraping, 
)

app_name = 'haishin-check'


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('execute_scraping/', execute_scraping, name='execute_scraping')
]


