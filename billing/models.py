from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime


def performa_path(instance, filename) -> str:
    today = datetime.data.today()
    return f"Performa/{today}/{filename}"

class StocksModel(models.Model):
    product_name = models.CharField(max_length=50)
    product_description = models.TextField(null=True)
    product_stock = models.IntegerField()
    product_prize = models.IntegerField()
    product_created_at = models.DateTimeField(auto_now_add=True)
    product_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.product_name} - {self.product_stock}"
    
class CustomerModel(models.Model):
    phone_no = PhoneNumberField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    
    def __str__(self)-> str:
        return f"{self.username} - {self.phone_no}"
    
class PerformaModel(models.Model):
    performa_for_user = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True)
    performa_name = models.FileField(upload_to=performa_path, max_length=100)
    performa_created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.performa_name