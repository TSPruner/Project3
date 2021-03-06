# Generated by Django 2.0.3 on 2019-11-28 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_subs_smallavail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pastaType', models.CharField(choices=[('w/ Mozzarella', 'w/ Mozzarella'), ('w/ Meatballs', 'w/ Meatballs'), ('w/ Chicken', 'w/ Chicken')], max_length=13)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Salads',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saladType', models.CharField(choices=[('Garden Salad', 'Garden Salad'), ('Greek Salad', 'Greek Salad'), ('Antipasto', 'Antipasto'), ('Salad w/ Tuna', 'Salad w/ Tuna')], max_length=13)),
                ('price', models.DecimalField(decimal_places=2, max_digits=4)),
            ],
        ),
    ]
