from django.urls import path
from myapp import views

urlpatterns = [
    path('', views.index),
    path('loadnotes/', views.loadNotes),
    path('savenote/', views.saveNote),
]
