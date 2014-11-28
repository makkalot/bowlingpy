# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bowlingapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='current_roll',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='roll',
            name='current_game',
            field=models.ForeignKey(default=1, to='bowlingapp.Game'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roll',
            name='current_player',
            field=models.ForeignKey(default=1, to='bowlingapp.Player'),
            preserve_default=False,
        ),
    ]
