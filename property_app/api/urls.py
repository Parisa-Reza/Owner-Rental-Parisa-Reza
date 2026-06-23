from django.urls import path
from .views import AutocompleteAPIView

urlpatterns = [
    path('autocomplete/', AutocompleteAPIView.as_view(), name='api-autocomplete'),
]