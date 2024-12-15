from django.contrib import admin
from .models import StocksModel, CustomerModel, PerformaModel


admin.site.register(StocksModel)
admin.site.register(CustomerModel)
admin.site.register(PerformaModel)