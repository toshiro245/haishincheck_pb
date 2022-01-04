from django.contrib import admin
from django.urls import path, include

from haishincheck import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('haishincheck.urls')),
]



handler404 = views.page_not_found
handler500 = views.server_error