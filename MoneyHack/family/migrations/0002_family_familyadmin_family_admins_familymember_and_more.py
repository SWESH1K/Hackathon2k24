# Generated by Django 5.1.2 on 2024-11-02 23:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('family', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Families',
            },
        ),
        migrations.CreateModel(
            name='FamilyAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_at', models.DateTimeField(auto_now_add=True)),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.family')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='family_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('family', 'user')},
            },
        ),
        migrations.AddField(
            model_name='family',
            name='admins',
            field=models.ManyToManyField(blank=True, related_name='admin_of_family', through='family.FamilyAdmin', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FamilyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='family.family')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='family_member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('family', 'user')},
            },
        ),
        migrations.AddField(
            model_name='family',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='member_of_family', through='family.FamilyMember', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='FamilyGroup',
        ),
    ]