from django.shortcuts import redirect
from django.http import JsonResponse

from django.views.generic import TemplateView, DetailView, ListView, View, CreateView

from .models import StocksModel, CustomerModel


class IndexView(TemplateView):
    template_name = "index.html"
    
class StocksView(ListView):
    template_name = "stocks.html"
    model = StocksModel
    # paginate_by = 1
    
class StockSearchView(ListView):
    model = StocksModel
    context_object_name = "stocks"
    
    def get_queryset(self):
        query = self.request.GET.get("query", "")
        if query:
            return StocksModel.objects.filter(product_name__icontains=query).values("product_name", "product_stock", "product_prize")[:10]
        return StocksModel.objects.all().values("id", "product_name", "product_stock", "product_prize")[:10]
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
            return JsonResponse(list(self.get_queryset()), safe=False) 
        return redirect("billing:index")

class CustomerSearchView(ListView):
    model = CustomerModel
    context_object_name = "customer"
    
    def get_queryset(self):
        query = self.request.GET.get("query", "")
        return CustomerModel.objects.filter(phone_no__icontains=query).values()[:5]
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            queryset = self.get_queryset()
            users = [
                {
                    "id": user["id"],
                    "phone_no": f"+{user['phone_no'].country_code}{user['phone_no'].national_number}",
                    "username": user["username"],
                    "email": user["email"],
                    "address": user["address"],
                }
                for user in queryset
            ]
            return JsonResponse(users, safe=False)
        return redirect("billing:index")

# class 
