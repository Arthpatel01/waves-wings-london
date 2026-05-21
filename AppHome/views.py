from django.views.generic import View, TemplateView
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q, Case, When, Value, IntegerField
from django.conf import settings

from AppHome.models import Reservation, SocialLink, RestaurantInfo, GalleryImage, Chef
# Import models from other apps
from AppMenu.models import MenuItem, Category, DailySpecial, SpecialPackage
from AppUser.models import User


def handle_reservation(self, request):
    """
    Process table reservation form, save to DB, and send WhatsApp notification
    """
    # FIX: Mapped to match the 'name' attributes in index.html exactly
    name = request.POST.get('name', '').strip()
    email = request.POST.get('email', '').strip()
    mobile = request.POST.get('mobile', '').strip()
    date = request.POST.get('date', '')
    time = request.POST.get('time', '')
    guests = request.POST.get('person', '')  # Fixed from 'guests' to 'person'

    if not all([name, email, mobile, date, time, guests]):
        messages.error(request, 'Please fill in all reservation fields.')
        return redirect('home')

    # 1. Save to Database
    try:
        reservation = Reservation.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            date=date,
            time=time,
            guests=guests
        )
    except Exception as e:
        messages.error(request, 'Error saving reservation. Please try again.')
        return redirect('home')

    # 2. Send WhatsApp Notification
    self.send_whatsapp_notification(name, mobile, date, time, guests)

    # 3. Return Success Message
    messages.success(request, f'Reservation confirmed for {guests} guests on {date} at {time}!')
    return redirect('home')


class IndexView(View):
    """
    Full-featured homepage view with GET and POST methods
    """

    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests - Display the homepage
        """
        # Get context data
        context = self.get_context_data()

        # Render the template with context
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests - Process contact form, newsletter signup, etc.
        """
        action = request.POST.get('action', None)
        if action == 'reservation_form':
            return self.handle_reservation(request)

        # Default: redirect to home
        return redirect('home')

    def get_context_data(self, **kwargs):
        """
        Prepare all data needed for the template
        """
        context = {}

        # ========== 6. Menu Categories (for navigation) ==========
        categories = Category.objects.filter(
            is_active=True,
            is_visible=True
        ).values("name", "slug").order_by('display_order')
        # Get top 8 categories
        context['categories'] = categories
        # =========== Menu Items ===================
        menu_items = MenuItem.objects.filter(
            is_available=True, is_active=True
        ).annotate(
            zero_last_order=Case(
                When(display_order=0, then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by(
            'zero_last_order',  # Pushes 0 values to bottom
            'display_order',  # Sorts active values ascending (1, 2, 3...)
            'name'  # Alphabetical fallback if order numbers match
        ).values("menu_item_id", "name", "description", "price", "image", "category__slug", "display_order")
        context['menu_items'] = menu_items

        # =========== 3. Dynamic Special Promotions Packages ===================
        # Fetches all active packages from the database to inject into the carousel loop
        special_packages = SpecialPackage.objects.filter(
            is_active=True
        ).order_by('-package_id')  # Newest packages appear first in sequence

        context['special_packages'] = special_packages

        # =========== Social Links ===================
        social_links = SocialLink.objects.filter(
            is_active=True
        ).order_by('display_order')

        context['social_links'] = social_links

        # =========== Restaurant Contact Info ===================
        # .first() safely gets the first record, or returns None if the database is empty
        context['contact_info'] = RestaurantInfo.objects.filter(is_active=True).first()

        # =========== Gallery Images ===================
        # Fetch all active images ordered by their display order
        context['gallery_images'] = GalleryImage.objects.filter(is_active=True)

        # =========== Chefs / Team ===================
        context['chefs'] = Chef.objects.filter(is_active=True).order_by('display_order')

        return context

    def handle_newsletter_signup(self, request):
        """
        Process newsletter email subscription
        """
        email = request.POST.get('newsletter_email', '').strip()

        if not email:
            messages.error(request, 'Please enter an email address.')
            return redirect('home')

        # TODO: Save to Newsletter model when created
        # For now, just show success message
        messages.success(request, f'Successfully subscribed with {email}!')

        return redirect('home')

    def handle_contact_form(self, request):
        """
        Process contact form submission
        """
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        message = request.POST.get('message', '').strip()

        if not all([name, email, message]):
            messages.error(request, 'Please fill in all fields.')
            return redirect('home')

        # TODO: Save to ContactMessage model or send email
        # For now, just show success
        messages.success(request, 'Thank you for your message! We will get back to you soon.')

        return redirect('home')

    def handle_reservation(self, request):
        """
            Process table reservation form, save to DB, and send WhatsApp notification
            """
        # FIX: Mapped to match the 'name' attributes in index.html exactly
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        date = request.POST.get('date', '')
        time = request.POST.get('time', '')
        guests = request.POST.get('person', '')  # Fixed from 'guests' to 'person'

        if not all([name, email, mobile, date, time, guests]):
            messages.error(request, 'Please fill in all reservation fields.')
            return redirect('home')

        # 1. Save to Database
        try:
            reservation = Reservation.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                date=date,
                time=time,
                guests=guests
            )
        except Exception as e:
            messages.error(request, 'Error saving reservation. Please try again.')
            return redirect('home')

        # # 2. Send WhatsApp Notification
        # self.send_whatsapp_notification(name, mobile, date, time, guests)

        # 3. Return Success Message
        messages.success(request,
                         f'Reservation request submitted for {guests} guests on {date} at {time}. We will verify availability and notify you soon!')
        return redirect('home')


# Alternative: Using TemplateView with extra functionality
class IndexViewWithTemplate(TemplateView):
    """
    Alternative using TemplateView with additional methods
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """Add extra context to template"""
        context = super().get_context_data(**kwargs)

        # Add your context data here
        context['featured_items'] = MenuItem.objects.filter(
            is_available=True,
            is_recommended=True
        )[:6]

        context['current_year'] = timezone.now().year

        return context

    def post(self, request, *args, **kwargs):
        """Handle POST requests"""
        context = self.get_context_data(**kwargs)
        context['form_submitted'] = True

        # Process form data
        email = request.POST.get('email')
        if email:
            messages.success(request, f'Thank you {email}!')

        return self.render_to_response(context)


# Add these alongside your existing IndexView
class PrivacyPolicyView(TemplateView):
    template_name = 'privacy.html'


class TermsConditionsView(TemplateView):
    template_name = 'terms.html'
