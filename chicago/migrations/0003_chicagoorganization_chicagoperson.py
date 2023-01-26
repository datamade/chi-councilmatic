# Generated by Django 3.2.16 on 2023-01-08 19:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('councilmatic_core', '0052_convert_last_action_date_to_datefield'),
        ('chicago', '0002_chicagoevent'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChicagoOrganization',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('councilmatic_core.organization',),
        ),
        migrations.CreateModel(
            name='ChicagoPerson',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('councilmatic_core.person',),
        ),
    ]