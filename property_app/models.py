from django.contrib.gis.db import models
from django.utils.text import slugify
from pgvector.django import VectorField, HnswIndex 

class Location(models.Model):
    name = models.CharField(max_length=255) 
    slug = models.SlugField(unique=True, blank=True) 
    country = models.CharField(max_length=100) 
    state = models.CharField(max_length=100, blank=True) 
    city = models.CharField(max_length=100) 
    address = models.TextField(blank=True) 
    point = models.PointField(geography=True, srid=4326, null=True, blank=True) 
    boundary = models.MultiPolygonField(srid=4326, null=True, blank=True) 
    embedding = VectorField(dimensions=1536, null=True, blank=True) 
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            HnswIndex(
                name="location_embedding_idx", 
                fields=["embedding"], 
                m=16, 
                ef_construction=64, 
                opclasses=["vector_cosine_ops"] # Compares vectors by meaning
            )
        ]
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.city}, {self.country}"

class Property(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="properties") 
    title = models.CharField(max_length=255) 
    slug = models.SlugField(unique=True, blank=True) 
    description = models.TextField(blank=True) 
    property_type = models.CharField(max_length=50) 
    status = models.CharField(max_length=50) 
    price = models.DecimalField(max_digits=14, decimal_places=2) 
    bedrooms = models.PositiveSmallIntegerField(default=0) 
    bathrooms = models.PositiveSmallIntegerField(default=0) 
    area_sqft = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True) 
    address = models.TextField(blank=True)
    
    # Text coordinate helpers for easy admin entry configuration
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    point = models.PointField(geography=True, srid=4326, null=True, blank=True) 
    footprint = models.PolygonField(srid=4326, null=True, blank=True) 
    embedding = VectorField(dimensions=1536, null=True, blank=True) 
    is_featured = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 

    class Meta:
        indexes = [ 
            HnswIndex( 
                name="property_embedding_idx", 
                fields=["embedding"], 
                m=16, 
                ef_construction=64, 
                opclasses=["vector_cosine_ops"]
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Intercept and build the Point geometric object automatically
        if self.latitude is not None and self.longitude is not None:
            from django.contrib.gis.geos import Point
            self.point = Point(float(self.longitude), float(self.latitude), srid=4326)
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class PropertyImage(models.Model): 
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images") 
    image = models.ImageField(upload_to="properties/%Y/%m/") 
    alt_text = models.CharField(max_length=255, blank=True) 
    caption = models.TextField(blank=True) 
    width = models.PositiveIntegerField(null=True, blank=True) 
    height = models.PositiveIntegerField(null=True, blank=True) 
    file_size = models.BigIntegerField(null=True, blank=True) 
    embedding = VectorField(dimensions=768, null=True, blank=True) 
    is_primary = models.BooleanField(default=False) 
    sort_order = models.PositiveIntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True) 