from django.urls import path

from AppHome.views import IndexView, PrivacyPolicyView, TermsConditionsView
urlpatterns = [
    path("", IndexView.as_view(), name="home"),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy"),
    path("terms-conditions/", TermsConditionsView.as_view(), name="terms"),
]