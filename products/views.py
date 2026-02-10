from django.shortcuts import render
from .models import Product, Income, Outcome

# Create your views here.

def report_view(request):
    products = Product.objects.all()  #barcha praductlarim
    incomes = Income.objects.all()
    outcomes = Outcome.objects.all()
    context = {
        'products': products,
        'incomes': incomes,
        'outcomes': outcomes,
        'total_income': total_income_sum(),  # hamma kirim summam
        'total_outcome': total_outcome_sum(),
        'finished_products': finished_products(),  # tugagan praductlarim
    }
    return render(request, 'products/report.html', context)
