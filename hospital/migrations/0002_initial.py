# Generated by Django 4.0.4 on 2022-05-05 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('order', '0001_initial'),
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratorystorage',
            name='orders',
            field=models.ManyToManyField(to='order.order'),
        ),
    ]
