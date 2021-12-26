# Generated by Django 3.2.8 on 2021-11-05 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_order_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-date_created']},
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(choices=[('Pending', 'Pending'), ('Out For Delivery', 'Out For Delivery'), ('Delievred', 'Delievred')], default='Pending', null=True),
        ),
    ]
