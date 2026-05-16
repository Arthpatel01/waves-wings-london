from django.contrib import admin
from django.utils.html import format_html
from django.db import models as db_models
from django.forms import Textarea, TextInput, NumberInput
from .models import Category, MenuItem, MenuImage, DailySpecial, SpecialPackage


# ============================================================================
# CATEGORY ADMIN
# ============================================================================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model
    """

    # List view configuration
    list_display = [
        'category_id',
        'name',
        'display_order',
        'is_visible',
        'subcategory_badge',
        'icon_preview',
        'active_items_count_display',
        'created_on',
        'integrity_badge',
    ]

    list_filter = [
        'is_visible',
        'parent_category',
        'created_on',
    ]

    search_fields = [
        'name',
        'description',
        'category_id',
    ]

    list_editable = [
        'display_order',
        'is_visible',
    ]

    list_per_page = 25
    ordering = ['display_order', 'name']

    # Form layout
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'slug',
                'description',
                'parent_category',
            )
        }),
        ('Display Settings', {
            'fields': (
                'display_order',
                'is_visible',
            )
        }),
        ('Visual Elements', {
            'fields': (
                'icon',
                'color_code',
                'image',
            ),
            'classes': ('collapse',),
        }),
        ('Staff Tracking', {
            'fields': (
                'created_by',
                'updated_by',
            ),
            'classes': ('collapse',),
        }),
        ('Security Information', {
            'fields': (
                'category_id',
                'salt',
                'nonce',
                'tag',
                'record_hash',
                'version',
                'created_on',
                'updated_on',
                'ip_address',
            ),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = [
        'category_id',
        'salt',
        'nonce',
        'tag',
        'record_hash',
        'version',
        'created_on',
        'updated_on',
    ]

    # Form field overrides
    formfield_overrides = {
        db_models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 80})},
        db_models.CharField: {'widget': TextInput(attrs={'style': 'width: 50%;'})},
    }

    # ========== CUSTOM DISPLAY METHODS ==========

    def subcategory_badge(self, obj):
        """Display if category is subcategory"""
        if obj.parent_category:
            return format_html(
                '<span style="background-color: #17a2b8; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Sub of: {}</span>',
                obj.parent_category.name
            )
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 12px; font-size: 11px;">Main Category</span>'
        )

    subcategory_badge.short_description = "Category Type"

    def icon_preview(self, obj):
        """Preview icon if exists"""
        if obj.icon:
            return format_html('<i class="{}" style="font-size: 20px;"></i>', obj.icon)
        return "-"

    icon_preview.short_description = "Icon"

    def active_items_count_display(self, obj):
        """Display active items count with color coding"""
        # This will work after MenuItem is created
        try:
            count = obj.items.filter(is_available=True).count()
            if count == 0:
                return format_html('<span style="color: red;">0 items</span>')
            elif count < 5:
                return format_html('<span style="color: orange;">{} items</span>', count)
            else:
                return format_html('<span style="color: green;">{} items</span>', count)
        except:
            return "-"

    active_items_count_display.short_description = "Active Items"

    def integrity_badge(self, obj):
        """Display integrity verification status"""
        if obj.verify_integrity():
            return format_html('<span style="color: green;">✓ Verified</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">⚠ TAMPERED!</span>')

    integrity_badge.short_description = "Integrity"

    # ========== ADMIN ACTIONS ==========
    actions = ['make_visible', 'make_hidden', 'verify_integrity_action']

    @admin.action(description='Mark selected categories as visible')
    def make_visible(self, request, queryset):
        updated = queryset.update(is_visible=True)
        self.message_user(request, f'{updated} categories marked as visible.')

    @admin.action(description='Mark selected categories as hidden')
    def make_hidden(self, request, queryset):
        updated = queryset.update(is_visible=False)
        self.message_user(request, f'{updated} categories marked as hidden.')

    @admin.action(description='Verify integrity of selected categories')
    def verify_integrity_action(self, request, queryset):
        tampered = []
        for category in queryset:
            if not category.verify_integrity():
                tampered.append(f"{category.name} (ID: {category.category_id})")

        if tampered:
            self.message_user(
                request,
                f'⚠️ Tampered categories found: {", ".join(tampered)}',
                level='ERROR'
            )
        else:
            self.message_user(
                request,
                f'✓ All {queryset.count()} categories passed integrity check.'
            )

    # ========== SAVE METHOD ==========
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# ============================================================================
# MENU ITEM ADMIN
# ============================================================================

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    """
    Admin configuration for MenuItem model with rich text support
    """

    # List view configuration
    list_display = [
        'menu_item_id',
        'name_preview',
        'category',
        'price_display',
        'availability_badge',
        'dietary_badges',
        'stock_status',
        'orders_count',
        'updated_on',
        'integrity_badge',
    ]

    list_filter = [
        'category',
        'is_available',
        'is_vegetarian',
        'is_vegan',
        'is_gluten_free',
        'is_spicy',
        'is_recommended',
        'is_new',
        'is_bestseller',
        'has_stock_limit',
        'created_on',
    ]

    search_fields = [
        'name',
        'description',
        'short_description',
        'menu_item_id',
        'ingredients',
    ]

    # list_editable = [
        # 'price',
        # 'is_available',
        # 'is_recommended',
    # ]

    list_per_page = 25
    ordering = ['category__display_order', 'name']

    # Form layout with rich text support
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'category',
                'name',
                'slug',
                'short_description',
                'description',
            )
        }),
        ('Pricing', {
            'fields': (
                'price',
                'compare_at_price',
                'cost_per_item',
            ),
            'classes': ('wide',),
        }),
        ('Dietary & Labels', {
            'fields': (
                ('is_vegetarian', 'is_vegan', 'is_gluten_free'),
                ('is_dairy_free', 'is_nut_free', 'is_spicy'),
                ('is_available', 'is_recommended', 'is_new', 'is_bestseller'),
            ),
        }),
        ('Nutrition Information', {
            'fields': (
                ('calories', 'protein', 'carbs', 'fat'),
            ),
            'classes': ('collapse',),
        }),
        ('Stock & Preparation', {
            'fields': (
                'preparation_time',
                'has_stock_limit',
                'stock_quantity',
                'low_stock_threshold',
            ),
            'classes': ('collapse',),
        }),
        ('Media', {
            'fields': (
                'image',
            ),
            'classes': ('collapse',),
        }),
        ('Staff Tracking', {
            'fields': (
                'created_by',
                'updated_by',
            ),
            'classes': ('collapse',),
        }),
        ('Security Information', {
            'fields': (
                'menu_item_id',
                'salt',
                'nonce',
                'tag',
                'record_hash',
                'version',
                'created_on',
                'updated_on',
                'ip_address',
            ),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = [
        'menu_item_id',
        # 'salt',
        # 'nonce',
        # 'tag',
        # 'record_hash',
        'version',
        'created_on',
        'updated_on',
    ]

    # Form field overrides
    formfield_overrides = {
        db_models.TextField: {'widget': Textarea(attrs={'rows': 6, 'cols': 80, 'style': 'font-family: monospace;'})},
        db_models.CharField: {'widget': TextInput(attrs={'style': 'width: 70%;'})},
        db_models.DecimalField: {'widget': NumberInput(attrs={'step': '0.01'})},
        db_models.JSONField: {
            'widget': Textarea(attrs={'rows': 3, 'cols': 80, 'placeholder': '["item1", "item2", "item3"]'})},
    }

    # ========== CUSTOM DISPLAY METHODS ==========

    def name_preview(self, obj):
        """Display name with image thumbnail"""
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 30px; width: 30px; object-fit: cover; border-radius: 4px; margin-right: 8px;"> {}',
                obj.image.url,
                obj.name
            )
        return obj.name

    name_preview.short_description = "Menu Item"

    def price_display(self, obj):
        """Display price with sale styling"""
        if obj.is_on_sale:
            return format_html(
                '<span style="color: red; font-weight: bold;">${}</span> '
                '<span style="text-decoration: line-through; color: gray;">${}</span>',
                obj.price,
                obj.compare_at_price
            )
        return format_html('<span style="font-weight: bold;">${}</span>', obj.price)

    price_display.short_description = "Price"

    def availability_badge(self, obj):
        """Display availability status"""
        if obj.is_available:
            if obj.is_out_of_stock:
                return format_html('<span style="color: orange;">⚠ Out of Stock</span>')
            elif obj.is_low_stock:
                return format_html('<span style="color: orange;">⚠ Low Stock ({})</span>', obj.stock_quantity)
            else:
                return format_html('<span style="color: green;">✓ Available</span>')
        else:
            return format_html('<span style="color: red;">✗ Unavailable</span>')

    availability_badge.short_description = "Status"

    def dietary_badges(self, obj):
        """Display dietary badges as colored labels"""
        badges = []
        if obj.is_vegetarian:
            badges.append(
                '<span style="background-color: #28a745; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin: 2px;">Veg</span>')
        if obj.is_vegan:
            badges.append(
                '<span style="background-color: #20c997; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin: 2px;">Vegan</span>')
        if obj.is_gluten_free:
            badges.append(
                '<span style="background-color: #ffc107; color: black; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin: 2px;">GF</span>')
        if obj.is_spicy:
            badges.append(
                '<span style="background-color: #dc3545; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin: 2px;">🌶 Spicy</span>')

        if obj.is_recommended:
            badges.append(
                '<span style="background-color: #6f42c1; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin: 2px;">⭐ Recommended</span>')

        if obj.is_new:
            badges.append(
                '<span style="background-color: #17a2b8; color: white; padding: 2px 6px; border-radius: 4px; font-size: 10px; margin: 2px;">🆕 New</span>')

        return format_html(''.join(badges)) if badges else "-"

    dietary_badges.short_description = "Labels"

    def stock_status(self, obj):
        """Display stock status"""
        if obj.has_stock_limit:
            if obj.stock_quantity <= 0:
                return format_html('<span style="color: red;">Out of stock</span>')
            elif obj.stock_quantity <= obj.low_stock_threshold:
                return format_html('<span style="color: orange;">Low: {}</span>', obj.stock_quantity)
            else:
                return format_html('<span style="color: green;">In stock: {}</span>', obj.stock_quantity)
        return "-"

    stock_status.short_description = "Stock"

    def orders_count(self, obj):
        """Display orders count (placeholder - implement when Order model exists)"""
        # This will be implemented when you create Order model
        return "-"

    orders_count.short_description = "Orders"

    def integrity_badge(self, obj):
        """Display integrity verification status"""
        if obj.verify_integrity():
            return format_html('<span style="color: green;">✓</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">⚠</span>')

    integrity_badge.short_description = "Hash"

    # ========== ADMIN ACTIONS ==========
    actions = [
        'make_available',
        'make_unavailable',
        'mark_recommended',
        'mark_not_recommended',
        'increase_price_by_10_percent',
        'decrease_price_by_10_percent',
        'verify_integrity_action',
        'export_selected_as_json',
    ]

    @admin.action(description='Mark selected items as available')
    def make_available(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} items marked as available.')

    @admin.action(description='Mark selected items as unavailable')
    def make_unavailable(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} items marked as unavailable.')

    @admin.action(description='Mark as recommended')
    def mark_recommended(self, request, queryset):
        updated = queryset.update(is_recommended=True)
        self.message_user(request, f'{updated} items marked as recommended.')

    @admin.action(description='Remove recommended label')
    def mark_not_recommended(self, request, queryset):
        updated = queryset.update(is_recommended=False)
        self.message_user(request, f'{updated} items removed from recommended.')

    @admin.action(description='Increase price by 10%%')  # Double %%
    def increase_price_by_10_percent(self, request, queryset):
        for item in queryset:
            item.price = item.price * 1.10
            item.save()
        self.message_user(request, f'{queryset.count()} items increased by 10%.')

    @admin.action(description='Decrease price by 10%%')  # Double %%
    def decrease_price_by_10_percent(self, request, queryset):
        for item in queryset:
            item.price = item.price * 0.90
            item.save()
        self.message_user(request, f'{queryset.count()} items decreased by 10%.')

    @admin.action(description='Verify integrity of selected items')
    def verify_integrity_action(self, request, queryset):
        tampered = []
        for item in queryset:
            if not item.verify_integrity():
                tampered.append(f"{item.name} (ID: {item.menu_item_id})")

        if tampered:
            self.message_user(
                request,
                f'⚠️ Tampered items found: {", ".join(tampered)}',
                level='ERROR'
            )
        else:
            self.message_user(
                request,
                f'✓ All {queryset.count()} items passed integrity check.'
            )

    @admin.action(description='Export selected as JSON')
    def export_selected_as_json(self, request, queryset):
        import json
        from django.http import HttpResponse

        data = []
        for item in queryset:
            data.append({
                'id': item.menu_item_id,
                'name': item.name,
                'description': item.description,
                'price': float(item.price),
                'category': item.category.name,
                'is_vegetarian': item.is_vegetarian,
                'is_vegan': item.is_vegan,
                'is_gluten_free': item.is_gluten_free,
                'is_available': item.is_available,
            })

        response = HttpResponse(json.dumps(data, indent=2), content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="menu_items_export.json"'
        return response

    # ========== SAVE METHOD ==========
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
# admin.site.register(MenuItem)

# ============================================================================
# MENU IMAGE ADMIN (Inline)
# ============================================================================

class MenuImageInline(admin.TabularInline):
    """
    Inline admin for MenuImage - Edit images directly from MenuItem page
    """
    model = MenuImage
    extra = 1
    fields = ['image_preview', 'image', 'caption', 'alt_text', 'display_order', 'is_primary']
    readonly_fields = ['menu_image_id', 'image_preview', 'created_on']

    def image_preview(self, obj):
        """Show image thumbnail preview"""
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 50px; width: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url)
        return "-"

    image_preview.short_description = "Preview"


@admin.register(MenuImage)
class MenuImageAdmin(admin.ModelAdmin):
    """
    Admin configuration for MenuImage model
    """
    list_display = ['menu_image_id', 'image_preview', 'menu_item', 'is_primary', 'display_order', 'created_on']
    list_filter = ['is_primary', 'menu_item__category']
    search_fields = ['caption', 'alt_text', 'menu_item__name']
    list_editable = ['display_order', 'is_primary']

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="height: 40px; width: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url)
        return "-"

    image_preview.short_description = "Preview"

    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


# ============================================================================
# DAILY SPECIAL ADMIN
# ============================================================================

@admin.register(DailySpecial)
class DailySpecialAdmin(admin.ModelAdmin):
    """
    Admin configuration for DailySpecial model
    """
    list_display = [
        'special_id',
        'menu_item',
        'day_of_week_display',
        'special_price_display',
        'is_active',
        'created_on',
    ]

    list_filter = [
        'day_of_week',
        'is_active',
        'menu_item__category',
    ]

    search_fields = [
        'menu_item__name',
        'special_id',
    ]

    list_editable = [
        # 'special_price',
        'is_active',
    ]

    fieldsets = (
        ('Special Information', {
            'fields': (
                'menu_item',
                'day_of_week',
                'special_price',
                'is_active',
            )
        }),
        ('Staff Tracking', {
            'fields': (
                'created_by',
                'updated_by',
            ),
            'classes': ('collapse',),
        }),
        ('Security', {
            'fields': (
                'special_id',
                'salt',
                'nonce',
                'tag',
                'record_hash',
            ),
            'classes': ('collapse',),
        }),
    )

    readonly_fields = [
        'special_id',
        'salt',
        'nonce',
        'tag',
        'record_hash',
        'created_on',
        'updated_on',
    ]

    # ========== CUSTOM DISPLAY METHODS ==========

    def day_of_week_display(self, obj):
        """Display day name"""
        return obj.get_day_of_week_display()

    day_of_week_display.short_description = "Day"
    day_of_week_display.admin_order_field = 'day_of_week'

    def special_price_display(self, obj):
        """Display special price with comparison"""
        if obj.special_price:
            return format_html(
                '<span style="color: green; font-weight: bold;">${}</span> '
                '<span style="color: gray; font-size: 11px;">(was ${})</span>',
                obj.special_price,
                obj.menu_item.price
            )
        return format_html('<span style="color: gray;">Same as regular</span>')

    special_price_display.short_description = "Special Price"

    # ========== ACTIONS ==========
    actions = ['activate_specials', 'deactivate_specials']

    @admin.action(description='Activate selected specials')
    def activate_specials(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} specials activated.')

    @admin.action(description='Deactivate selected specials')
    def deactivate_specials(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} specials deactivated.')

    # ========== SAVE METHOD ==========
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(SpecialPackage)
class SpecialPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'available_days', 'price', 'is_active')
    list_filter = ('is_active', 'available_days')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'price')  # Modify prices directly from the main list overview table!

    # Auto-assign administrative logging updates transparently behind the scenes
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)
