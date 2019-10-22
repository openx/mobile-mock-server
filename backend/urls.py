from django.urls import path, re_path

from . import views

urlpatterns = [
    path('ma/1.0/acj', views.MockView.as_view(), name='index'),
    path('api', views.ApiView.as_view(), name='api'),
    path('image', views.ImageGeneratorView.as_view(), name='image'),
    path('events_log', views.EventsLogView.as_view(), name='events_log'),
    re_path('events/.*', views.EventsView.as_view(), name='events'),
]
