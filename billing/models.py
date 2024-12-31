from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class StocksModel(models.Model):
    product_name = models.CharField(max_length=150)
    product_description = models.TextField(null=True)
    product_stock = models.IntegerField()
    product_prize = models.IntegerField()
    product_created_at = models.DateTimeField(auto_now_add=True)
    product_updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.product_name} - {self.product_stock}"
    
class CustomerModel(models.Model):
    phone_no = PhoneNumberField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    
    def __str__(self)-> str:
        return f"{self.username} - {self.phone_no}"
    
class BillIDModel(models.Model):
    bill_id = models.CharField(max_length=50)
    customer = models.ForeignKey(CustomerModel, on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return f"{self.bill_id} - {self.customer}"
    
class BillModel(models.Model):
    bill = models.ForeignKey(BillIDModel, on_delete=models.CASCADE)
    
    igst = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    
    product = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=8 ,decimal_places=2)
    quantity = models.DecimalField(max_digits=8 ,decimal_places=2)
    actualamount = models.DecimalField(max_digits=8 ,decimal_places=2)
    gstamount = models.DecimalField(max_digits=8 ,decimal_places=2)
    totalamount = models.DecimalField(max_digits=8 ,decimal_places=2)
    
    def __str__(self):
        return f"{self.product} - {self.bill.bill_id}"
    
class CompanyDetailsModel(models.Model):
    data_name = models.CharField(max_length=50, unique=True)
    account_holder_name = models.CharField(max_length=150)
    bank_acc_no = models.CharField(max_length=150)
    bank_branch = models.CharField(max_length=250)
    ifsc_code = models.CharField(max_length=150)
    gst_in = models.CharField(max_length=150)
    upi_id = models.CharField(max_length=150)
    address_line1 = models.CharField(max_length=150)
    address_line2 = models.CharField(max_length=150)
    address_line3 = models.CharField(max_length=150)
    contacts = models.CharField(max_length=150)
    invoice_status = models.BooleanField(null=True, blank=True, default=True)
    bill_type = models.CharField(max_length=50, default="Invoice", null=True, blank=True)
    
    def __str__(self):
        return self.data_name