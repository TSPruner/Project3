from django.contrib import admin

from .models import PizzaTopping, Pizza, SubTopping, Subs, Pasta, Salads, FoodOrder

# Register your models here.
admin.site.register(PizzaTopping)
admin.site.register(Pizza)
admin.site.register(SubTopping)
admin.site.register(Subs)
admin.site.register(Pasta)
admin.site.register(Salads)
admin.site.register(FoodOrder)
