# Generated by Django 5.0.4 on 2024-05-23 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bi3smart', '0009_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='user',
        ),
    ]
