import pandas as pd
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils.text import slugify
from property_app.models import Property, Location

class Command(BaseCommand):
    help = 'Parse and ingest properties from an input CSV file through Pandas dataframes'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to target dataset source spreadsheet file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        try:
            # Leverage Pandas loading engine matrices to map rows instantly
            df = pd.read_csv(csv_file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading target dataset file: {str(e)}"))
            return

        # Ensure at least one default region exists to satisfy ForeignKey relationships
        default_location, _ = Location.objects.get_or_create(
            name="Primary Area Hub",
            defaults={'city': 'Metropolis', 'country': 'Global', 'slug': 'primary-area-hub'}
        )

        counter = 0


        for _, row in df.iterrows():
            title = row.get('title')
            if not title:
                continue

            # Pulling the unique location strings from the current CSV row
            csv_loc_name = row.get('loc_name', 'Default Hub')
            csv_city = row.get('loc_city', 'Unknown City')
            csv_country = row.get('loc_country', 'Global')

            # creating a dynamic Location row mapped specifically to this country
            row_location, _ = Location.objects.get_or_create(
                name=csv_loc_name,
                defaults={
                    'city': csv_city,
                    'country': csv_country,
                    'slug': slugify(csv_loc_name)
                }
            )

            # Extract spatial coordinates
            lat = float(row.get('latitude', 0.0))
            lon = float(row.get('longitude', 0.0))
            geo_point = Point(lon, lat, srid=4326)

            property_obj, created = Property.objects.get_or_create(
                title=title,
                defaults={
                    'location': row_location,  #  links to the dynamic country model row!
                    'slug': slugify(title),
                    'description': row.get('description', ''),
                    'property_type': row.get('property_type', 'Vacation Rental'),
                    'status': row.get('status', 'Active'),
                    'price': float(row.get('price', 120.00)),
                    'bedrooms': int(row.get('bedrooms', 1)),
                    'bathrooms': int(row.get('bathrooms', 1)),
                    'latitude': lat,
                    'longitude': lon,
                    'point': geo_point
                }
            )

            if created:
                counter += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully processed CSV. Ingested {counter} global entries!"))