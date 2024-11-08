# Generated by Django 5.1.2 on 2024-11-03 00:46

import django.core.validators
import django.db.models.deletion
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0003_invitation'),
        ('goals', '0006_alter_goal_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='FamilyGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('weightage', models.DecimalField(decimal_places=3, default=0, help_text='Discount percentage (0-100)', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0')), django.core.validators.MaxValueValidator(Decimal('100'))])),
                ('due_date', models.DateField()),
                ('icon', models.ImageField(blank=True, default='../static/images/default_goal.png', null=True, upload_to='goal_icons/')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.family')),
            ],
        ),
    ]
