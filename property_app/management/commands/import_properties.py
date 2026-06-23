import pandas as pd
import numpy as np 
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from django.utils.text import slugify
from sentence_transformers import SentenceTransformer 
from property_app.models import Property, Location

class Command(BaseCommand):
    help = 'Parse and ingest properties from an input CSV file through Pandas dataframes'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to target dataset source spreadsheet file')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        #  Load the lightweight AI engine into your web container memory
        ai_model = SentenceTransformer('all-MiniLM-L6-v2')

        try:
            df = pd.read_csv(csv_file_path)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading target dataset file: {str(e)}"))
            return

        counter = 0

        for _, row in df.iterrows():
            title = row.get('title')
            if not title:
                continue

            csv_loc_name = row.get('loc_name', 'Default Hub')
            csv_city = row.get('loc_city', 'Unknown City')
            csv_country = row.get('loc_country', 'Global')

            # Extract spatial coordinates upfront
            lat = float(row.get('latitude', 0.0))
            lon = float(row.get('longitude', 0.0))
            geo_point = Point(lon, lat, srid=4326)
            
            #  Create a natural phrase describing this location text
            sentence = f"Properties located at {csv_loc_name} within the region of {csv_city}, {csv_country}."
            
            #  Convert that sentence text into raw numbers (384 elements)
            base_vector = ai_model.encode(sentence)
            
            #  Create a blank container with 1536 slots 
            padded_vector = np.zeros(1536)
            
            # Paste our 384 generated numbers into the beginning of the 1536 container
            padded_vector[:len(base_vector)] = base_vector
            
            # Convert it to a simple Python list so Django can save it
            final_embedding = padded_vector.tolist()
            
           
            unique_slug = slugify(f"{csv_city}-{csv_loc_name}")
            
            row_location, _ = Location.objects.get_or_create(
                city=csv_city,
                country=csv_country,
                defaults={
                    'name': csv_loc_name,
                    'slug': unique_slug,
                    'point': geo_point,
                    'embedding': final_embedding  
                }
            )

            property_obj, created = Property.objects.get_or_create(
                title=title,
                defaults={
                    'location': row_location,
                    'slug': slugify(title),
                    'description': row.get('description', ''),
                    'property_type': row.get('property_type', 'Vacation Rental'),
                    'status': row.get('status', 'Active'),
                    'price': float(row.get('price', 120.00)),
                    'bedrooms': int(row.get('bedrooms', 1)),
                    'bathrooms': int(row.get('bathrooms', 1)),
                    'point': geo_point
                }
            )

            if created:
                counter += 1
        
        self.stdout.write(self.style.SUCCESS(f"Successfully processed CSV. Ingested {counter} global entries with location embeddings!"))