from django.urls import include, re_path
from CameraSite.views import user_list

urlpatterns = [
    re_path(r'^$', user_list, name='user_list'),
]
