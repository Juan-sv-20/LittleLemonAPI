# Generated by Django 5.0.1 on 2024-01-17 18:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APILemon', '0002_order_orderitem'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='delivery_crew',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='delivery_crew', to=settings.AUTH_USER_MODEL),
        ),
    ]
