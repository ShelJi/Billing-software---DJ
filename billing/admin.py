from django.contrib import admin
from .models import StocksModel, CustomerModel, BillModel, BillIDModel, CompanyDetailsModel


admin.site.register(StocksModel)
admin.site.register(CustomerModel)
admin.site.register(BillIDModel)
admin.site.register(BillModel)
admin.site.register(CompanyDetailsModel)