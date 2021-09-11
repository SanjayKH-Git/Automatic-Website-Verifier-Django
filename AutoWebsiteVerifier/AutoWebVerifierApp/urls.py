from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('VerifyWeb', views.VerifyWeb, name='VerifyWeb'),
    path('download', views.download, name='download')
]