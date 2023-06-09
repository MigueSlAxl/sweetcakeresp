# Generated by Django 3.2.19 on 2023-05-15 00:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_insumo', models.CharField(max_length=40)),
                ('fecha_llegada', models.DateTimeField()),
                ('fecha_vencimiento', models.DateField()),
                ('proveedor', models.CharField(max_length=30)),
                ('tipo_insumo', models.CharField(max_length=40)),
                ('numero_lote', models.IntegerField(max_length=40)),
                ('marca_producto', models.CharField(max_length=40)),
                ('cantidad', models.IntegerField(max_length=40)),
                ('imagen_supplies', models.ImageField(blank=True, null=True, upload_to='supplies/')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
    ]
