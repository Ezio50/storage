# Generated by Django 5.1.3 on 2024-11-26 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0003_item_size_shelf_size_limit'),
    ]

    operations = [
        migrations.AddField(
            model_name='shelf',
            name='max_capacity',
            field=models.PositiveIntegerField(default=100, verbose_name='Максимальная вместимость'),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='capacity',
            field=models.PositiveIntegerField(verbose_name='Текущая вместимость'),
        ),
    ]
