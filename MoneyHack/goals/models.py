from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    weightage = models.DecimalField(
        max_digits=5,
        decimal_places=3,
        validators=[
            MinValueValidator(Decimal('0')),
            MaxValueValidator(Decimal('100'))
        ],
        help_text="Discount percentage (0-100)",
        default=0
    )
    due_date = models.DateField()
    icon = models.ImageField(upload_to='goal_icons/', default='../static/images/default_goal.png', null=True, blank=True)

    def __str__(self):
        return self.title