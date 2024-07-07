import datetime
from hashlib import md5
from rest_framework import serializers 
from core.models import Reservation, Country
from rest_framework.exceptions import ValidationError
from datetime import  date

def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month.")


def check_expiry_year(value):
    today = datetime.datetime.now()
    print("today", today)
    print("value", value)
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year.")


def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid cvc number.")


def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid payment_method.")

class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=150, required=True)
    expiry_month = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_expiry_month],
    )
    expiry_year = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_expiry_year],
    )
    cvc = serializers.CharField(
        max_length=150,
        required=True,
        validators=[check_cvc],
    )

    # amount = serializers.DecimalField(max_digits=12, decimal_places=2, required=True)
    # paymnet_method = serializers.CharField(max_length=200, required=True)
    # currency = serializers.CharField(max_length=10, required=False)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class ResrvationSerializer(serializers.ModelSerializer):
    destination = CountrySerializer(read_only=True)
    class Meta:
        model = Reservation
        fields = '__all__'
    

    def validate_depart(self, value):
        if value < date.today():
            raise ValidationError("you can't create a reservation with a date in the past.")
        return value
        
    def validate_return_date(self, value):
        if value < date.today():
            raise ValidationError("you can't create a reservation with a date in the past.")
        return value
        
    def validate(self, data):
        if data['depart'] > data['return_date']:
            raise ValidationError("The depart date should be smaller than return date.")
        return data



        






                 


