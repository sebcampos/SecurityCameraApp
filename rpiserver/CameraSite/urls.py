from django.urls import include, re_path
from . import views

urlpatterns = [
    re_path(r'^$', user_list, name='user_list'),
]
