# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('date', models.DateTimeField(default=None)),
                ('classification', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('order', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ActionRelatedEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('entity_type', models.CharField(max_length=100)),
                ('entity_name', models.CharField(max_length=255)),
                ('organization_ocd_id', models.CharField(max_length=100, blank=True)),
                ('person_ocd_id', models.CharField(max_length=100, blank=True)),
                ('action', models.ForeignKey(related_name='related_entities', to='councilmatic_core.Action')),
            ],
        ),
        migrations.CreateModel(
            name='AgendaItemBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('note', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ocd_id', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('identifier', models.CharField(max_length=50)),
                ('bill_type', models.CharField(max_length=50)),
                ('classification', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(default=None)),
                ('date_updated', models.DateTimeField(null=True, default=None)),
                ('source_url', models.CharField(max_length=255)),
                ('source_note', models.CharField(max_length=255, blank=True)),
                ('full_text', models.TextField(blank=True)),
                ('abstract', models.TextField(blank=True)),
                ('last_action_date', models.DateTimeField(null=True, default=None)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='BillDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('bill', models.ForeignKey(related_name='documents', to='councilmatic_core.Bill')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('note', models.TextField()),
                ('url', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ocd_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('classification', models.CharField(max_length=100)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField(null=True)),
                ('all_day', models.BooleanField(default=False)),
                ('status', models.CharField(max_length=100)),
                ('location_name', models.CharField(max_length=255)),
                ('location_url', models.CharField(max_length=255, blank=True)),
                ('source_url', models.CharField(max_length=255)),
                ('source_note', models.CharField(max_length=255, blank=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventAgendaItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('order', models.IntegerField()),
                ('description', models.TextField()),
                ('event', models.ForeignKey(related_name='agenda_items', to='councilmatic_core.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('document', models.ForeignKey(related_name='events', to='councilmatic_core.Document')),
                ('event', models.ForeignKey(related_name='documents', to='councilmatic_core.Event')),
            ],
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('note', models.TextField()),
                ('entity_name', models.CharField(max_length=255)),
                ('entity_type', models.CharField(max_length=100)),
                ('event', models.ForeignKey(related_name='participants', to='councilmatic_core.Event')),
            ],
        ),
        migrations.CreateModel(
            name='LegislativeSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('identifier', models.CharField(max_length=255)),
                ('jurisdiction_ocd_id', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('label', models.CharField(max_length=255, blank=True)),
                ('role', models.CharField(max_length=255, blank=True)),
                ('start_date', models.DateField(null=True, default=None)),
                ('end_date', models.DateField(null=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ocd_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('classification', models.CharField(max_length=255, null=True)),
                ('source_url', models.CharField(max_length=255, blank=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
                ('parent', models.ForeignKey(null=True, to='councilmatic_core.Organization', related_name='children')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ocd_id', models.CharField(max_length=100, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('headshot', models.CharField(max_length=255, blank=True)),
                ('source_url', models.CharField(max_length=255)),
                ('source_note', models.CharField(max_length=255, blank=True)),
                ('website_url', models.CharField(max_length=255, blank=True)),
                ('email', models.CharField(max_length=255, blank=True)),
                ('slug', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('ocd_id', models.CharField(max_length=100, unique=True)),
                ('label', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('organization', models.ForeignKey(related_name='posts', to='councilmatic_core.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Sponsorship',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('classification', models.CharField(max_length=255)),
                ('is_primary', models.BooleanField(default=False)),
                ('bill', models.ForeignKey(related_name='sponsorships', to='councilmatic_core.Bill')),
                ('person', models.ForeignKey(related_name='sponsorships', to='councilmatic_core.Person')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(related_name='memberships', to='councilmatic_core.Organization'),
        ),
        migrations.AddField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(related_name='memberships', to='councilmatic_core.Person'),
        ),
        migrations.AddField(
            model_name='membership',
            name='post',
            field=models.ForeignKey(null=True, to='councilmatic_core.Post', related_name='memberships'),
        ),
        migrations.AddField(
            model_name='billdocument',
            name='document',
            field=models.ForeignKey(related_name='bills', to='councilmatic_core.Document'),
        ),
        migrations.AddField(
            model_name='bill',
            name='from_organization',
            field=models.ForeignKey(null=True, to='councilmatic_core.Organization', related_name='bills'),
        ),
        migrations.AddField(
            model_name='bill',
            name='legislative_session',
            field=models.ForeignKey(null=True, to='councilmatic_core.LegislativeSession', related_name='bills'),
        ),
        migrations.AddField(
            model_name='agendaitembill',
            name='agenda_item',
            field=models.ForeignKey(related_name='related_bills', to='councilmatic_core.EventAgendaItem'),
        ),
        migrations.AddField(
            model_name='agendaitembill',
            name='bill',
            field=models.ForeignKey(related_name='related_agenda_items', to='councilmatic_core.Bill'),
        ),
        migrations.AddField(
            model_name='action',
            name='bill',
            field=models.ForeignKey(null=True, to='councilmatic_core.Bill', related_name='actions'),
        ),
        migrations.AddField(
            model_name='action',
            name='organization',
            field=models.ForeignKey(null=True, to='councilmatic_core.Organization', related_name='actions'),
        ),
    ]
