from django.urls import path
from . import views


app_name = "billing"

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('stocks/', views.StocksView.as_view(), name="stocks"),
    path('stocksearch/', views.StockSearchView.as_view(), name="stock_search"),
    path('pdf', views.PDFView.as_view(), name="pdf"),
    path('createpdf', views.createpdf.as_view(), name="createpdf"),
]
