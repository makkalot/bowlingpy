# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_finished', models.BooleanField(default=False)),
                ('current_roll', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('total_score', models.IntegerField(default=0)),
                ('game', models.ForeignKey(to='bowlingapp.Game')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Roll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_ball', models.IntegerField(default=0)),
                ('second_ball', models.IntegerField(default=0)),
                ('is_prev_strike', models.BooleanField(default=False)),
                ('is_prev_prev_strike', models.BooleanField(default=False)),
                ('is_prev_spare', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='player',
            name='latest_roll',
            field=models.ForeignKey(blank=True, to='bowlingapp.Roll', null=True),
            preserve_default=True,
        ),
    ]
