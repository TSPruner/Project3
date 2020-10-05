from django.db import models

# Create your models here.
class PizzaTopping(models.Model):
    item = models.CharField(max_length=20)
    avail = models.BooleanField()
    incInSpecial = models.BooleanField()
    
    def __str__(self):
        return f"w/ ID #{self.id} {self.item}"

class Pizza(models.Model):
    CHOICES = (
        (0, 'Cheese'),
        (1, '1 Item'),
        (2, '2 Items'),
        (3, '3 Items'),
        (4, 'Special'),
    )

    TYPES = (
        ('Regular', 'Regular'),
        ('Sicilian', 'Sicilian'),
    )

    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    numToppings = models.IntegerField(default=0, choices=CHOICES)
    crustType = models.CharField(max_length=10, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {dict(Pizza.CHOICES)[self.numToppings]} {self.crustType} Pizza for ${self.price}"

# Create your models here.
class SubTopping(models.Model):
    item = models.CharField(max_length=20)
    avail = models.BooleanField()
    price = models.DecimalField(default=0, max_digits=3, decimal_places=2)
    
    def __str__(self):
        return f"w/ ID #{self.id} {self.item} for ${self.price}"

class Subs(models.Model):
    TYPES = (
        ('Cheese', 'Cheese'),
        ('Italian', 'Italian'),
        ('Ham & Cheese', 'Ham & Cheese'),
        ('Meatball', 'Meatball'),
        ('Tuna', 'Tuna'),
        ('Turkey', 'Turkey'),
        ('Chicken Parmigiana', 'Chicken Parmigiana'),
        ('Eggplant Parmigiana', 'Eggplant Parmigiana'),
        ('Steak', 'Steak'),
        ('Steak & Cheese', 'Steak & Cheese'),
        ('Sausage, Peppers & Onions', 'Sausage, Peppers & Onions'),
        ('Hamburger', 'Hamburger'),
        ('Cheeseburger', 'Cheeseburger'),
        ('Fried Chicken', 'Fried Chicken'),
        ('Veggie', 'Veggie'),
    )

    SIZE = (
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    subType = models.CharField(max_length=25, choices=TYPES)
    size = models.CharField(max_length=5, choices=SIZE)
    smallAvail = models.BooleanField(default=True)
    mushroomsAvail = models.BooleanField(default=False)
    peppersAvail = models.BooleanField(default=False)
    onionsAvail = models.BooleanField(default=False)
    extrasPrice = models.DecimalField(max_digits=2, decimal_places=2)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"ID #{self.id} {self.size}, {self.subType} for ${self.price}"

class Pasta(models.Model):
    TYPES = (
        ('w/ Mozzarella', 'w/ Mozzarella'),
        ('w/ Meatballs', 'w/ Meatballs'),
        ('w/ Chicken', 'w/ Chicken'),
    )

    SIZE = (
        ('Reg', 'Reg'),
        ('Small', 'Small'),
        ('Large', 'Large'),
    )

    pastaType = models.CharField(max_length=13, choices=TYPES)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.CharField(max_length=5, choices=SIZE, default='Reg')
    dinnerAvail = models.BooleanField(default=True)

    def __str__(self):
        phrase1 = "Baked Ziti "

        phrase2 = ""
        if self.dinnerAvail:
            if self.size == 'Reg':
                phrase2 = phrase1 + self.pastaType + " for $" + str(self.price)
            else:
                if self.pastaType == 'w/ Mozzarella':
                    phrase2 = self.size + " Baked Ziti Dinner Platter for $" + str(self.price)
                elif self.pastaType == 'w/ Chicken':
                    phrase2 = self.size + " Chicken Parm Dinner Platter for $" + str(self.price)
                else:
                    phrase2 = self.size + " Meatball Parm Dinner Platter for $" + str(self.price)
        else:
            phrase2 = phrase1 + self.pastaType + " for $" + str(self.price)

        return f"ID #{self.id} {phrase2}"

class Salads(models.Model):
    TYPES = (
        ('Garden Salad', 'Garden Salad'),
        ('Greek Salad', 'Greek Salad'),
        ('Antipasto', 'Antipasto'),
        ('Salad w/ Tuna', 'Salad w/ Tuna'),
    )

    SIZE = (
        ('Reg', 'Reg'),
        ('Small', 'Small'),
        ('Large', 'Large'),
    )
    
    saladType = models.CharField(max_length=13, choices=TYPES)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    size = models.CharField(max_length=5, choices=SIZE, default='Reg')
    dinnerAvail = models.BooleanField(default=True)
    
    def __str__(self):
        phrase2 = ""
        if self.dinnerAvail:
            if self.size == 'Reg':
                phrase2 = self.saladType + " for $" + str(self.price)
            else:
                phrase2 = self.size + " " + self.saladType + " Dinner Platter for " + str(self.price)
        else:
            phrase2 = self.saladType + " for $" + str(self.price)

        return f"ID #{self.id} {phrase2}"

class FoodOrder(models.Model):
    STATE = (
        (0, 'Cancelled'),
        (1, 'Cart'),
        (2, 'Submitted'),
        (3, 'In Progress'),
        (4, 'Assembling'),
        (5, 'Cooking'),
        (6, 'Packaging'),
        (7, 'Completed'),
    )

    CHOICES = (
        (0, 'PizzaTopping'),
        (1, 'RegularPizza'),
        (2, 'SicilianPizza'),        
        (3, 'SubTopping'),
        (4, 'Subs'),
        (5, 'Pasta'),
        (6, 'Salads'),
        (7, 'DinnerPasta'),
        (8, 'DinnerSalad'),
    )
    
    username = models.CharField(max_length=50)
    itemId = models.IntegerField()
    orderId = models.IntegerField(default=0)
    itemChoice = models.IntegerField(default=0, choices=CHOICES)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    status = models.IntegerField(choices=STATE, default=1)
    itemDesc = models.CharField(default=None, max_length=100)
    specialInstructions = models.CharField(blank=True, max_length=300)

    def __str__(self):
        return f"order# {self.orderId} for customer {self.username}: {self.itemDesc}"