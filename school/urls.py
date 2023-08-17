from django.contrib import admin
from django.urls import path
from base.views import *
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login', handle_login, name='login'),
    path('register', register, name='register'),
    path('dashboard', dashboard, name='dashboard'),
    path('logout', handle_logout, name='logout'),
    path('school/<slug>', get_school, name='get_school'),
    path('notice', pub_notice, name='pub_notice'),
    path('dashboard/class', class_info, name='class_info')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

