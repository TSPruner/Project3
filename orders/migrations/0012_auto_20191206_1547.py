# Generated by Django 2.0.3 on 2019-12-06 20:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_orders_subtopping'),
    ]

    operations = [
        migrations.AddField(
            model_name='subs',
            name='addMushrooms',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subs',
            name='addOnions',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subs',
            name='addPeppers',
            field=models.BooleanField(default=False),
        ),
    ]
