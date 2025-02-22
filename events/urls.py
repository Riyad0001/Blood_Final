from django.urls import path
from .views import EventListView, DonationListView, AcceptDonationView,EventDetailView

urlpatterns = [
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('donations/', DonationListView.as_view(), name='donation-list'),
    path('events/<int:event_id>/accept/', AcceptDonationView.as_view(), name='accept-donation'),
]