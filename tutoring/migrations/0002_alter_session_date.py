# Generated by Django 5.1.2 on 2024-10-25 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoring', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(),
        ),
    ]
