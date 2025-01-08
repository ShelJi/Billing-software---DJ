from django.urls import path
from . import views


app_name = "billing"

urlpatterns = [
    path('temp/', views.TempDebug.as_view(), name="temp"),
    
    path('', views.IndexView.as_view(), name="index"),
    path('stocks/', views.StocksView.as_view(), name="stocks"),
    path('stocksearch/', views.StockSearchView.as_view(), name="stock_search"),
    path('customersearch/', views.CustomerSearchView.as_view(), name="customer_search"),
    path('save/', views.SaveBillView.as_view(), name='save_bill'),
    path('bill/', views.AllBillsView.as_view(), name="bills"),
    path('bill/<str:bill_id>/', views.SingleBillView.as_view(), name="detailed_bill"),
    path('pdfq/', views.PDFView.as_view(), name="pdfq"),
    path('pdfq/<int:bill_id>/', views.PDFView.as_view(), name="pdf_billq"),
    
    path('pdf/', views.PDFView.as_view(), name="pdf"), 
    path('pdf/<int:bill_id>/', views.DownloadBill.as_view(), name="pdf_bill"), 
    
    path('404_page', views.Error_404_page.as_view(), name="404_page"),
]
