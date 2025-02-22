from rest_framework import serializers
from .models import Event, Donation

class EventSerializer(serializers.ModelSerializer):
    creator = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'creator', 'title', 'description', 'blood_group_needed', 'is_active', 'created_at']

class DonationSerializer(serializers.ModelSerializer):
    donor = serializers.StringRelatedField(read_only=True)
    event = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Donation
        fields = ['id', 'donor', 'event', 'status', 'created_at']