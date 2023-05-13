# Generated by Django 3.2.18 on 2023-05-10 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('precio', models.CharField(max_length=20)),
                ('fecha_elaboracion', models.DateField()),
                ('fecha_vencimiento', models.DateField()),
                ('imagen', models.ImageField(null=True, upload_to='productos/')),
                ('estado', models.BooleanField(default=True)),
                ('categoria', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='productos.categoria')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
