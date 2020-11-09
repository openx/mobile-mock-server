from django.urls import path, re_path

from . import views

urlpatterns = [
    path('openrtb2/auction', views.PrebidMockView.as_view(), name='index'),
    path('cache', views.CacheMockView.as_view(), name='index'),
    path('ma/1.0/acj', views.MockView.as_view(), name='index'),
    path('v/1.0/av', views.VideoMockView.as_view(), name='index'),
    path('api/add_mock', views.AddMockView.as_view(), name='api'),
    path('api/logs', views.EventsLogView.as_view(), name='events_log'),
    path('api/clear_logs', views.ClearLogView.as_view(), name='clear_log'),
    path('api/set_error', views.SetErrorView.as_view(), name='set_error'),
    path('api/cancel_error', views.CancelErrorView.as_view(), name='cancel_error'),
    path('api/set_latency', views.SetLatencyView.as_view(), name='set_latency'),
    path('api/cancel_latency', views.CancelLatencyView.as_view(), name='cancel_latency'),
    path('api/set_random_no_bids', views.SetRandomNoBidsView.as_view(), name='set_random_no_bids'),
    path('api/cancel_random_no_bids', views.CancelRandomNoBidsView.as_view(), name='cancel_random_no_bids'),
    path('image', views.ImageGeneratorView.as_view(), name='image'),
    re_path('events.*', views.EventsView.as_view(), name='events'),
]
