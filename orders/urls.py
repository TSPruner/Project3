from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("viewOrder", views.view_order, name="viewOrder"),
    path("viewCart", views.view_cart, name="viewCart"),
    path("placeOrder", views.place_order, name="placeOrder"),
    path('<int:order_id>/orderStatus', views.order_status, name="orderStatus"),
    path("regPizza", views.reg_pizza, name="regPizza"),
    path("sicPizza", views.sic_pizza, name="sicPizza"),
    path("subOrder", views.sub_order, name="subOrder"),
    path("salad", views.salad, name="salad"),
    path("pasta", views.pasta, name="pasta"),
    path("dinner", views.dinner, name="dinner")
]
