from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import TemplateView

from AppHome.sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}

from AppHome.views import IndexView, PrivacyPolicyView, TermsConditionsView

urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy"),
    path("terms-conditions/", TermsConditionsView.as_view(), name="terms"),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
