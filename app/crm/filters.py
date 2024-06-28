import django_filters
from .models import Apartment

class ApartmentFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=Apartment.STATUS_CHOICES)

    class Meta:
        model = Apartment
        fields = ['status']
