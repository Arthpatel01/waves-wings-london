# models.py (Add this to your models file)
from django.db import models
from base_models import BaseModel


class Reservation(BaseModel):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    mobile = models.CharField(max_length=20)
    date = models.CharField(
        max_length=50)  # Using CharField for simple MVP date strings, or use DateField if you parse it
    time = models.CharField(max_length=50)
    guests = models.IntegerField()

    # Optional: Track status
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')],
        default='Pending'
    )

    class Meta:
        db_table = 'app_reservation'
        verbose_name = 'Reservation'
        verbose_name_plural = 'Reservations'

    def __str__(self):
        return f"{self.name} - {self.date} at {self.time} ({self.guests} guests)"


class SocialLink(BaseModel):
    """
    Dynamic Social Media Links for the footer
    """

    platform_name = models.CharField(
        max_length=50,
        help_text="e.g., 'Restaurant Instagram'"
    )

    # CHANGED: Removed choices to make it a standard text input box
    icon_class = models.CharField(
        max_length=50,
        help_text="Enter the FontAwesome class exactly (e.g., 'fa-facebook', 'fa-instagram', 'fa-tiktok')"
    )

    url = models.URLField(
        max_length=500,
        help_text="The full link to your social media page (include https://)"
    )

    display_order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first (e.g., 1, 2, 3...)"
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this icon from the website temporarily"
    )

    class Meta:
        db_table = 'app_home_social_link'
        verbose_name = 'Social Link'
        verbose_name_plural = 'Social Links'
        ordering = ['display_order']

    def __str__(self):
        # CHANGED: We now just output the raw icon_class text instead of get_icon_class_display()
        return f"{self.platform_name} ({self.icon_class})"


class RestaurantInfo(BaseModel):
    """
    Stores global contact information for the restaurant.
    Designed so the client only ever needs to keep ONE active record.
    """
    address = models.TextField(
        help_text="Full physical address (e.g., 40, Colindale, Knightsbridge House...)"
    )

    # NEW FIELD: Google Maps URL
    address_url = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        help_text="Paste the Google Maps 'Share' link here so customers can click for directions."
    )

    email = models.EmailField(
        help_text="Public contact email address"
    )

    phone = models.CharField(
        max_length=30,
        help_text="Contact phone number (e.g., +44 77 2198 1295)"
    )

    class Meta:
        db_table = 'app_home_restaurant_info'
        verbose_name = 'Restaurant Info'
        verbose_name_plural = 'Restaurant Info'

    def __str__(self):
        return "Main Restaurant Contact Details"


class GalleryImage(BaseModel):
    """
    Restaurant Photo Gallery for the homepage carousel.
    """
    title = models.CharField(
        max_length=150,
        help_text="Crucial for SEO! Describe the image (e.g., 'Crispy Chicken Wings Platter')"
    )

    image = models.ImageField(
        upload_to='gallery/%Y/%m/',
        help_text="Upload high-quality gallery image."
    )

    display_order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first."
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide from the gallery."
    )

    class Meta:
        db_table = 'app_home_gallery'
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery Images'
        ordering = ['display_order', '-id']

    def __str__(self):
        return self.title


class Chef(BaseModel):
    """
    Model for the 'Our Chefs' team section on the homepage.
    """
    name = models.CharField(
        max_length=100,
        help_text="Chef's full name (e.g., 'Mark Angelila')"
    )

    bio = models.CharField(
        max_length=150,
        help_text="A short tagline or description about the chef."
    )

    image = models.ImageField(
        upload_to='team/%Y/%m/',
        help_text="Upload chef's photo (Recommended aspect ratio: square or portrait)"
    )

    # Optional Social Media Links
    facebook = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True, verbose_name="Twitter / X")
    instagram = models.URLField(max_length=255, blank=True, null=True)
    dribbble = models.URLField(max_length=255, blank=True, null=True)
    behance = models.URLField(max_length=255, blank=True, null=True)

    # Management controls
    display_order = models.IntegerField(
        default=0,
        help_text="Lower numbers appear first."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Uncheck to hide this chef from the website."
    )

    class Meta:
        db_table = 'app_home_chef'
        verbose_name = 'Chef'
        verbose_name_plural = 'Chefs'
        ordering = ['display_order', 'id']

    def __str__(self):
        return self.name