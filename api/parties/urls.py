"""Paties URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import parties as parties_views

router = DefaultRouter()
router.register(r'parties', parties_views.PartiesViewSet, basename='parties')

urlpatterns = [
    path('', include(router.urls)),
]
