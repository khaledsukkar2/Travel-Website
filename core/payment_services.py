import stripe
from rest_framework import status

class PaymentService:
    def process_payment(self, payment_data: dict):
        raise NotImplementedError


class StripePaymentService(PaymentService):
    def __init__(self, api_key):
        self.api_key = api_key
    
    def process_payment(self, payment_data):
        stripe.api_key = self.api_key
        try:
            amount = payment_data.get('amount', 5000)
            currency = payment_data.get('currency', 'usd')
            payment_method = payment_data.get('payment_method', "pm_card_visa")

            if not amount or not payment_method:
                return {
                    'message': "Amount and payment method are required.",
                    'status': status.HTTP_400_BAD_REQUEST
                }
            
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                payment_method_types=['card'],
            )
            
            confirm_result = stripe.PaymentIntent.confirm(
                payment_intent.id,
                payment_method=payment_method,
            )
            
            if confirm_result.status == 'succeeded':
                return {
                    'message': "Card Payment Success",
                    "amount" : amount,
                    "currency" : currency,
                    "payment_method" : payment_method,
                    'status': status.HTTP_200_OK,
                }
        except Exception as e:
            return {
                'error': f"An error occurred: {str(e)}",
                'status': status.HTTP_400_BAD_REQUEST,
                'payment_intent': {'id': None}
            }








