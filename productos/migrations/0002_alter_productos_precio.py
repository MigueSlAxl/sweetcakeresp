# Generated by Django 3.2.18 on 2023-05-10 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productos',
            name='precio',
            field=models.FloatField(max_length=20),
        ),
    ]
