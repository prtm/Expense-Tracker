# Generated by Django 2.0.7 on 2018-07-12 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_manager', '0002_auto_20180712_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=8),
        ),
    ]
