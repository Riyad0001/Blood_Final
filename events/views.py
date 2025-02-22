from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event, Donation
from .serializers import EventSerializer, DonationSerializer
from .permissons import IsEventCreator
from rest_framework import generics, permissions

class EventListView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['blood_group_needed']

    def get_queryset(self):
        return Event.objects.filter(is_active=True).exclude(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsEventCreator]

    def perform_update(self, serializer):
        serializer.save()  # Add any custom update logic here

    def perform_destroy(self, instance):
        instance.is_active = False  # Soft delete example
        instance.save()

class DonationListView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(donor=self.request.user)

class AcceptDonationView(generics.CreateAPIView):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        event_id = self.kwargs.get('event_id')
        event = Event.objects.get(id=event_id)
        
        if event.creator == self.request.user:
            return Response(
                {'detail': 'You cannot accept your own request'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer.save(donor=self.request.user, event=event)