from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from django.urls import reverse
from property_app.models import Location

class AutocompleteAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        if not query or len(query) < 2:
            return Response([])

        # Find matching locations by city or country name string values
        location_matches = Location.objects.filter(
            Q(city__icontains=query) | Q(country__icontains=query)
        ).distinct()[:6] # Limit dropdown view frame entries to top 6 combinations

        results = []
        for loc in location_matches:
            # Safely point to your main property search listing template view name
            # Usually named 'property_listing' or 'listings' in your main urls.py
            try:
                base_url = reverse('property_listing')
            except Exception:
                base_url = reverse('property_app:property_listing')

            results.append({
                'display_text': f"{loc.city}, {loc.country}",
                'subtitle': "view all properties",
                'url': f"{base_url}?q={encode_uri_component(loc.city)}" if 'encode_uri_component' in locals() else f"{base_url}?q={loc.city}"
            })

        return Response(results)