# Generated by Django 5.0.4 on 2024-05-21 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0005_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
