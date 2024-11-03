from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Family(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # We use related_name to distinguish between admins and members
    admins = models.ManyToManyField(
        User,
        related_name='admin_of_family',
        through='FamilyAdmin',
        blank=True
    )
    
    members = models.ManyToManyField(
        User,
        related_name='member_of_family',
        through='FamilyMember',
        blank=True
    )

    def clean(self):
        # Ensure users aren't both admin and member of the same family
        admin_set = set(self.admins.all())
        member_set = set(self.members.all())
        intersection = admin_set.intersection(member_set)
        if intersection:
            raise ValidationError(
                f"Users {', '.join([user.username for user in intersection])} "
                "cannot be both admin and member of the same family"
            )

    def add_admin(self, user):
        """
        Add a user as an admin to the family
        First checks if user is already in another family
        """
        if hasattr(user, 'family_admin') or hasattr(user, 'family_member'):
            raise ValidationError(f"User {user.username} already belongs to a family")
        FamilyAdmin.objects.create(family=self, user=user)

    def add_member(self, user):
        """
        Add a user as a member to the family
        First checks if user is already in another family
        """
        if hasattr(user, 'family_admin') or hasattr(user, 'family_member'):
            raise ValidationError(f"User {user.username} already belongs to a family")
        FamilyMember.objects.create(family=self, user=user)

    def remove_user(self, user):
        """Remove a user from the family regardless of their role"""
        FamilyAdmin.objects.filter(family=self, user=user).delete()
        FamilyMember.objects.filter(family=self, user=user).delete()

    def get_all_users(self):
        """Get all users (both admins and members) in the family"""
        return list(self.admins.all()) + list(self.members.all())

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Families"


class FamilyAdmin(models.Model):
    """Through model for Family-Admin relationship"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='family_admin'
    )
    added_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        # Ensure user isn't already a member of another family
        if hasattr(self.user, 'family_member'):
            raise ValidationError(
                f"User {self.user.username} is already a member of another family"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('family', 'user')


class FamilyMember(models.Model):
    """Through model for Family-Member relationship"""
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='family_member'
    )

    def clean(self):
        # Ensure user isn't already an admin of another family
        if hasattr(self.user, 'family_admin'):
            raise ValidationError(
                f"User {self.user.username} is already an admin of another family"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('family', 'user')

class Invitation(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')