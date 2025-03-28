# Generated by Django 5.1.3 on 2024-11-26 11:59

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('action', models.CharField(choices=[('incoming', 'Приход'), ('outgoing', 'Расход')], max_length=8, verbose_name='Действие')),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата и время')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='journal_entries', to='storage.item', verbose_name='Товар')),
            ],
            options={
                'verbose_name': 'Запись журнала',
                'verbose_name_plural': 'Записи журнала',
            },
        ),
    ]
