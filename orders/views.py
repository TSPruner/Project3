from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime

from .models import Pizza, PizzaTopping, SubTopping, Subs, Pasta, Salads, FoodOrder

# Create your views here.
def index(request):
    count = 0
    total = 0
    if request.user.is_authenticated:
        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        admin_user = user.is_superuser
        reg_user = not admin_user
    else:
        username = None
        reg_user = False

    if reg_user:
        request.session['order_id'] = 0

        order = FoodOrder.objects.filter(username=username).filter(status=1)
        if order.exists():
            request.session['order_id'] = order.first().orderId
            for item in order:
                if item.itemChoice > 0:
                    total = total + item.price
                    if item.itemChoice != 3:
                        count = count + 1
            request.session['order_count'] = count
            request.session['order_total'] = str(total)
        else:        
            request.session['order_count'] = 0
            request.session['order_total'] = 0
            found = True
            try:
                order_all = FoodOrder.objects.all().order_by('orderId')
            except FoodOrder.DoesNotExist:
                request.session['order_id'] = 1
                found = False

            if found:
                if order_all.exists():
                    order_last = order_all.last()
                    request.session['order_id'] =  order_last.orderId + 1
                else:
                    request.session['order_id'] = 1

    menus = [1, 2, 3, 4, 5, 6, 7]
    note = "* Included in Special"
    context = {
        "user": username,
        "reg_user": reg_user,
        "count": count,
        "menus": menus,
        "regularPizzas": Pizza.objects.filter(crustType="Regular").order_by('numToppings'),
        "sicilianPizzas": Pizza.objects.filter(crustType="Sicilian").order_by('numToppings'),
        "pizzaToppings": PizzaTopping.objects.all(),
        "noteToppings": note,
        "subs": Subs.objects.all(),
        "pasta": Pasta.objects.filter(size="Reg"),
        "salads": Salads.objects.filter(size="Reg"),
        "dinnerSalads": Salads.objects.exclude(size="Reg"),
        "dinnerPasta": Pasta.objects.exclude(size="Reg"),
    }
    return render(request, "orders/index.html", context)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        first = request.POST["first"]
        last = request.POST["last"]
        try:
            user = User.objects.get(username=username)
            return render(request, "users/register.html", {"message": "Username already exists."})
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password, first_name=first, last_name=last)
            user.save()
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "users/register.html", {"message": None})

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "users/login.html", {"message": "Login with your credentials."})
       
def logout_view(request):
    request.session['order_count'] = 0
    request.session['order_total'] = 0
    request.session['order_id'] = 0
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out."})

def view_order(request):
    if not request.user.is_authenticated:
        return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

    username = request.user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, "users/register.html", {"message": "User does not exists."})

    found = False
    admin_user = user.is_superuser
    reg_user = not admin_user
    if admin_user:
        order = FoodOrder.objects.exclude(status=0).exclude(status=1).order_by('orderId')
        if order.exists():
            found = True
    else:
        order = FoodOrder.objects.filter(username=username).exclude(status=0).exclude(status=1).order_by('orderId')
        if order.exists():
            found = True

    if found:
        context = {
            "user": request.user,
            "reg_user": reg_user,
            "submitted": order.filter(status=2).order_by('orderId'),
            "inProgress": order.filter(status=3).order_by('orderId'),
            "assembling": order.filter(status=4).order_by('orderId'),
            "cooking": order.filter(status=5).order_by('orderId'),
            "packaging": order.filter(status=6).order_by('orderId'),
            "completed": order.filter(status=7).order_by('orderId'),
        }
        return render(request, "orders/viewOrder.html", context)

    context = {
        "reg_user": reg_user,
        "tab": "view",
        "message": "No orders found for user.",
    }
    return render(request, "orders/error.html", context)

def order_status(request, order_id):
    if request.method == "POST":
        username = request.user
        update_item = request.POST.get('update')
        order_id = request.POST.get('orderId')

        item_count = 0
        if update_item is not None:
            try:
                order = FoodOrder.objects.get(pk=update_item)
            except FoodOrder.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "status",
                    "message": "Item to remove does not exist.",
                }
                return render(request, "orders/error.html", context)

            index = order.id
            order_id = order.orderId
            order.status = order.status + 1
            order.save()

            # update toppings for pizza and subs
            item_count = 1
            more_items = True
            if order.itemChoice <= 4:
                while more_items:
                    try:
                        next_order = FoodOrder.objects.get(pk=index+item_count)
                    except FoodOrder.DoesNotExist:
                        more_items = False
 
                    if more_items:
                        # check if item is a topping
                        if next_order.itemChoice == 0 or next_order.itemChoice == 3:
                            next_order.status = order.status
                            next_order.save()
                            item_count = item_count + 1
                        else:
                            more_items = False

            if order.status == 7:
                return HttpResponseRedirect(reverse("viewOrder"))

        if order_id is not None:
            return HttpResponseRedirect(reverse("orderStatus", args=(order_id,)))

        context = {
            "user": request.user,
        }
        return render(request, "orders/viewOrder.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        username = request.user
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})

        if order_id > 0:
            context = {
                "user": request.user,
                "order_id": order_id,
                "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            }
        else:
            context = {
                "user": request.user,
                "order_id": order_id,
            }
        return render(request, "orders/orderStatus.html", context)

def view_cart(request):
    order_id = request.session['order_id'] 
    total = float(request.session['order_total'])
    count = request.session['order_count']

    if request.method == "POST":
        username = request.user
        remove_item = request.POST.get('remove')
        
        item_count = 0
        if remove_item is not None:
            try:
                order = FoodOrder.objects.get(pk=remove_item)
            except FoodOrder.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "cart",
                    "message": "Item to remove does not exist.",
                }
                return render(request, "orders/error.html", context)

            order.status = 0
            order.save()
            item_count = item_count + 1
            total = total - float(order.price)
            request.session['order_total'] = str(total)
            request.session['order_count'] = count - 1

            # remove toppings for pizza and subs
            more_items = True
            index = order.id
            if order.itemChoice <= 4:
                while more_items:
                    try:
                        next_order = FoodOrder.objects.get(pk=index+item_count)
                    except FoodOrder.DoesNotExist:
                        more_items = False
                    if more_items:
                        # check if item is a topping
                        if next_order.itemChoice == 0 or next_order.itemChoice == 3:
                            next_order.status = 0
                            next_order.save()
                            item_count = item_count + 1
                            if next_order.itemChoice == 3:
                                total = total - float(next_order.price)
                                request.session['order_total'] = str(total)
                        else:
                            more_items = False

            if request.session['order_count'] < 1:
                request.session['order_id'] = 0
                return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(reverse("viewCart"))
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        if count <= 0:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "No items found in cart. Please try again.",
            }
            return render(request, "orders/error.html", context)

        context = {
            "user": request.user,
            "count": count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).filter(status=1).order_by('id'),
            "total": total,
        }
        return render(request, "orders/viewCart.html", context)

def place_order(request):
    username = request.user

    if request.method == "POST":
        order_id = request.session['order_id'] 
        total = float(request.session['order_total'])
        count = request.session['order_count']
        
        try:
            order = FoodOrder.objects.filter(orderId=order_id).filter(status=1)
        except FoodOrder.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "order",
                "message": "Items to order cannot be found.",
            }
            return render(request, "orders/error.html", context)

        if order.exists():
            for order_next in order:
                if (order_next.status != 0):
                    order_next.status = 2
                    order_next.save()

            request.session['order_id'] = 0
            request.session['order_total'] = 0
            request.session['order_count'] = 0
            return render(request, "orders/success.html", {"message": "Your order has been successfully submitted."})

            context = {
                "reg_user": True,
                "tab": "order",
                "message": "Items to order cannot be found.",
            }
            return render(request, "orders/error.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "users/register.html", {"message": "User does not exists."})
        
        order_id = request.session['order_id'] 
        total = float(request.session['order_total'])
        count = request.session['order_count']
        
        if count <= 0:
            context = {
                "reg_user": True,
                "tab": "order",
                "message": "No items found in cart. Please try again.",
            }
            return render(request, "orders/error.html", context)

        context = {
            "user": request.user,
            "count": count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": total,
        }
        return render(request, "orders/placeOrder.html", context)
    
def reg_pizza(request):
    note = "* Included in Special"

    if request.method == "POST":
        username = request.user
        num_toppings = int(request.POST["numToppings"])
        size = request.POST["size"]
        topping_list = []
        
        if (num_toppings > 3):
            special_toppings = PizzaTopping.objects.filter(incInSpecial=True).count()
        else: 
            special_toppings = num_toppings

        item = 0
        while (item < special_toppings):
            if (item == 0):
                topping_list.append(request.POST['topping1'])
            elif (item == 1):
                topping_list.append(request.POST['topping2'])
            elif (item == 2):
                topping_list.append(request.POST['topping3'])
            elif (item == 3):
                topping_list.append(request.POST['topping4'])
            elif (item == 4):
                topping_list.append(request.POST['topping5'])
            else:
                topping_list.append(request.POST['topping6'])
            item = item + 1

        # add pizza to order table
        try:
            pizza = Pizza.objects.get(crustType="Regular", numToppings=num_toppings, size=size)
        except Pizza.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Pizza type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(pizza)
        new_order = FoodOrder(username=username, itemId=pizza.id, price=pizza.price, itemChoice=1, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(pizza.price)
        request.session['order_total'] = str(order_total)

        # add toppings to order table
        item = 0
        while (item < len(topping_list)):
            try:
                topping = PizzaTopping.objects.get(item=topping_list[item])
            except PizzaTopping.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "cart",
                    "message": "Pizza type added to cart not found. Please try again.",
                }
                return render(request, "orders/error.html", context)  
            item_desc = str(topping)
            new_order = FoodOrder(username=username, itemId=topping.id, price=0, itemChoice=0, orderId=order_id, itemDesc=item_desc)
            new_order.save()
            item = item + 1

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "regularPizzas": Pizza.objects.filter(crustType="Regular").order_by('numToppings'),
            "pizzaToppings": PizzaTopping.objects.all(),
            "noteToppings": note,
        }
        # need to check if user is in customer db and then if authenticated
        return render(request, "orders/regPizza.html", context)
  
def sic_pizza(request):
    note = "* Included in Special"

    if request.method == "POST":
        username = request.user
        num_toppings = int(request.POST["numToppings"])
        size = request.POST["size"]
        topping_list = []
        
        if (num_toppings > 3):
            special_toppings = PizzaTopping.objects.filter(incInSpecial=True).count()
        else: 
            special_toppings = num_toppings

        item = 0
        while (item < special_toppings):
            if (item == 0):
                topping_list.append(request.POST['topping1'])
            elif (item == 1):
                topping_list.append(request.POST['topping2'])
            elif (item == 2):
                topping_list.append(request.POST['topping3'])
            elif (item == 3):
                topping_list.append(request.POST['topping4'])
            elif (item == 4):
                topping_list.append(request.POST['topping5'])
            else:
                topping_list.append(request.POST['topping6'])
            item = item + 1

        # add pizza to order table
        try:
            pizza = Pizza.objects.get(crustType="Sicilian", numToppings=num_toppings, size=size)
        except Pizza.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Pizza type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(pizza)
        new_order = FoodOrder(username=username, itemId=pizza.id, price=pizza.price, itemChoice=2, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(pizza.price)
        request.session['order_total'] = str(order_total)

        # add toppings to order table
        item = 0
        while (item < len(topping_list)):
            try:
                topping = PizzaTopping.objects.get(item=topping_list[item])
            except PizzaTopping.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "cart",
                    "message": "Pizza type added to cart not found. Please try again.",
                }
                return render(request, "orders/error.html", context)  
            item_desc = str(topping)
            new_order = FoodOrder(username=username, itemId=topping.id, price=0, itemChoice=0, orderId=order_id, itemDesc=item_desc)
            new_order.save()
            item = item + 1

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        context = {
            "sicilianPizzas": Pizza.objects.filter(crustType="Sicilian").order_by('numToppings'),
            "pizzaToppings": PizzaTopping.objects.all(),
            "noteToppings": note,
        }
        # need to check if user is in customer db and then if authenticated
        return render(request, "orders/sicPizza.html", context)
  
def sub_order(request):
    num_toppings_count = SubTopping.objects.filter(avail=True).count()
    # don't count mushrooms, peppers, onions, and extra cheese 
    num_toppings_count = num_toppings_count - 4

    if request.method == "POST":
        username = request.user
        sub_type = request.POST["subType"]
        size = request.POST["size"]
        topping_list = []
                
        item = 0
        item_count = 0
        while (item < num_toppings_count):
            if (item == 0):
                topping = request.POST['topping1']
                if topping != "Please Select":
                    topping_list.append(topping)
                    item_count = item_count + 1
            elif (item == 1):
                topping = request.POST['topping2']
                if topping != "Please Select":
                    topping_list.append(topping)
                    item_count = item_count + 1
            elif (item == 2):
                topping = request.POST['topping3']
                if topping != "Please Select":
                    topping_list.append(topping)
                    item_count = item_count + 1
            elif (item == 3):
                topping = request.POST['topping4']
                if topping != "Please Select":
                    topping_list.append(topping)
                    item_count = item_count + 1
            elif (item == 4):
                topping = request.POST['topping5']
                if topping != "Please Select":
                    topping_list.append(topping)
                    item_count = item_count + 1
            else:
                topping = request.POST['topping6']
                if topping != "Please Select":
                    topping_list.append(topping)
                    item_count = item_count + 1
            item = item + 1

        # add sub to order table
        try:
            sub = Subs.objects.get(subType=sub_type, size=size)
        except Subs.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Sub type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(sub)
        new_order = FoodOrder(username=username, itemId=sub.id, price=sub.price, itemChoice=4, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(sub.price)
        request.session['order_total'] = str(order_total)

        topping = request.POST['topping7']
        if topping != "Please Select":
            topping_list.append(topping)
            item_count = item_count + 1

        if sub.mushroomsAvail:
            topping = request.POST['topping8']
            if topping != "Please Select":
                topping_list.append(topping)
                item_count = item_count + 1
        if sub.peppersAvail:
            topping = request.POST['topping9']
            if topping != "Please Select":
                topping_list.append(topping)
                item_count = item_count + 1
        if sub.onionsAvail:
            topping = request.POST['topping10']
            if topping != "Please Select":
                topping_list.append(topping)
                item_count = item_count + 1

        # add toppings to order table
        item = 0
        while (item < len(topping_list)):
            try:
                topping = SubTopping.objects.get(item=topping_list[item])
            except SubTopping.DoesNotExist:
                context = {
                    "reg_user": True,
                    "tab": "cart",
                    "message": "Sub type added to cart not found. Please try again.",
                }
                return render(request, "orders/error.html", context) 
            item_desc = str(topping)
            price = topping.price
            order_total = order_total + float(price)
            request.session['order_total'] = str(order_total)
            new_order = FoodOrder(username=username, itemId=topping.id, price=price, itemChoice=3, orderId=order_id, itemDesc=item_desc)
            new_order.save()
            item = item + 1

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to place orders."})

        xtra_price = Subs.objects.last().extrasPrice

        context = {
            "subs": Subs.objects.all(),
            "Mushrooms": Subs.objects.filter(mushroomsAvail=True),
            "Peppers": Subs.objects.filter(peppersAvail=True),
            "Onions": Subs.objects.filter(onionsAvail=True),
            "Xcheese": Subs.objects.all(),
            "count": num_toppings_count,
            "price": xtra_price,
            "subToppings": SubTopping.objects.filter(avail=True),
        }
        # need to check if user is in customer db and then if authenticated
        return render(request, "orders/subOrder.html", context)

def pasta(request):
    if request.method == "POST":
        username = request.user
        pasta_type = request.POST["pastaType"]
        
        # add pasta to order table
        try:
            pasta = Pasta.objects.get(pastaType=pasta_type, size="Reg")
        except Pasta.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Pasta type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(pasta)
        new_order = FoodOrder(username=username, itemId=pasta.id, price=pasta.price, itemChoice=5, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(pasta.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,
        }
        return render(request, "orders/viewCart.html", context)
    else:
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        context = {
            "pasta": Pasta.objects.filter(size="Reg"),
        }
        return render(request, "orders/pasta.html", context)
              
def salad(request):
    if request.method == "POST":
        username = request.user
        salad_type = request.POST["saladType"]

        # add salad to order table
        try:
            salad = Salads.objects.get(saladType=salad_type, size="Reg")
        except Salads.DoesNotExist:
            context = {
                "reg_user": True,
                "tab": "cart",
                "message": "Salad type added to cart not found. Please try again.",
            }
            return render(request, "orders/error.html", context)  
        
        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        order_id = request.session.get('order_id')
        order_total = float(request.session.get('order_total'))
        order_count = request.session.get('order_count')
        item_desc = str(salad)
        new_order = FoodOrder(username=username, itemId=salad.id, price=salad.price, itemChoice=6, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
        new_order.save()
        order_count = order_count + 1
        request.session['order_count'] = order_count
        order_total = order_total + float(salad.price)
        request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,
        }
        return render(request, "orders/viewCart.html", context)
    else:    
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        context = {
            "salad": Salads.objects.filter(size="Reg"),
        }
        return render(request, "orders/salad.html", context)
     
def dinner(request):
    if request.method == "POST":
        username = request.user
        dinner_pasta = request.POST["pastaType"]
        dinner_salad = request.POST["saladType"]
        size = request.POST["size"]
        salad_found = True
        pasta_found = True

        # add dinner to order table
        if dinner_salad != "Please Select":
            try:
                dinner = Salads.objects.get(saladType=dinner_salad, size=size)
            except Salads.DoesNotExist:
                salad_found = False
        elif dinner_pasta != "Please Select":
            try:
                dinner = Pasta.objects.get(pastaType=dinner_pasta, size=size)
            except Pasta.DoesNotExist:
                pasta_found = False
        else:
            pasta_found = False
            salad_found = False

        try:
            comment = request.POST["comment"]
        except ValueError:
            comment = " "

        if salad_found or pasta_found:
            order_id = request.session.get('order_id')
            order_total = float(request.session.get('order_total'))
            order_count = request.session.get('order_count')
            item_desc = str(dinner)
            if pasta_found:
                new_order = FoodOrder(username=username, itemId=dinner.id, price=dinner.price, itemChoice=7, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
            else:
                new_order = FoodOrder(username=username, itemId=dinner.id, price=dinner.price, itemChoice=8, orderId=order_id, itemDesc=item_desc, specialInstructions=comment)
            order_total = order_total + float(dinner.price)
            new_order.save()
            order_count = order_count + 1
            request.session['order_count'] = order_count
            request.session['order_total'] = str(order_total)

        context = {
            "user": request.user,
            "count": order_count,
            "orderId": order_id,
            "order": FoodOrder.objects.filter(orderId=order_id).exclude(status=0).order_by('id'),
            "total": order_total,
        }
        return render(request, "orders/viewCart.html", context)
    else: 
        if not request.user.is_authenticated:
            return render(request, "users/login.html", {"message": "User must be logged in to view orders."})

        context = {
            "dinnerSalad": Salads.objects.exclude(size="Reg"),
            "dinnerPasta": Pasta.objects.exclude(size="Reg"),
        }
        return render(request, "orders/dinner.html", context)
