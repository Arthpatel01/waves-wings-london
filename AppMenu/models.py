from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from base_models import BaseModel
# from Restaurent.models import Restaurent  # TODO: Uncomment after Restaurent is created
from AppUser.models import User


class Category(BaseModel):
    """
    Menu Category Model - Each category has a unique category_id
    """

    # ========== PRIMARY KEY ==========
    category_id = models.AutoField(primary_key=True, verbose_name="Category ID")

    # ========== BASIC INFORMATION ==========
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Category name (e.g., 'Appetizers', 'Main Course')"
    )

    slug = models.SlugField(
        max_length=120,
        blank=True,
        unique=False,
        help_text="URL-friendly name (auto-generated from name)"
    )

    description = models.TextField(
        blank=True,
        help_text="Brief description of this category"
    )

    # ========== DISPLAY SETTINGS ==========
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Order in which categories appear (lower numbers first)"
    )

    is_visible = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Whether this category is visible to customers"
    )

    # ========== VISUAL ELEMENTS ==========
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="Font Awesome icon class"
    )

    image = models.ImageField(
        upload_to='menu/categories/%Y/%m/',
        blank=True,
        null=True,
        help_text="Category cover image"
    )

    color_code = models.CharField(
        max_length=7,
        blank=True,
        help_text="Hex color code for category"
    )

    # ========== PARENT CATEGORY ==========
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories',
        db_index=True,
        help_text="Parent category for subcategories (optional)"
    )

    # ========== STAFF TRACKING ==========
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_categories',
        help_text="Staff member who created this category"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_categories',
        help_text="Staff member who last updated this category"
    )

    class Meta:
        db_table = 'app_menu_category'
        verbose_name = 'Menu Category'
        verbose_name_plural = 'Menu Categories'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['parent_category']),
            models.Index(fields=['slug']),
        ]

    @property
    def full_path(self):
        """Get category path for breadcrumbs"""
        if self.parent_category:
            return f"{self.parent_category.full_path} > {self.name}"
        return self.name

    @property
    def is_subcategory(self):
        """Check if this is a subcategory"""
        return self.parent_category is not None

    @property
    def get_icon_html(self):
        """Return HTML for icon if exists"""
        if self.icon:
            return f'<i class="{self.icon}"></i>'
        return ''

    def __str__(self):
        return f"{self.name} (ID: {self.category_id})"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('menu:category_detail', kwargs={'category_id': self.category_id, 'slug': self.slug})


# ============================================================================
# MENU ITEM MODEL
# ============================================================================

class MenuItem(BaseModel):
    """
    Menu Item Model - Each menu item has a unique menu_item_id
    Represents individual dishes on the menu
    """

    # ========== PRIMARY KEY ==========
    menu_item_id = models.AutoField(primary_key=True, verbose_name="Menu Item ID")

    # ========== RELATIONSHIPS ==========
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='items',  # ✅ This creates the 'items' relation!
        db_index=True,
        help_text="Category this item belongs to"
    )

    # TODO: Uncomment after Restaurent model is created
    # restaurent = models.ForeignKey(
    #     Restaurent,
    #     on_delete=models.CASCADE,
    #     related_name='menu_items',
    #     db_index=True,
    #     help_text="Which restaurant this item belongs to"
    # )

    # ========== BASIC INFORMATION ==========
    name = models.CharField(
        max_length=200,
        db_index=True,
        help_text="Name of the dish"
    )

    slug = models.SlugField(
        max_length=220,
        blank=True,
        help_text="URL-friendly name (auto-generated)"
    )

    short_description = models.CharField(
        max_length=100,
        blank=True,
        help_text="Short description for lists"
    )

    description = models.TextField(
        help_text="Detailed description of the dish"
    )

    # ========== PRICING ==========
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        db_index=True,
        help_text="Regular price"
    )

    compare_at_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Original price (for sale items)"
    )

    cost_per_item = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Cost to make (for profit calculation)"
    )

    # ========== DIETARY OPTIONS ==========
    is_vegetarian = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Vegetarian friendly"
    )

    is_vegan = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Vegan friendly"
    )

    is_gluten_free = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Gluten free"
    )

    is_dairy_free = models.BooleanField(
        default=False,
        help_text="Dairy free"
    )

    is_nut_free = models.BooleanField(
        default=False,
        help_text="Nut free"
    )

    is_spicy = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Spicy dish"
    )

    # ========== AVAILABILITY ==========
    is_available = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Currently available for order"
    )

    is_recommended = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Featured/Recommended item"
    )

    is_new = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Newly added item"
    )

    is_bestseller = models.BooleanField(
        default=False,
        help_text="Bestselling item"
    )

    # ========== PREPARATION ==========
    preparation_time = models.PositiveIntegerField(
        default=15,
        help_text="Preparation time in minutes"
    )

    # ========== STOCK MANAGEMENT ==========
    has_stock_limit = models.BooleanField(
        default=False,
        help_text="Enable stock tracking"
    )

    stock_quantity = models.PositiveIntegerField(
        default=0,
        help_text="Current stock quantity"
    )

    low_stock_threshold = models.PositiveIntegerField(
        default=5,
        help_text="Alert when stock goes below this number"
    )

    # ========== MEDIA ==========
    image = models.ImageField(
        upload_to='menu/items/%Y/%m/',
        blank=True,
        null=True,
        help_text="Main image for this item"
    )

    # ========== NUTRITION (Optional) ==========
    calories = models.PositiveIntegerField(
        blank=True,
        null=True,
        help_text="Calories per serving"
    )

    protein = models.FloatField(
        blank=True,
        null=True,
        help_text="Protein in grams"
    )

    carbs = models.FloatField(
        blank=True,
        null=True,
        help_text="Carbohydrates in grams"
    )

    fat = models.FloatField(
        blank=True,
        null=True,
        help_text="Fat in grams"
    )

    # ========== STAFF TRACKING ==========
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_menu_items',
        help_text="Staff who created this item"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_menu_items',
        help_text="Staff who last updated this item"
    )

    class Meta:
        db_table = 'app_menu_item'
        verbose_name = 'Menu Item'
        verbose_name_plural = 'Menu Items'
        ordering = ['category__display_order', 'name']
        indexes = [
            models.Index(fields=['category', 'is_available']),
            models.Index(fields=['price']),
            models.Index(fields=['is_vegetarian', 'is_available']),
            models.Index(fields=['is_recommended']),
            models.Index(fields=['is_new']),
            models.Index(fields=['slug']),
        ]

    # ========== PROPERTIES ==========
    @property
    def is_on_sale(self):
        """Check if item is on sale"""
        return self.compare_at_price is not None and self.compare_at_price > self.price

    @property
    def discount_percentage(self):
        """Calculate discount percentage if on sale"""
        if self.is_on_sale:
            return int(((self.compare_at_price - self.price) / self.compare_at_price) * 100)
        return 0

    @property
    def is_low_stock(self):
        """Check if stock is low"""
        if self.has_stock_limit:
            return self.stock_quantity <= self.low_stock_threshold
        return False

    @property
    def is_out_of_stock(self):
        """Check if out of stock"""
        if self.has_stock_limit:
            return self.stock_quantity <= 0
        return False

    @property
    def get_price_display(self):
        """Return formatted price"""
        return f"${self.price:.2f}"

    @property
    def get_dietary_badges(self):
        """Return list of dietary badges for display"""
        badges = []
        if self.is_vegetarian:
            badges.append('vegetarian')
        if self.is_vegan:
            badges.append('vegan')
        if self.is_gluten_free:
            badges.append('gluten-free')
        if self.is_spicy:
            badges.append('spicy')
        return badges

    # ========== METHODS ==========
    def __str__(self):
        return f"{self.name} - ${self.price} (ID: {self.menu_item_id})"

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def reduce_stock(self, quantity=1):
        """Reduce stock when ordered"""
        if self.has_stock_limit and self.stock_quantity >= quantity:
            self.stock_quantity -= quantity
            self.save()
            return True
        return False

    def increase_stock(self, quantity=1):
        """Increase stock when restocking"""
        if self.has_stock_limit:
            self.stock_quantity += quantity
            self.save()
            return True
        return False

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('menu:menu_item_detail', kwargs={'menu_item_id': self.menu_item_id, 'slug': self.slug})


# ============================================================================
# MENU IMAGE MODEL
# ============================================================================

class MenuImage(BaseModel):
    """
    Menu Image Model - Each image has a unique menu_image_id
    Supports multiple images per menu item
    """

    # ========== PRIMARY KEY ==========
    menu_image_id = models.AutoField(primary_key=True, verbose_name="Menu Image ID")

    # ========== RELATIONSHIPS ==========
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='images',
        db_index=True,
        help_text="Which menu item this image belongs to"
    )

    # ========== IMAGE DETAILS ==========
    image = models.ImageField(
        upload_to='menu/items/gallery/%Y/%m/',
        help_text="Image file"
    )

    caption = models.CharField(
        max_length=200,
        blank=True,
        help_text="Image caption/description"
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True,
        help_text="Alt text for accessibility/SEO"
    )

    # ========== DISPLAY SETTINGS ==========
    display_order = models.PositiveIntegerField(
        default=0,
        help_text="Order in gallery (lower numbers first)"
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Is this the primary image for the menu item?"
    )

    # ========== STAFF TRACKING ==========
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_menu_images',
        help_text="Staff who uploaded this image"
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_menu_images',
        help_text="Staff who last updated this image"
    )

    class Meta:
        db_table = 'app_menu_image'
        verbose_name = 'Menu Image'
        verbose_name_plural = 'Menu Images'
        ordering = ['display_order']
        indexes = [
            models.Index(fields=['menu_item', 'is_primary']),
            models.Index(fields=['is_primary']),
        ]

    # ========== METHODS ==========
    def __str__(self):
        return f"Image {self.menu_image_id} - {self.menu_item.name}"

    def save(self, *args, **kwargs):
        """Ensure only one primary image per menu item"""
        if self.is_primary:
            # Set all other images of this menu item to non-primary
            MenuImage.objects.filter(
                menu_item=self.menu_item,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    @property
    def get_image_url(self):
        """Return image URL or default placeholder"""
        if self.image:
            return self.image.url
        return '/static/images/placeholder.png'


# ============================================================================
# DAILY SPECIAL MODEL (Optional)
# ============================================================================

class DailySpecial(BaseModel):
    """
    Daily Special Model - Special items on specific days
    """

    # ========== PRIMARY KEY ==========
    special_id = models.AutoField(primary_key=True, verbose_name="Special ID")

    # ========== RELATIONSHIPS ==========
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='specials',
        help_text="Menu item that is on special"
    )

    # ========== SPECIAL DETAILS ==========
    DAYS_OF_WEEK = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    day_of_week = models.IntegerField(
        choices=DAYS_OF_WEEK,
        db_index=True,
        help_text="Which day this special applies to"
    )

    special_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text="Special price (leave blank to use regular price)"
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Is this special currently active"
    )

    # ========== STAFF TRACKING ==========
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_specials'
    )

    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='updated_specials'
    )

    class Meta:
        db_table = 'app_menu_daily_special'
        verbose_name = 'Daily Special'
        verbose_name_plural = 'Daily Specials'
        unique_together = [['menu_item', 'day_of_week']]
        indexes = [
            models.Index(fields=['day_of_week', 'is_active']),
        ]

    @property
    def effective_price(self):
        """Return special price if set, else regular price"""
        return self.special_price or self.menu_item.price

    def __str__(self):
        return f"{self.get_day_of_week_display()}: {self.menu_item.name} - ${self.effective_price}"


class SpecialPackage(BaseModel):
    """
    Special Package Model - Flexible promotions and meal combo bundles
    displayed within the homepage carousel wrapper.
    """
    package_id = models.AutoField(primary_key=True, verbose_name="Package ID")

    # ========== PROMOTIONAL DETAILS ==========
    title = models.CharField(
        max_length=250,
        help_text="e.g., '40% off for 9'' - 12'' pizza' or 'Signature Fish Meal Feast'"
    )

    available_days = models.CharField(
        max_length=150,
        help_text="e.g., 'Wed, Thu, Friday only' or 'Weekends Only' or 'Daily 12pm - 4pm'"
    )

    description = models.TextField(
        help_text="Describe what's included, e.g., 'Large Haddock + 1 Side Dish + Cold Drink'"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        help_text="Special promotional price in British Pounds (£)"
    )

    # ========== IMAGE UPLOAD PROCESSING ==========
    image = models.ImageField(
        upload_to='promotions/%Y/%m/',
        blank=True,
        null=True,
        help_text="Upload premium promotion flyer graphics (Recommended: 370x240px or proportional aspect ratios)"
    )

    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Uncheck this box to instantly hide the promotion from the homepage carousel without deleting it"
    )

    # ========== STAFF AUDIT TRACKING ==========
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_packages'
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name='updated_packages'
    )

    class Meta:
        db_table = 'app_menu_special_package'
        verbose_name = 'Special Package'
        verbose_name_plural = 'Special Packages'
        ordering = ['-package_id']  # Shows newest creations first by default

    def __str__(self):
        return f"{self.title} - £{self.price} ({self.available_days})"