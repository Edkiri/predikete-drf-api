"""
URL configuration for predikete project.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('api.users.urls', 'users'), namespace='users')),
    path('', include(('api.parties.urls', 'parties'), namespace='parties'))
]
