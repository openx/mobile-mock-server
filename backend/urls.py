from django.urls import path, re_path

from . import views

urlpatterns = [
    path('ma/1.0/acj', views.MockView.as_view(), name='index'),
    path('v/1.0/av', views.VideoMockView.as_view(), name='index'),
    path('api/add_mock', views.ApiView.as_view(), name='api'),
    path('api/events', views.EventsLogView.as_view(), name='events_log'),
    path('image', views.ImageGeneratorView.as_view(), name='image'),
    re_path('events/.*', views.EventsView.as_view(), name='events'),
]
