# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='elements_table',
            fields=[
                ('elements_id', models.AutoField(serialize=False, primary_key=True)),
                ('parent_id', models.IntegerField()),
                ('required', models.BooleanField(default=False)),
                ('description', models.TextField()),
                ('title', models.CharField(max_length=1000)),
                ('priority', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='form_table',
            fields=[
                ('form_id', models.AutoField(serialize=False, primary_key=True)),
                ('form_permissions', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='form_object_table',
            fields=[
                ('form', models.ForeignKey(primary_key=True, serialize=False, to='online_forms.form_table')),
                ('response_url', models.CharField(unique=True, max_length=100)),
                ('form_url', models.CharField(unique=True, max_length=100)),
                ('form_title', models.CharField(max_length=200)),
                ('form_description', models.CharField(max_length=500)),
                ('flag', models.BooleanField(default=True, verbose_name=b'Form is Active or Not')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='group_table',
            fields=[
                ('group_id', models.AutoField(serialize=False, primary_key=True)),
                ('permissions', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='input_object_table',
            fields=[
                ('input_id', models.AutoField(serialize=False, primary_key=True)),
                ('input_type', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='response_object_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('response_string', models.TextField()),
                ('response_time', models.DateField()),
                ('elements', models.ForeignKey(to='online_forms.elements_table')),
                ('form', models.ForeignKey(to='online_forms.form_table')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='user_info',
            fields=[
                ('group', models.ForeignKey(primary_key=True, serialize=False, to='online_forms.group_table')),
                ('first_name', models.CharField(max_length=200, null=True)),
                ('last_name', models.CharField(max_length=200, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='user_table',
            fields=[
                ('user_id', models.AutoField(serialize=False, primary_key=True)),
                ('username', models.CharField(unique=True, max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user_info',
            name='user',
            field=models.ForeignKey(to='online_forms.user_table'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='response_object_table',
            name='user',
            field=models.ForeignKey(to='online_forms.user_table'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='response_object_table',
            unique_together=set([('user', 'form', 'elements')]),
        ),
        migrations.AddField(
            model_name='form_table',
            name='user',
            field=models.ForeignKey(to='online_forms.user_table'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='elements_table',
            name='Input',
            field=models.ForeignKey(to='online_forms.input_object_table'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='elements_table',
            name='form_object',
            field=models.ForeignKey(to='online_forms.form_object_table'),
            preserve_default=True,
        ),
    ]
