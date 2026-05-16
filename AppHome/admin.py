from django.contrib import admin
from django.utils.html import format_html  # Import this for safe HTML rendering
from .models import Reservation, SocialLink, RestaurantInfo, GalleryImage, Chef


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    # Added 'status_light' to the beginning of the list display
    list_display = ('status_light', 'name', 'mobile', 'date', 'time', 'guests', 'status')

    list_filter = ('status', 'date')
    search_fields = ('name', 'mobile', 'email')
    list_editable = ('status',)

    fieldsets = (
        ('Guest Information', {
            'fields': ('name', 'mobile', 'email')
        }),
        ('Reservation Details', {
            'fields': ('date', 'time', 'guests', 'status')
        }),
    )

    actions = ['mark_as_confirmed', 'mark_as_cancelled']

    # ==========================================
    # CUSTOM LED LIGHT INDICATOR
    # ==========================================
    def status_light(self, obj):
        """
        Returns a colored dot based on the reservation status.
        """
        # Define your colors based on the status
        if obj.status == 'Confirmed':
            color = '#28a745'  # Green
            box_shadow = '0 0 5px #28a745'  # Adds a little glow effect
        elif obj.status == 'Pending':
            color = '#F6FF00'  # Orange/Yellow
            box_shadow = '0 0 5px #ffc107'
        elif obj.status == 'Cancelled':
            color = '#dc3545'  # Red
            box_shadow = '0 0 5px #dc3545'
        else:
            color = '#6c757d'  # Gray (fallback)
            box_shadow = 'none'

        # Generate the HTML for the "LED" dot
        return format_html(
            '<span style="display:inline-block; width:12px; height:12px; border-radius:50%; background-color:{}; box-shadow:{};" title="{}"></span>',
            color, box_shadow, obj.status
        )

    # This sets the column header name in the Django Admin table
    status_light.short_description = '🚥'

    # ==========================================
    # BULK ACTIONS
    # ==========================================
    @admin.action(description='Mark selected reservations as Confirmed')
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='Confirmed')
        self.message_user(request, f'{updated} reservations successfully marked as Confirmed.')

    @admin.action(description='Mark selected reservations as Cancelled')
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='Cancelled')
        self.message_user(request, f'{updated} reservations successfully marked as Cancelled.')


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    # Added 'icon_preview' so the client can visually see the icon they typed!
    list_display = ('platform_name', 'icon_preview', 'icon_class', 'url', 'display_order', 'is_active')

    # Allows them to quickly change links and order without clicking into the record
    list_editable = ('display_order', 'is_active', 'url')

    # We removed 'icon_class' from list_filter because filtering by a raw text box isn't very helpful
    list_filter = ('is_active',)
    search_fields = ('platform_name', 'icon_class', 'url')

    # ==========================================
    # CUSTOM ICON PREVIEW FOR ADMIN PANEL
    # ==========================================
    def icon_preview(self, obj):
        """
        Renders the actual FontAwesome icon inside the Django Admin table.
        This helps the client verify they typed the correct class name.
        """
        if obj.icon_class:
            # We inject the font-awesome class and make it a bit larger (20px) for visibility
            return format_html(
                '<i class="fa {}" style="font-size: 20px; color: #555;"></i>',
                obj.icon_class
            )
        return "No Icon"

    # Sets the column header text in the admin table
    icon_preview.short_description = 'Preview'


@admin.register(RestaurantInfo)
class RestaurantInfoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'email')

    # Optional: A neat trick to prevent the client from creating 50 different
    # contact addresses. It forces them to only have ONE master record.
    def has_add_permission(self, request):
        if self.model.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'title', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('title',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url)
        return "No Image"

    image_preview.short_description = 'Preview'


@admin.register(Chef)
class ChefAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'bio', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    search_fields = ('name',)

    fieldsets = (
        ('Basic Details', {
            'fields': ('name', 'bio', 'image', 'is_active', 'display_order')
        }),
        ('Social Links (Optional)', {
            'fields': ('facebook', 'twitter', 'instagram', 'dribbble', 'behance'),
            'description': 'Leave a link blank to hide that specific icon on the website.'
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 50%;" />',
                obj.image.url)
        return "No Image"

    image_preview.short_description = 'Photo'