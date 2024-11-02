# Generated by Django 5.1.2 on 2024-11-02 10:37

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weightage', models.DecimalField(decimal_places=2, default=0, help_text='Discount percentage (0-100)', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('due_date', models.DateField()),
            ],
        ),
    ]