from django.contrib import admin
from .models import Product, Income, Outcome 

# Register your models here.
admin.site.register(Product)
admin.site.register(Income)
admin.site.register(Outcome) 