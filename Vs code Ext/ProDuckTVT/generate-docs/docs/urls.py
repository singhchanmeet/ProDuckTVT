# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('explain/', views.generate_documentation, name='generate_documentation'),
    # Add other URLs as needed
]