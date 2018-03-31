# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-13 21:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labreport',
            name='lab_creatinine',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=5),
        ),
        migrations.AlterField(
            model_name='temppatientdata',
            name='creatinine',
            field=models.DecimalField(decimal_places=2, default=0.5, max_digits=5),
        ),
    ]
