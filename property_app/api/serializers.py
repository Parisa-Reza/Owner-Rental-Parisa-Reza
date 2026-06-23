from rest_framework import serializers
from property_app.models import Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [ 'city', 'country']