# Generated by Django 4.2.11 on 2024-03-23 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joblist', '0005_alter_recruiter_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
                ('job', models.CharField(max_length=150)),
                ('applied_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(max_length=150)),
            ],
        ),
    ]
