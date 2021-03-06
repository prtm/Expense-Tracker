# Generated by Django 2.0.7 on 2018-07-13 10:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('expense_manager', '0003_auto_20180712_1926'),
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=8)),
                ('month', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(12), django.core.validators.MinValueValidator(1)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budget', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='budget',
            unique_together={('user', 'month')},
        ),
    ]
