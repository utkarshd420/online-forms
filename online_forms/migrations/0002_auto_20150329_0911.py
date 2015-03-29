# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('online_forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='form_object_table',
            options={'verbose_name': 'Form', 'verbose_name_plural': 'Forms'},
        ),
        migrations.AlterUniqueTogether(
            name='response_object_table',
            unique_together=set([]),
        ),
    ]
