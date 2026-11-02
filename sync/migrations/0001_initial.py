# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sync',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, editable=False)),
                ('destination', models.CharField(choices=[('local', 'LOCAL'), ('remote', 'REMOTE')], max_length=10)),
                ('last_sync', models.DateTimeField(auto_now_add=True)),
                ('center', models.ForeignKey(to='custom.ExamVenue')),
            ],
        ),
    ]
