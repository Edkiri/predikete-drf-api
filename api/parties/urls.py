"""Paties URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import parties as parties_views
from .views import memberships as memberships_views
from .views import join_invitations as invitations_views
from .views import join_requests as requests_views

router = DefaultRouter()
router.register(r'parties', memberships_views.MembershipViewSet, basename='party_memberships')
router.register(r'parties', parties_views.PartiesViewSet, basename='parties')
router.register(r'join-invitations', invitations_views.JoinInvitationViewSet, basename='join_invitations')
router.register(r'join-requests', requests_views.JoinRequestViewSet, basename='join_requests')


urlpatterns = [
    path('', include(router.urls)),
]
