from django.contrib.gis import admin
from django.utils.html import format_html
from .models import Location, Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    """Enables nesting multiple image uploads directly inside the main Property form layout."""
    model = PropertyImage
    extra = 1  # Provision 1 blank placeholder field slot to attach files instantly
    fields = ('image', 'alt_text', 'is_primary', 'sort_order', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 80px; border-radius: 4px;" />', obj.image.url)
        return "No Image File Provided"
    image_preview.short_description = "Preview"

@admin.register(Property)
class PropertyAdmin(admin.GISModelAdmin):  # GISModelAdmin enables visual interactive OpenStreetMap controls
    fieldsets = (
        ("Core Specifications", {
            'fields': ('location', 'title', 'slug', 'description', 'property_type', 'status', 'price')
        }),
        ("Manual GPS Entry", {
            'description': "Type coordinates here. Saving updates the map point vector automatically.",
            'fields': ('latitude', 'longitude')
        }),
        ("Spatial Geography Maps", {
            'fields': ('point', 'footprint')
        }),
        ("AI Embeddings & State", {
            'fields': ('embedding', 'is_featured', 'is_active')
        }),
    )
    
    # Active sorting filters and analytical fields tracking lists
    list_display = ('title', 'property_type', 'price', 'status', 'is_featured')
    list_filter = ('property_type', 'status', 'is_featured', 'created_at')
    search_fields = ('title', 'description', 'address')
    prepopulated_fields = {'slug': ('title',)}
    
    # Embed the Tabular Inline layout for images
    inlines = [PropertyImageInline]

@admin.register(Location)
class LocationAdmin(admin.GISModelAdmin):
    list_display = ('name', 'city', 'country', 'is_active')
    list_filter = ('country', 'is_active')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(PropertyImage)