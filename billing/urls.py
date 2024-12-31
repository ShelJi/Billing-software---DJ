from django.urls import path
from . import views


app_name = "billing"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('stocks/', views.StocksView.as_view(), name="stocks"),
    path('stocksearch/', views.StockSearchView.as_view(), name="stock_search"),
    path('customersearch/', views.CustomerSearchView.as_view(), name="customer_search"),
    path('save/', views.SaveBillView.as_view(), name='save_bill'),
    path('bill/', views.AllBillsView.as_view(), name="bills"),
    path('bill/<str:bill_id>/', views.SingleBillView.as_view(), name="detailed_bill"),
    path('pdf/', views.PDFView.as_view(), name="pdf"),
]
