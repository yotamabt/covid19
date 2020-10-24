from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index', views.index, name='index'),
    path('maketestvsposreport',views.makeTestVsPosReport,name="maketestvsposreport"),
    path('testload',views.testpath,name="test"),


]