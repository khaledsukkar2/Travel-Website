from django.urls import path
from core import views
urlpatterns = [
    path('reservation/', views.ReservationAPIView.as_view(), name="reservation"),
    path('country/', views.CountryAPIView.as_view(), name="country"),
    path('make_payment/stripe/',views.StripePayemntAPIView.as_view(), name="payment" ),
]