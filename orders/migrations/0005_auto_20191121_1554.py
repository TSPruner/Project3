# Generated by Django 2.0.3 on 2019-11-21 20:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_remove_pizza_toppings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='pizzas',
        ),
        migrations.RemoveField(
            model_name='pizzatopping',
            name='price',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
