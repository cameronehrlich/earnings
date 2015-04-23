# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('symbol', models.CharField(max_length=256, serialize=False, primary_key=True)),
                ('company', models.CharField(max_length=1024)),
                ('cap', models.FloatField()),
                ('recommendation', models.FloatField()),
                ('eps', models.FloatField()),
                ('number', models.IntegerField()),
                ('report_date', models.DateField()),
                ('last_report_date', models.DateField()),
                ('last_eps', models.FloatField()),
                ('time', models.CharField(max_length=256)),
                ('quarter', models.CharField(max_length=256)),
            ],
        ),
    ]
