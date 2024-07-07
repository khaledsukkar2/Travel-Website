import random
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)


    def in_group(self, group_name : str):
        """This is a method to check if a user is belong to a specific group."""
        return self.groups.filter(name=group_name).exists()
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
    
    def get_verify_code(self):
        code = ""
        try:
           code = EmailVerificationCode.objects.get(email=self.email).code
        except:
            code = "-1"
        
        return code
        

    


class EmailVerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6,null=True,blank=True)


    def __str__(self):
        return f'{self.code} is generated for {self.email} '

    def save(self,*args,**kwargs):
        numbers = [i for i in range(10)]
        code =[]

        for _ in range(6):
            num = random.choice(numbers)
            code.append(num)
        code_str = ''.join(str(i) for i in code)
        self.code = code_str
        return super().save(*args,**kwargs)