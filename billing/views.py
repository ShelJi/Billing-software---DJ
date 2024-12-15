from django.shortcuts import redirect
from django.http import JsonResponse

from django.views.generic import TemplateView, DetailView, ListView

from .models import StocksModel


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
            return StocksModel.objects.filter(product_name__startswith=query).values("product_name", "product_stock", "product_prize")[:10]
        return StocksModel.objects.all().values("product_name", "product_stock", "product_prize")[:10]
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest': 
            return JsonResponse(list(self.get_queryset()), safe=False) 
        return redirect("billing:index")