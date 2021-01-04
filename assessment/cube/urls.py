
from django.conf.urls import url, include
from cube import views

urlpatterns = [
    url('events/', views.end_user_event_list),
]