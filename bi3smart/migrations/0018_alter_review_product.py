# Generated by Django 5.0.4 on 2024-05-23 18:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0017_alter_review_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bi3smart.product'),
        ),
    ]
