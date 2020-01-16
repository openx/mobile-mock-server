from django.urls import path, re_path

from . import views

urlpatterns = [
    path('ma/1.0/acj', views.MockView.as_view(), name='index'),
    path('v/1.0/av', views.VideoMockView.as_view(), name='index'),
    path('api/add_mock', views.AddMockView.as_view(), name='api'),
    path('api/logs', views.EventsLogView.as_view(), name='events_log'),
    path('api/clear_logs', views.ClearLogView.as_view(), name='clear_log'),
    path('api/clear_configs', views.ClearConfigsView.as_view(), name='clear_configs'),
    path('api/set_error', views.SetErrorView.as_view(), name='set_error'),
    path('api/set_latency', views.SetLatencyView.as_view(), name='set_latency'),
    path('image', views.ImageGeneratorView.as_view(), name='image'),
    re_path('events.*', views.EventsView.as_view(), name='events'),
]
