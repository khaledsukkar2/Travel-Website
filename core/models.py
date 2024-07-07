from typing import Iterable, Optional
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

class HomePage(models.Model):
    image = models.ImageField(upload_to="home_page/images/")
    title = models.CharField(max_length=300)
    sub_title = models.CharField(max_length=600)

    def save(self,*args, **kwargs):
        if self.id and self.__class__.objects.exists():
            return ValidationError("you can only add one row for home page.")
        return super().save(*args, **kwargs)
    
class Country(models.Model):
    image = models.ImageField(upload_to="countries/images/", null=True)
    country_name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.country_name

class Reservation(models.Model):
    destination = models.ForeignKey(Country, on_delete=models.PROTECT)
    adults = models.PositiveSmallIntegerField(blank = True, default = 0)
    childs = models.PositiveSmallIntegerField(blank = True, default = 0)
    infants = models.PositiveSmallIntegerField(blank = True, default = 0)
    depart = models.DateField()
    return_date = models.DateField()

    def __str__(self) -> str:
        return f"{self.destination} : {self.id}"
    
    # def save(self, *args, **kwargs):
    #     if self.depart > self.return_date:
    #         raise ValidationError("The depart date should be smaller than return date.")
    #     super().save(*args, **kwargs)


    