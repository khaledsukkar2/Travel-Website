from django.conf import settings
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Reservation, Country
from core.serializers import ResrvationSerializer, CountrySerializer, CardInformationSerializer
from core.payment_services import StripePaymentService

class ReservationAPIView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ResrvationSerializer
    permission_classes = []

class CountryAPIView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = []


class StripePayemntAPIView(APIView):
    serializer_class = CardInformationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            payment_service = StripePaymentService(api_key=settings.STRIPE_SECRET_KEY)
            response = payment_service.process_payment(serializer.validated_data)
            return Response(response, status=response.get("status"))

        else:
            return Response({"errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




# class StripePaymentAPIView(APIView):
#     serializer_class = CardInformationSerializer
    
    # def post(self, request):
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         stripe.api_key = settings.STRIPE_SECRET_KEY
    #         response = self.stripe_card_payment(data_dict=serializer.validated_data)
    #         return Response(response, status=response.get('status', status.HTTP_200_OK))
    #     else:
    #         response = {
    #             'errors': serializer.errors,
    #             'status': status.HTTP_400_BAD_REQUEST
    #         }
    #         return Response(response, status=status.HTTP_400_BAD_REQUEST)

    # def stripe_card_payment(self, data_dict):
    #     try:
    #         payment_intent = stripe.PaymentIntent.create(
    #             amount=10000,  # Amount in cents
    #             currency='usd',
    #             payment_method_types=['card'],  
    #         )

    #         confirm_result = stripe.PaymentIntent.confirm(
    #             payment_intent.id,
    #             payment_method='pm_card_visa', 
    #         )

    #         if confirm_result.status == 'succeeded':
    #             response = {
    #                 'message': "Card Payment Success",
    #                 'status': status.HTTP_200_OK,
    #                 'payment_intent': confirm_result
    #             }
    #         else:
    #             response = {
    #                 'message': "Card Payment Failed",
    #                 'status': status.HTTP_400_BAD_REQUEST,
    #                 'payment_intent': confirm_result
    #             }
    #     except stripe.error.StripeError as e:
    #         response = {
    #             'error': f"An error occurred: {str(e)}",
    #             'status': status.HTTP_400_BAD_REQUEST,
    #             'payment_intent': {'id': None}
    #         }
    #     return response
    

# class StripePaymentAPIView(APIView):
#     serializer_class = CardInformationSerializer
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             payment_service = StripePaymentService(api_key=settings.STRIPE_SECRET_KEY)
#             response = payment_service.process_payment(serializer.validated_data)
#             return Response(response, status=response.get('status'))
#         else:
#             return Response(
#                 {'errors': serializer.errors},
#                 status=status.HTTP_400_BAD_REQUEST
#             )


# class StripePaymentService:
    # def __init__(self, api_key):
    #     self.api_key = api_key
    
    # def process_payment(self, payment_data):
    #     stripe.api_key = self.api_key
    #     try:
    #         # You might need to adjust the amount and other details based on `payment_data`
    #         # instead of hardcoding them.
    #         payment_intent = stripe.PaymentIntent.create(
    #             amount=10000,  # This should be dynamic
    #             currency='usd',
    #             payment_method_types=['card'],
    #         )
            
    #         confirm_result = stripe.PaymentIntent.confirm(
    #             payment_intent.id,
    #             payment_method='pm_card_visa',  # This should probably come from `payment_data`
    #         )
            
    #         if confirm_result.status == 'succeeded':
    #             return {
    #                 'message': "Card Payment Success",
    #                 'status': status.HTTP_200_OK,
    #                 'payment_intent': confirm_result
    #             }
    #         else:
    #             return {
    #                 'message': "Card Payment Failed",
    #                 'status': status.HTTP_400_BAD_REQUEST,
    #                 'payment_intent': confirm_result
    #             }

    #     except stripe.error.StripeError as e:
    #         return {
    #             'error': f"An error occurred: {str(e)}",
    #             'status': status.HTTP_400_BAD_REQUEST,
    #             'payment_intent': {'id': None}
    #         }