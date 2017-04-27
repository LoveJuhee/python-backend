from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from backend import views


urlpatterns = [
    url(r'^api/centers/', views.CenterViewSet.as_view()),
    url(r'^api/sensors/', views.SensorViewSet.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
